from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, Table, Text, update
Base = declarative_base()



#Base = declarative_base()
#engine = create_engine('sqlite:///Systemdata.db')
#Base.metadata.bind = engine
#DBSession = sessionmaker(bind=engine)
#session = DBSession()
#Base.metadata.create_all(engine)



	# What does a survey pool contain?
	# A pool of response objects!
	# A pool of questions!
	# A list of surveys!
	# Each survey object contains:
	# The question IDs it has
	# The response IDs it has
	# Has a coursename
	# Has an ID
	# Each question object has:
	# A question ID
	# A string
	# A manFlag
	# An MCQFlag
	# Each response object contains:
	# An RID, String, QID, UID, and SID

##########################################
##########SQLALCHEMY CLASSES##############
##########################################

class UsersCourses(Base):
	__tablename__ = "users_courses"
	userid = Column(Integer, ForeignKey('USERS.zid'), primary_key=True)
	userid = Column(String, ForeignKey('COURSES.coursename'), primary_key=True)


class Users(Base):

	__tablename__ = 'USERS'
	zid = Column(String, primary_key=True)
	password = Column(String)
	permission = Column(Integer) #0 = admin, 1 = staff, 2 = student
	enrolment = relationship("Courses", secondary = users_courses, back_populates='users')
	response = relationship("Responses", back_populates='user')

	def __repr__(self):
		return "<User(zid='%s', password='%s', permission='%s')>" % (self.zid, self.password, self.permission)



class Courses(Base):

	__tablename__ = "COURSES"
	coursename = Column(String, primary_key=True, )
	users = relationship("Users", secondary='users_courses', back_populates="enrolment")
	survey = relationship("Surveys", back_populates="coursename")

	def __repr__(self):
		return "<Courses(coursename='%s')>" % (self.coursename)



class SurveysQuestions(Base):
	__tablename__ = "surveys_questions"
	qid = Column(Integer, ForeignKey('QUESTIONS.qid'),primary_key=True)
	sid = Column(Integer, ForeignKey('SURVEYS.sid'),primary_key=True)


	
class Surveys(Base):

	__tablename__ = 'SURVEYS'
	sid = Column(Integer, primary_key=True)
	course = Column(String, ForeignKey(Courses.coursename))
	stage = Column(Integer) #stage 0 = to be reviewed, stage 1 = live, stage 2 = closed

	coursename = relationship("Courses", back_populates="survey")
	questions = relationship("Questions", secondary='surveys_questions', back_populates='survey')
	responses = relationship("Responses", back_populates="survey")

	def __repr__(self):
		return "<Survey(sid='%s', course='%s', stage='%s')>" % (self.sid, self.course, self.stage)



class Questions(Base):
	
	__tablename__ = 'QUESTIONS'
	qid = Column(Integer, primary_key=True)
	string = Column(String)
	isMCQ = Column(Integer)	# 0 = text response, 1 = MCQ
	isMan = Column(Integer) #1 = Mandatory, 0 = optional
	isVis = Column(Integer) # 1 = visible, 0 is invisible

	survey = relationship('Surveys', secondary='surveys_questions', back_populates='questions')
	responses = relationship('Responses', back_populates='question')

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

	def __repr__(self):
		return "<Responses(rid='%s', string='%s', u_id='%s', q_id='%s', s_id='%s')>" % (self.rid,
													 self.string, self.u_id, self.q_id, self.s_id)




##########################################################
##########################################################
#############ACTUAL CLASSES###############################
##########################################################
##########################################################

#QUERY EXAMPLE
#session = self.DBSession()
#item = session.query(Item).filter(Item.id == item_id).one()
#session.close()

#INSERT EXAMPLE
#session = self.DBSession()
#item = Item(id=item_id, name=name, desc=desc, seller_id=owner_id, seller=seller)
#self.add_row(session, item)





class SurveySystem(object):
	def __init__(self, surveypool, questionpool, responsepool, currentuser):
		#Database config
		self.engine = create_engine('sqlite:///SystemData.db') #Creates am engine
		try:
			Base.metadata.create_all(self.engine) #Attempts to create all
		except:
			pass
		Base.metadata.bind = self.engine #Attempts to bind
		self.DBSession = sessionmaker(bind=self.engine) #Attempts to create a session

	def add_row(self, session, row):
		session.add(row)
		session.commit()
		session.close()


