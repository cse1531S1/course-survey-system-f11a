from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, Table, Text, update


Base = declarative_base()
engine = create_engine('sqlite:///Systemdata.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

users_courses = Table('users_courses', Base.metadata, 
							Column('userid', Integer, ForeignKey('USERS.zid'), primary_key=True),
							Column('coursename', String, ForeignKey('COURSES.coursename'), primary_key=True),
							)
class Users(Base):

	__tablename__ = 'USERS'
	zid = Column(String, primary_key=True)
	password = Column(String)
	permission = Column(Integer) #0 = admin, 1 = staff, 2 = student
	
	enrolment = relationship("Courses", secondary = users_courses, back_populates='users')
	response = relationship("Responses", back_populates='user')

	def isValidUser(self, username, password):
		return session.query(Users).filter_by(zid=str(username), password=str(password)).one_or_none()

	def getpermission(self):
		return self.permission

	def __repr__(self):
		return "<User(zid='%s', password='%s', permission='%s')>" % (self.zid, self.password, self.permission)



class Courses(Base):

	__tablename__ = "COURSES"
	coursename = Column(String, primary_key=True, )
	users = relationship("Users", secondary='users_courses', back_populates="enrolment")
	survey = relationship("Surveys", back_populates="coursename")

	def getCourses(self, semester):
		courses = []
		for course in session.query(Courses).all():
			coursecode = course.coursename[:8]
			sem = course.coursename[8:]
			if sem == semester:
				if coursecode not in courses:
					courses.append(coursecode)
		return courses

	def getSemesters(self):
		semlist = []
		for semester in session.query(Courses).all():
			sem = semester.coursename[8:]
			if sem not in semlist:
				semlist.append(sem)
		return semlist

	def getCoursesList(self):
		semesters = self.getSemesters()
		courses = {}
		for sem in semesters:
			courses[sem] = self.getCourses(sem)
		return courses


	def __repr__(self):
		return "<Courses(coursename='%s')>" % (self.coursename)




surveys_questions = Table('surveys_questions', Base.metadata,
							Column('qid', Integer, ForeignKey('QUESTIONS.qid'), primary_key=True),
							Column('sid', Integer, ForeignKey('SURVEYS.sid'), primary_key=True)
							)

class Surveys(Base):

	__tablename__ = 'SURVEYS'
	sid = Column(Integer, primary_key=True)
	course = Column(String, ForeignKey(Courses.coursename))
	stage = Column(Integer) #stage 0 = to be reviewed, stage 1 = live, stage 2 = closed

	coursename = relationship("Courses", back_populates="survey")
	questions = relationship("Questions", secondary='surveys_questions', back_populates='survey')
	responses = relationship("Responses", back_populates="survey")

	def addNewSurvey(self, surveyname):
		if not surveyname:
			raise Exception('InvalidInput')
		thissurvey = Surveys(course = str(surveyname), stage = 0)
		session.add(thissurvey)
		session.commit()
		return thissurvey

	def addQuestion(self, thissurvey, thisquestion):
		thissurvey.questions.append(thisquestion)
		session.commit()

	def getSurvey(self, coursename):
		return session.query(Surveys).filter_by(course = coursename).one_or_none()

	def getSurveyID(self, coursename):
		survey = session.query(Surveys).filter_by(course = coursename).one_or_none()
		return survey.sid

	def getMandatorySurveyQuestions(self, survey):
		manquestionlist = []
		for q in survey.questions:
			if q.isMan == 1:
				manquestionlist.append(q)
		return manquestionlist


	def getReviewSurveys(self):
		rslist = []
		for survey in session.query(Surveys).filter_by(stage = 0).all():
			rslist.append(survey)
		return rslist

	def getLiveSurveys(self):
		lslist = []
		for survey in session.query(Surveys).filter_by(stage = 1).all():
			lslist.append(survey)
		return lslist

	def getClosedSurveys(self):
		cslist = []
		for survey in session.query(Surveys).filter_by(stage = 2).all():
			cslist.append(survey)
		return cslist

	def getMyReviewSurveys(self, currentuser):
		for subject in currentuser.enrolment:
			surveys = session.query(Surveys).filter_by(course=subject.coursename, stage=0).all()
		return surveys
			#returns list of survey objects

	def getMyClosedSurveys(self, currentuser):
		closedsurveys = []
		for subject in currentuser.enrolment:
			surveys = session.query(Surveys).filter_by(course=subject.coursename, stage=2).all()
			if surveys:
				closedsurveys.append(surveys[0])
		return closedsurveys

	def getMyLiveSurveys(self, currentuser):
		removeitem = False
		finalsurveys = []
		for subject in currentuser.enrolment:
			survey = self.getSurvey(subject.coursename)
			if survey != None and survey.stage == 1:
				finalsurveys.append(survey)
		print(finalsurveys)
		for item in finalsurveys:
			print(item)
			if item.responses:
				for resp in item.responses:
					if str(resp.u_id) == str(currentuser.zid):
						removeitem = True

			if removeitem == True:
				finalsurveys.remove(item)
		print('final survey', finalsurveys)
		return finalsurveys

	def getQuestionsInSurvey(self, thisSurvey):
		return thisSurvey.questions

	def setStage(self, survey, Stage):
		survey.stage = Stage
		session.commit()

	def getSurveyMetrics(self, currentuser, coursename):
		thisSurvey = self.getSurvey(coursename)
		closedresponse = []
		liveresponse = []
		if thisSurvey.stage == 2:
			closedresponse = session.query(Responses).filter_by(s_id = thisSurvey.sid).all()
		if thisSurvey.stage == 1 and currentuser.zid == 'admin':
			print('live survey')
			liveresponse = session.query(Responses).filter_by(s_id = thisSurvey.sid).all()
			print('adminresponse', liveresponse)
		
		allresponses = closedresponse+liveresponse
		print('response', allresponses)
		return allresponses

	def __repr__(self):
		return "<Survey(sid='%s', course='%s', stage='%s')>" % (self.sid, self.course, self.stage)



class Questions(Base):
	
	__tablename__ = 'QUESTIONS'
	qid = Column(Integer, primary_key=True)
	string = Column(String)
	isMCQ = Column(Integer)	# 0 = text response, 1 = MCQ
	isMan = Column(Integer) #1 = Mandatory, 0 = optional
	survey = relationship('Surveys', secondary='surveys_questions', back_populates='questions')
	responses = relationship('Responses', back_populates='question')

	def addNewQuestion(self, question, entrytype, questiontype):
		if not question:
			raise Exception('InvalidInput')
 
		question = Questions(string = str(question), isMCQ = entrytype, isMan = questiontype)
		session.add(question)
		session.commit()

	def addResponseToQuestion(self, thisquestion, thisresponse):
		if not thisquestion or not thisresponse:
			raise Exception('InvalidInput') 
		thisquestion.responses.append(thisresponse)
		session.commit()

	def getAllQuestions(self):
		qlist = []
		for question in session.query(Questions).all():
			qlist.append(question)
		return qlist

	def getMandatoryQuestions(self):
		mqlist = []
		for question in session.query(Questions).filter_by(isMan = 1).all():
			mqlist.append(question)
		return mqlist

	def getOptionalQuestions(self):
		oqlist = []
		for question in session.query(Questions).filter_by(isMan = 0).all():
			oqlist.append(question)
		return oqlist

	def getQuestion(self, qstring):
		return session.query(Questions).filter_by(string=qstring).one_or_none()

	def getQuestionString(self):
		return self.string

	def getMCQ(self):
		return self.isMCQ

	def removeQuestion(self, questionid):
		if not questionid:
			raise Exception('InvalidInput')
 
		session.query(Questions).filter_by(qid = questionid).delete(synchronize_session=False)
		session.commit()

	def getQuestionFromId(self, qid):
		return session.query(Questions).filter_by(qid=qid).one()

	def __repr__(self):
		return "<Questions(qid='%s', string='%s', isMCQ='%s', isMan='%s')>" % (self.qid,
													 self.string, self.isMCQ, self.isMan)


class Responses(Base):

	__tablename__ = 'RESPONSES'
	rid = Column(Integer, primary_key=True)
	string = Column(String)
	u_id = Column(Integer, ForeignKey('USERS.zid'))
	q_id = Column(Integer, ForeignKey('QUESTIONS.qid'))
	s_id = Column(Integer, ForeignKey('SURVEYS.sid'))

	user = relationship("Users", back_populates='response') #access via Responses.user or User.responses
	question = relationship("Questions", back_populates='responses')
	survey = relationship("Surveys", back_populates="responses")

	def addNewResponse(self, answer, questionid, survey, user):
		if not survey or not user:
			raise Exception('InvalidInput')
 
		response = Responses(string = answer, q_id = questionid, s_id = survey.sid, u_id = user.zid)
		session.add(response)
		session.commit()
		return response

	def removeResponsesToSurvey(self, survey):
		session.query(Responses).filter_by(s_id = survey.sid).delete(synchronize_session=False)
		session.commit()

	def getResponseQID(self):
		return self.q_id

	def getResponseString(self):
		return self.string


	def __repr__(self):
		return "<Responses(rid='%s', string='%s', u_id='%s', q_id='%s', s_id='%s')>" % (self.rid,
													 self.string, self.u_id, self.q_id, self.s_id)
													 





Base.metadata.create_all(engine)
