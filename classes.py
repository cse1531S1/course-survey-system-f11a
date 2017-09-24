class User():
	def __init__(self, newID, permLevel, DBName):
		self._dbName = DBName
		self._id = newID
		self._permLevel = permLevel
		self._courses = []
		self._notCompletedSurveys = []
		self._closedSurveys = []

	def addCourse(newCourse):
		self._courses.append(newCourse)
		self._notCompletedSurveys.append(newCourse.getCourseID())

	def addClosedSurveys(courseID):
		self._closedSurveys.append(course)

	#Given a course ID, add it to the list of closed surveys
	def nowCompleted(courseID):
		for course in self._notCompletedSurveys:
			if(course == courseID):
				self._notCompletedSurveys.remove(course)

	def getID():
		return self._id

	def getPermission():
		return self._permLevel		

	def getCourses():
		return self._courses

	def getNotCompleted():
		return _notCompletedSurveys

	def getClosedSurveys():
		return _closedSurveys

	def setID(newID):
		self._id = newID

	def setPermission(newPermLevel):
		self._permLevel = newPermLevel

	def setCourses(courseList):
		self._courses = courseList

	def setNotCompletedSurveys(newUntouchedSurveys):
		self._notCompletedSurveys = newUntouchedSurveys

	def setClosedSurveys(newClosedSurveys)
		self._closedSurveys = newClosedSurveys

#How do we know on startup what surveys are there?
#We need a list
class SurveyPool(Object):
	def __init__(self, dbName):
		self._dbName = dbName
		self._surveys = []

	def getSurvey(surveyID):
		retVal = None
		for survey in self._surveys:
			if(survey.getSurveyID() == surveyID):
				retVal = survey
		return retVal

	def addSurvey(survey):
		self._surveys.append(survey)

	def deleteSurvey(surveyID):
		for survey in self._surveys:
			if(survey.getSurveyID() == surveyID):
				self._surveys.remove(survey)

	def generatePool():
		#PENDING DATABASE CONFIG

	def storePool():
		#PENDING DATABASE CONFIG	

	def getSurveyList(self):
		return self._surveys

class QuestionPool(Object):
	def __init__(self, dbName):
		self._dbName = dbName
		self._questions = []

	def getQuestion(questionID):
		retVal = None
		for question in self._questions:
			if(question.getQuestionID() == questionID):
				retVal = question
		return retVal

	def deleteQuestion(questionID):
		for question in self._questions:
			if(question.getQuestionID() == questionID):
				self._questions.remove(question)

	def generatePool(self):
		#PENDING DATABASE CONFIG
	def storePool(self):
		#PENDING DATABASE CONFIG

	def getQuestionList():
		return self._questions

class DataPool(Object):
	def __init__(self):

class Survey(Object):
	def __init__(self):

class Question(Object):
	def __init__(self):

class Data(Object):
	def __init__(self):

class FileWriter(Object):
	def __init__(self):

class SQLWriter(FileWriter):
	def __init__(self):

class CSVWriter(FileWriter)
	def __init__(self):