class Authentication(SurveySystem):
		def __init__(self):
			self._currentPerm = -1

		def isValidUser(self, username, password):
			session = self.DBSession
			retVal = session.query(Users).filter_by(zid=str(username), password=str(password)).one_or_none()
			session.close()
			return retVal

		# Create and return the new user object, and set the authentiation objects' current permission
		def loginUser(self, uid, password, permission):
			newUser = User(uid, password, permission)
			self.setPermission(permission)
			return newUser

		#Set the permission level of the user
		def setPermission(self, perm):
			self._currentPerm = perm

		#Returns the permission level of the user
		def checkPermission(permission):
			if permission == self._currentPerm:
				return True
			return False


#User class objet
class User(SurveySystem):
	def __init__(self, uid, password, permission):
		self._uid = uid
		self._password = password
		self._permission = permission
		self._courses = self.findCourses() #List of course names
		self._completed = self.findCompleted() #List of course names

	#Returns incomplete surveys
	def getIncomplete(self):
		#Because this isn't linked to the survey pool list, we require our own database interfaces
		retVal = []
		for c in self._courses:
			if c not in self._completed:
				retVal.append(c)
		return retVal

	#Returns completed surveys
	def getComplete(self):
		return self._completed

	def getCourses(self):
		return self._courses

	# Returns true if permission level pass in is user's permission level
	def isValidPermission(self, status):
		if status == self._permission:
			return True
		return False

	# Returns user's permission level
	def getPermissionLevel(self):
		return self._permission

	#Adds a survey to the list of completed surveys
	def addCompleted(self, surveyCompleted):
		self._completed.append(surveyCompleted)

	#Queries the database to attempt to determine
	def findCourses(self):
		session = self.DBSession()
		courses = session.query(Users).filter(Users.zid == self._uid).all()
		session.close()
		return courses

	def findCompleted(self):
		session = self.DBSession
		#search through responses table, and return sids for each ocurence of our zid
		#then, search through surveys table, and get 
		session.close

class QuestionPool(SurveySystem):
	def __init__(self):
		self._questions = self.findAllQuestions()

	#Add a new question to the list/database
	def addNewQuestion(self, question, entrytype, questiontype):
		question = Questions(string = str(question), isMCQ = entrytype, isMan = questiontype)
		session.add(question)
		session.commit()
		#We need to get the questionID somehow, and then add it
		newq = Question()
		session.close()
		self._questions.append(newq)

	#Return a list of all current questions objects
	def getAllQuestions(self):
		return self._questions

	# Return a list of all current mandatory question objects
	def getMandatoryQuestions(self):
		retVal = []
		for q in self._questions:
			if q.getManFlag() == 1:
				retVal.append(q)
		return retVal

	# Return a list of all current optional question objects
	def getOptionalQuestions(self):
		retVal = []
		for q in self._questions:
			if q.getManFlag() == 0:
				retVal.append(q)
		return retVal

	# Return a question object given a question ID
	def getQuestion(self, qID):
		retVal = None
		for q in self._questions:
			if q.getQID == qID:
				retVal = q
		return retVal

	# Find all questions in the database and return the list
	def findAllQuestions(self):
		session = self.DBSession
		qlist = []
		for question in session.query(Questions).all():
			qlist.append(question)
		session.close()
		return qlist

	# Locates a question in the database given a question id
	def findQuestion(self, qstring):
		session = self.DBSession
		retVal =  session.query(Questions).filter_by(string=qstring).one_or_none()
		session.close()
		return retVal

	# Removes a question given a question id
	def removeQuestion(self, questionid):
		session = self.DBSession
		session.query(Questions).filter_by(qid = questionid).delete(synchronize_session=False)
		session.commit()
		session.close()

class CoursePool(SurveySystem):
	def __init__(self):
		self._courses = self.findCoursesList()

	def getCourseList(self):
		return self._courses

	def findCourses(self, semester):
		session = self.DBSession
		courses = []
		for course in session.query(Courses).all():
			coursecode = course.coursename[:8]
			sem = course.coursename[8:]
			if sem == semester:
				if coursecode not in courses:
					courses.append(coursecode)
		session.close()
		return courses

	def findSemesters(self):
		session = self.DBSession
		semlist = []
		for semester in session.query(Courses).all():
			sem = semester.coursename[8:]
			if sem not in semlist:
				semlist.append(sem)
		session.close()
		return semlist

	def findCoursesList(self):
		session = self.DBSession
		semesters = self.getSemesters()
		courses = {}
		for sem in semesters:
			courses[sem] = self.getCourses(sem)
		session.close()
		return courses
#############################################HERE THERE BE DRAGONS#######################################################################

