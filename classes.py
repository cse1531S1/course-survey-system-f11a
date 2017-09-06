import csv

class SurveyPool(object):
	def __init__(self,filename):
		self._filename = filename
		self._listOfSurveys = []

	def getSurvey(self, semester, course):
		retVal = None
		for survey in self._listOfSurveys:
			if survey.getCourseName() == course and survey.getSemesterName() == semester:
				retVal = survey
		return retVal

	def addSurvey(self, newSurvey):
		self._listOfSurveys.append(newSurvey)

	def generatePool(self):
		with open('%s.csv' % self._filename, 'r') as csv_in:
			reader = csv.reader(csv_in)
			for row in reader:
				newSurvey = Survey(row[0],row[1])
				newSurvey.generateSurvey()
				newSurvey.generateResponses()
				self.addSurvey(newSurvey)

	def storePool(self):
		with open('%s.csv' % self._filename, 'wb') as csv_out:
			writer = csv.writer(csv_out, delimiter = ',')
			for survey in self._listOfSurveys:
				writer.writerow(survey.getCourseName(), survey.getSemesterName())

class Survey(object):
	def __init__(self, courseName, semesterName):
		self._courseName = courseName
		self._semesterName = semesterName
		self._questionList = []
		self._responses = []

	def getCourseName(self):
		return self._courseName

	def getSemesterName(self):
		return self._semesterName
	
	def addQuestion(self, newQuestion):
		self._questionList.append(newQuestion)

	def setQuestions(self, newQuestions):
		self._questionList = newQuestions

	def getQuestions(self):
		return self._questions;

	def addResponse(self, newResponse):
		self._responses.append(newResponse)

	def setResponses(self, newResponses):
		self._responses = newResponses

	def getResponses(self):
		return self._responses

	def generateSurvey(self):
		with open('%s%sQ.csv' % (self._semesterName, self._courseName) , 'r') as csv_in:
			reader = csv.reader(csv_in)
			for row in reader:
				questionToAdd = Question(row[0])
				self.addQuestion(questionToAdd)

	def storeSurvey(self):
		with open('%s%sQ.csv' % (self._semesterName, self._courseName) , 'wb') as csv_out:
			writer = csv.writer(csv_out, delimiter = ',')
			for question in self._questionList:
				writer.writerow(question)

	def generateResponses(self):
		with open('%s%sA.csv' % (self._semesterName, self._courseName) , 'r') as csv_in:
			reader = csv.reader(csv_in)
			for row in reader:
				responseToAdd = Data(row)
				self.addResponse(responseToAdd)

	def storeResponses(self):
		with open('%s%sA.csv' % (self._semesterName, self._courseName) , 'wb') as csv_out:
			writer = csv.writer(csv_out, delimiter = ',')
			totalList = getResponses()
			for responseList in totalList:
				writer.writerow(responseList.getData())


class Question(object):
	def __init__(self, questionString):
		self._questionString = questionString

	def getQuestionName(self):
		return self._questionString

	def setQuestionName(self, newName):
		self._questionString = newName



class Data(object):
	def __init__(self, responses):
		self._responses = responses

	def getData(self):
		return self._responses

	def readData(self, newResponses):
		self._responses = newResponses

	def addData(self, responseToAdd):
		self._responses.append(responseToAdd)