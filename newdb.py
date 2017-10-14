from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, Table, Text
import csv

engine = create_engine('sqlite:///Systemdata.db')
Base = declarative_base()
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

# class Authentication(object):

#     def __init__(self):
#         self.engine = create_engine('sqlite:///Systemdata.db')
#         try:
#             Base.metadata.create_all(self.engine)
#         except:
#             pass
#         Base.metadata.bind = self.engine
#         self.DBSession = sessionmaker(bind=self.engine)

#     def readFromCSV(self):
#     	session = self.DBSession()
#     	with open('passwords.csv', 'r') as csv_in:
#     		reader = csv.reader(csv_in)
#     		for row in reader:
#     			print (row)
#     			'''#person = Users(zid = str(row[0]), password = str(row[1]))
#     			if str(row[2]) == 'student':
#     				person.permission = 2
				
#                 if str(row[2]) == 'staff':
#                 	person.permission = 1
#                 else:
#                 	person.permission = 0

#                 #session.add(person)
# '''
# 		with open('courses.csv','r') as csv_in:
# 			reader = csv.reader(csv_in)
# 			for row in reader:
# 				print (row)
# 				course = Courses(coursename = str(row[0])+str(row[1]))
# 				session.add(course)
		
# 		with open('enrolments.csv', 'r') as csv_in:
# 			reader = csv.reader(csv_in)
# 			for row in reader:
# 				print(row)
# 				#statement = users_courses.insert().values(userid=str(row[0]), coursename=str(row[1])+str(row[2]))
# 				#session.execute(statement)

# 		session.commit()
# 		session.close()

    # def query_user(self, user_id):
    #     session = self.DBSession()
    #     user = session.query(Users).filter(Users.zid == user_id).one()
    #     session.close()
    #     if user is not None:
    #         return user
    #     else: return None

users_courses = Table('users_courses', Base.metadata, 
							Column('userid', Integer, ForeignKey('USERS.zid'), primary_key=True),
							Column('coursename', String, ForeignKey('COURSES.coursename'), primary_key=True)
							)

class Users(Base):

    __tablename__ = 'USERS'
    zid = Column(Integer, primary_key=True)
    password = Column(String)
    permission = Column(Integer) #0 = admin, 1 = staff, 2 = student
    
    enrolment = relationship("Courses", secondary = users_courses)
    def __repr__(self):
        return "<User(zid='%s', password='%s', permission='%s')>" % (self.zid, self.password, self.permission)
#     responses = relationship("Responses")



class Courses(Base):

    __tablename__ = "COURSES"
    coursename = Column(String, primary_key=True)
    
#    users = relationship("Users", secondary = users_courses, back_populates = "COURSES")
#     survey = relationship("Surveys", back_populates="COURSES")



# surveys_questions = Table('surveys_questions', Base.metadata,
# 							Column('qid', Integer, ForeignKey('QUESTIONS.qid'), primary_key=True),
# 							Column('sid', Integer, ForeignKey('SURVEYS.sid'), primary_key=True)
# 							)

# class Surveys(Base):

# 	__tablename__ = 'SURVEYS'
# 	sid = Column(Integer, primary_key=True)
# 	course = Column(String, ForeignKey(Courses.coursename))
# 	stage = Column(Integer) #stage 0 = to be reviewed, stage 1 = live, stage 2 = closed

# 	cousename = relationship("Courses", back_populates="SURVEYS")
# 	questions = relationship("Questions", secondary='surveys_questions', back_populates='SURVEYS')
# 	responses = relationship("Responses", back_populates="SURVEYS")


# class Questions(Base):

# 	__tablename__ = 'QUESTIONS'
# 	qid = Column(Integer, primary_key=True)
# 	string = Column(String)
# 	isMCQ = Column(Integer)	# 0 = text response, 1 = MCQ
# 	isMan = Column(Integer) #1 = Mandatory, 0 = optional

# 	survey = relationship('Surveys', secondary='surveys_questions', back_populates='QUESTIONS')
# 	response = relationship('Responses', back_populates='QUESTIONS')

# class Responses(Base):

#     __tablename__ = 'RESPONSES'
#     rid = Column(Integer, primary_key=True)
#     string = Column(String)
#     u_id = Column(Integer, ForeignKey('USERS.zid'))
#     q_id = Column(Integer, ForeignKey('QUESTIONS.qid'))
#     s_id = Column(Integer, ForeignKey('SURVEYS.sid'))

#     user = relationship("Users", back_populates='RESPONSES') #access via Responses.user or User.responses
#     question = relationship("Questions", back_populates='RESPONSES')
#     survey = relationship("Surveys", back_populates="RESPONSES")

mandar = Users(zid=5060517, password='pass123', permission = 3)
#course = Courses(coursename ='COMP1531')
#mandar.enrolment.append(course)
session.add(mandar)

#session.add(course)
session.commit()
print(mandar)
print(mandar.enrolment)