class SurveyPool(SurveySystem):
	def __init__(self):
		self._questionPool = QuestionPool()
		self._responsePool = ResponsePool()
		self._surveyList = self._findSurveys()

	def findSurveys():
		#SOMEONE PLEASE WRITE THIS
		#SHOULD, BASED ON THE DATABASE, CREATE A BUNCH OF SURVEY OBJECTS AND ADD THEM TO A LIST
		#IT SHOULD THEN RETURN THAT LIST

	def addNewSurvey(self, surveyname):
		thissurvey = Surveys(course = str(surveyname), stage = 0)
		session = self.DBSession
		session.add(thissurvey)
		session.commit()
		session.close()
		return thissurvey

	def getSurvey(self, coursename):
		retVal = None
		for s in self._surveyList:
			if s.getCourse() == coursename:
				retVal = s
		return retVal

	def getReviewSurveys(self):
		rslist = []
		for s in self._surveyList:
			if s.getStage() == 0:
				rslist.append(s)
		return rslist

	def getLiveSurveys(self):
		lslist = []
		for l in self._surveyList:
			if l.getStage() == 1:
				lslist.append(l)
		return lslist

	def getClosedSurveys(self):
		cslist = []
		for  in self._surveyList:
			if c.getStage() == 2:
				cslist.append(c)
		return cslist


	def getMyReviewSurveys(self, currentuser):
		cslist = []
		for  in self._surveyList:
			if c.getStage() == 2 and c.getCourse() is in currentuser.getCourses() :
				cslist.append(c)
		return cslist


	def getMyClosedSurveys(self, currentuser):
		for subject in currentuser.enrolment:
			surveys = session.query(Surveys).filter_by(course=subject.coursename, stage=2).all()
		return surveys

	def getMyLiveSurveys(self, currentuser):
		removeitem = False
		for subject in currentuser.enrolment:
			surveys = session.query(Surveys).filter_by(course=subject.coursename, stage=1).all()
			print(surveys)
		for item in surveys:
			print(item.responses)
			for resp in item.responses:
				if str(resp.u_id) == str(currentuser.zid):
					removeitem = True

			if removeitem == True:
				surveys.remove(item)
				print(surveys)
		print('final survey', surveys)
		return surveys

	def setStage(self, survey, Stage):
		survey.stage = Stage
		session.commit()

	def deleteSurvey(self, survey):
		session = self.DBSession
		session.query(Surveys).filter_by(sid=survey).delete(synchronize_session=False)
		session.commit()
		session.close()
		#ALSO NEED TO DELETE SURVEY FROM LIST

class ResponsePool(SurveySystem)
	def __init__(self):
		self._responses = self.findResponses()

	def findResponses(self):
		# SHOULD BUILD RESPONSE OBJECTS BASED ON STUFF IN DATABASE AND ADD THEM TO THE LIST
		# PLEASE CODE THIS

	def addNewResponse(self, answer, questionid, survey, user):
		session = self.DBSession
		response = Responses(string = answer, q_id = questionid, s_id = survey.sid, u_id = user.zid)
		session.add(response)
		session.commit()
		session.close()
		return response

	def removeNullResponses(self, survey):
		session.query(Responses).filter_by(s_id = survey.sid).delete(synchronize_session=False)
		session.commit()

	def getMetrics(self, currentuser, coursename):
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
#################################################### END DRAGONS#########################################################
class Question(object):
	def __init__(self, qid, qstring, manFlag, mcqFlag):
		self._qid = qid;
		self._qstring = qstring
		self._manFlag = manFlag
		self._mcqFlag = mcqFlag
		self._visflag = 1

	def getQid(self):
		return self._qid

	def getQstring(self):
		return self._qstring

	def getManFlag(self):
		return self._manFlag

	def getMCQFlag(self):
		return self._mcqFlag

	def getVisFlag(self):
		return self._visflag

	def hideQuestion(self):
		self._visflag = 0

class Response(object):
	def __init__(self, rid, sid, qid, uid, rstring):
		self._rid = rid
		self._sid = sid
		self._qid = qid
		self._uid = uid
		self._rstring = rstring

	def getRID(self):
		return self._rid

	def getSID(self):
		return self._sid

	def getQID(self):
		return self._qid

	def getUID(self):
		return self._uid

	def getRString(self):
		return self._rstring


class Survey(object):
	def __init__(self, coursename, sid):
		self._qidList = []
		self._ridList = []
		self._coursename = coursename
		self._sid = sid
		self._stage = 0

	def getQIDList(self):
		return self._qidList

	def getRIDList(self):
		return self._qidList

	def getCourse(self):
		return self._coursename

	def getSID(self):
		return self._sid

	def getStage(self):
		return self._stage

	def setStage(self, stage):
		self._stage = stage

	def addRID(self):
		self._ridList.append(rid)

	def addQIDList(self, qlist):
		self._qidList.append(qlist)

	def setRIDList(self, ridList):
		self._ridList = ridList

	def setQList(self, qlist):
		self._qidList = qlist

