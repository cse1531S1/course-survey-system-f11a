from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, Table, Text


Base = declarative_base()
engine = create_engine('sqlite:///Systemdata.db')


users_courses = Table('users_courses', Base.metadata, 
                            Column('userid', Integer, ForeignKey('USERS.zid'), primary_key=True),
                            Column('coursename', String, ForeignKey('COURSES.coursename'), primary_key=True)
                            )
class Users(Base):

    __tablename__ = 'USERS'
    zid = Column(Integer, primary_key=True)
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


class Questions(Base):
    
    __tablename__ = 'QUESTIONS'
    qid = Column(Integer, primary_key=True)
    string = Column(String)
    isMCQ = Column(Integer)	# 0 = text response, 1 = MCQ
    isMan = Column(Integer) #1 = Mandatory, 0 = optional
    survey = relationship('Surveys', secondary='surveys_questions', back_populates='questions')
    responses = relationship('Responses', back_populates='question')

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

Base.metadata.create_all(engine)







# mandar = Users(zid=5060517, password='pass123', permission = 3)
# course = Courses(coursename ='COMP1531')
# mandar.enrolment.append(course)

# if not session.query(Users).filter_by(zid='5060517').one():
#     print('adding name')
#     session.add(mandar)

# if not session.query(Courses).filter_by(coursename='COMP1531').one():
#     print('adding course')
#     session.add(course)
# #session.add(course)
# session.commit()
# print(mandar)
# print(mandar.enrolment)
