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

class SurveyPool(Object):
	def __init__(self, dbName):
		self._dbName = dbName
		self._surveys = []
		self._idCounter = 0
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

	def getIDCounter():
		retVal = self._idCounter
		self._idCounter++
		return retVal

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

	def clearPool(self):
		#PENDING DATABASE CONFIG

	def getQuestionList():
		return self._questions

class ResponsePool(Object):
	def __init__(self, dbName):
		self._dbName = dbName
		self._responses = []

	def getResponse(responseID):
		retVal = None
		for resp in self._responses:
			if(resp.getResponseID() == responseID):
				retVal = resp
		return retVal

	def deleteResponse(responseID):
		for resp in self._responses:
			if(resp.getResponseID() == responseID):
				self._responses.remove(resp)

	def generatePool(self):
		#PENDING DATABASE CONFIG
		
	def storePool(self):
		#PENDING DATABASE CONFIG

	def clearPool(self):
		#PENDING DATABASE CONFIG

	def getResponseList():
		return self._responses

class Survey(Object):
	def __init__(self, coursename, uniqueID):
		self._coursename = coursename
		self._uniqueID = uniqueID
		self._questionPool = QuestionPool("InitData.db")
		self._responsePool = ResponsePool("")#TBD
	
	def getCourseName(self):
		return self._coursename

	def addQuestion(self, q):
		self._questionPool.addQuestion(q)
	
	def setQuestions(self, newQuestions):
		self._questionPool.setQuestions(newQuestions)

	def getQuestions(self):
		return self._questionPool.getQuestions();

	def addResponse(self, newResponse):
		self._responsePool.addResponse(newResponse)

	def setResponses(self, newResponses):
		self._responsePool.setResponses(newResponses)

	def getResponses(self):
		return self._responsePool.getResponses()

	def generateSurvey(self):
		#TBD

	def storeSurvey(self):
		#TBD

	def generateResponses(self):
		self._responsePool.generatePool()

	def storeResponses(self):
		self._responsePool.storePool()

	def storeResponse(self, singularResponse):
		#TBD

	def storeQuestion(self, singularQuestion):
		#TBD

	def resetSurvey(self):
		self._questionPool.clearPool()
		self._responsePool.clearPool()

class Question(Object):
	def __init__(self, questionID, qString, answerType, isMandatory):
		self._questionID = questionID
		self._question = qString
		self._answerType = answerType
		self._isMandatory = isMandatory

	def getQuestionID():
		return self._questionID

	def getQuestionString():
		return self._question

	def getAswerType():
		return self._answerType

	def getIsMandatory():
		return self._isMandatory

class Response(Object):
	def __init__(self, responses):
		self._responses = responses

	def getResponse():
		return self._responses

	def setResponse(newResponseList):
		self._responses = newResponseList

	def addResponse(newResponse):
		self._responses.append(newResponse)


#FOR TOMORROW
class SQLWriter(Object):
	def _dbselect(self, query, dbName):
		connection = sqlite3.connect(dbName)
		cursorObj = connection.cursor() #Basically our file handle lol
		rows = cursorObj.execute(query) #Add the query to the command queue, get response
		connection.commit() #Execute the command queue
		results = [] 
		for row in rows: #For every tuple we've beenr eturned
			results.append(row) #Append this to our list of tuples
		cursorObj.close() #Close cursor (like fclose)
		return results #We're done

	def _dbinsert(self, query, dbName):
		connection = sqlite3.conect(dbName)
		cursorObj = connection.cursor()
		cursorObj.execute(query)
		connection.commit()
		cursorObj.close()

class CSVWriter(FileWriter)
	def readFromCSV(filename):
		retVal = []
		with open('%s' % (filename) , 'r') as csv_in:
			reader = csv.reader(csv_in)
			for row in reader:
				retVal.append(row)
		return retVal