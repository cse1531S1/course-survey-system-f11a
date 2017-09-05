import csv

class SurveyPool(object):
	def __init__(self,filename):
		self._filename = filename
		self._listOfSurveys = []

	def getSurvey(semester, course):
		retVal = None
		for survey in self._listOfSurveys:
			if survey.getCourseName() == course and survey.getSemesterName() == semester:
				retVal = survey
		return retVal

	def addSurvey(newSurvey):
		self._listOfSurveys.append(newSurvey)

	def generatePool():
		with open('%s.csv' % self._filename, 'r') as csv_in:
			reader = csv.reader(csv_in)
			for row in reader:
				newSurvey = Survey(row[0],row[1])
				self.addSurvey(newSurvey)

	def storePool():
		with open('%s.csv' % self._filename, 'wb') as csv_out:
			writer = csv.writer(csv_out, delimiter = ',')
			for survey in self._listOfSurveys:
				writer.writerow(survey.getCourseName(), survey.getSemesterName())

class Survey(object):
	def __init__(self, courseName, semesterName):
		self._courseName = courseName
		self._semesterName = semesterName
		self._questionList = []
		self._responses = None

	def getCourseName():
		return self._courseName

	def getSemesterName():
		return self._semesterName
	
	def addQuestion(newQuestion):
		self._questionList.append(newQuestion)

	def setQuestions(newQuestions):
		self._questionList = newQuestions

	def getQuestions():
		return self._questions;

	def addResponse(newResponse):
		self._responses.append(newResponse)

	def setResponses(newResponses):
		self._responses = newResponses

	def getResponses():
		return self._responses

	def generateSurvey():
		with open('%s%sQ.csv' % (self._semesterName, self._courseName) , 'r') as csv_in:
			reader = csv.reader(csv_in)
			for row in reader:
				questionToAdd = Question(row[0])
				self.addQuestion(questionToAdd)

	def storeSurvey():
		with open('%s%sQ.csv' % (self._semesterName, self._courseName) , 'wb') as csv_out:
			writer = csv.writer(csv_out, delimiter = ',')
			for question in self._questionList:
				writer.writerow(question)

	def generateResponses():
		with open('%s%sA.csv' % (self._semesterName, self._courseName) , 'r') as csv_in:
			reader = csv.reader(csv_in)
			for row in reader:
				responseToAdd = Data(row)
				self.addResponse(responseToAdd)

	def storeResponses():
		with open('%s%sA.csv' % (self._semesterName, self._courseName) , 'wb') as csv_out:
			writer = csv.writer(csv_out, delimiter = ',')
			for responseList in self._responses
				writer.writerow(responseList.getData())


class Question(object):
	def __init__(self, questionString):
		self._questionString = questionString

	def getQuestionName():
		return self._questionString

	def setQuestionName(newName):
		self._questionString = newName



class Data(object):
	def __init__(self, responses):
		self._responses = responses

	def getData():
		return self._responses

	def readData(newResponses):
		self._responses = newResponses

	def addData(responseToAdd):
		self._responses.append(responseToAdd)