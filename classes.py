class SurveyPool(object):
	def __init__(self,filename):
		self._filename = filename
		self._listOfSurveys = []

	def getSurvey(semester, course):

	def addSurvey(newSurvey):
		self._listOfSurveys.append(newSurvey)

	def generatePool():

	def storePool():


class Survey(object):
	def __init__(self, courseName, semesterName):
		self._courseName = courseName
		self._semesterName = semesterName
		self._questionList = []

	def getCourseName():
		return self._courseName

	def getSemesterName():
		return self._semesterName
	
	def addQuestion(newQuestion):

	def setQuestions(newQuestions):
		self._questionList = newQuestions

	def getQuestions():
		return self._questions;

	def generateSurvey():

	def storeSurvey():


class Question(object):
	def __init__(self, questionString):
		self._questionString = questionString
		self._responses = None
	def getQuestionName():
		return self._questionString

	def setQuestionName(newName):
		self._questionString = newName

	def addResponse(newResponse):

	def getResponses():

class Data(object):
	def __init__(self):
		self._responses = []

	def getData():
		return self._responses

	def generateResponses():

	def storeResponses():