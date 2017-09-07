import csv
import os
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

	def deleteSurvey(self, semester, course):
		i = 0
		for survey in self._listOfSurveys:
			if survey.getCourseName() == course and survey.getSemesterName() == semester:
				self._listOfSurveys.pop(i)
			i += 1
		os.remove('%s.csv' % self._filename)
		self.storePool()

	def generatePool(self):
		with open('%s.csv' % self._filename, 'r') as csv_in:
			reader = csv.reader(csv_in)
			for row in reader:
				if row != "":
					newSurvey = Survey(row[0],row[1])
					newSurvey.generateSurvey()
					newSurvey.generateResponses()
					self.addSurvey(newSurvey)

	def storePool(self):
		with open('%s.csv' % self._filename, 'a') as csv_out:
			writer = csv.writer(csv_out)
			for survey in self._listOfSurveys:
				writer.writerow(survey.getCourseName(), survey.getSemesterName())
				toWrite = []
				toWrite.append(survey.getCourseName())
				toWrite.append(survey.getSemesterName())
				writer.writerow(toWrite)
				survey.storeSurvey()
				survey.storeResponses()
	
	def getSurveyList(self):
		return self._listOfSurveys
  
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
		if(type(newQuestion) == Question):
			self._questionList.append(newQuestion)
			print("Question added")
		else:
			print("Failure")
			print(type(newQuestion))

	def setQuestions(self, newQuestions):
		self._questionList = newQuestions

	def getQuestions(self):
		return self._questionList;

	def addResponse(self, newResponse):
		if(newResponse.getData() != []):
			self._responses.append(newResponse)
		else:
			print("Nice try lol")

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
		with open('%s%sQ.csv' % (self._semesterName, self._courseName) , 'a') as csv_out:
			writer = csv.writer(csv_out)
			#self._questionList[:] = [x for x in self._questionList if type(x) == Question]

			for question in self._questionList:
				writer.writerow([question.getQuestionName()])

	def generateResponses(self):
		with open('%s%sA.csv' % (self._semesterName, self._courseName) , 'r') as csv_in:
			reader = csv.reader(csv_in)
			for row in reader:
				responseToAdd = Data(row)
				self.addResponse(responseToAdd)

	def storeResponses(self):
		with open('%s%sA.csv' % (self._semesterName, self._courseName) , 'a') as csv_out:
			writer = csv.writer(csv_out)
			#TotalList is our list of all responses
			totalList = self.getResponses()
			#For every data object in the list
			for response in totalList:
				newStr = response.getData()
				print("The response data is:")
				print(response.getData())
				#We're going to call the getData function
				writer.writerow(newStr)
	def resetSurvey(self):
		os.remove('%s%sA.csv' % (self._semesterName, self._courseName))
		os.remove('%s%sQ.csv' % (self._semesterName, self._courseName))
		self.setQuestions([])
		self.setResponses([])

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
