#CHANGE SURVEY SO THAT IT ONLY INCLUDES A LIST OF QUESTION IDS, AND NOT A QUESTION POOL

class User():
	def __init__(self, newID, permLevel, dbName):
		self._dbName = dbName
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
		self._questionCounter = 0

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

	def addQuestion(self, qString, answerType, isMandatory):
		q = Question(self._questionCounter, qString, answerType, isMandatory)
		self._questions.append(q)
		self._questionCounter++
		writer = SQLWriter()
		query = "INSERT INTO Questions (QID, QString, AnswerType, IsMandatory) VALUES ('%s', '%s', '%s', '%s')" % (self._questionCounter, qString, answerType, isMandatory)
		writer.dbinsert(query, self.dbName)	

	def generatePool(self):
		writer = SQLWriter()
		i = 0
		while True:
			query = "SELECT * FROM Questions WHERE rowid = %s" % str(i) 
			retVal = writer.dbselect(query, self.dbName)
			if retVal == []:
				break
			else:
				newq = Question(retVal[0], retVal[1], retVal[2], retVal[3])
				self._questions.append(newq)
				if int(retVal[0]) > self._questionCounter:
					self._questionCounter = int(retVal[0])
			i++

	def storePool(self):
		writer = SQLWriter()
		for q in self._questions:
			query = "INSERT INTO Questions (QID, QString, AnswerType, IsMandatory) VALUES ('%s', '%s', '%s', '%s')" % (q.getQuestionID(), q.getQuestionString(), q.getAnswerType(), q.getIsMandatory())
			writer.dbinsert(query, self.dbName)

	def clearPool(self):
		query = "DELETE * FROM Questions"
		SQLWriter.dbselect(query)
		self._questions = []
		self._questionCounter = 0

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
		self._questionList = [] #The question pool is merely a list of unique numbers
		self._responsePool = ResponsePool("")#TBD
	
	def getCourseName(self):
		return self._coursename

	#Given a question, add the question ID to the pool
	def addQuestion(self, q):
		self._questionList.append(q.getQuestionID())
	
	#Given a list of question IDs, set the list of QIDs to those questions
	def setQuestions(self, newQuestions):
		self._questionList = newQuestions

	#Return the question ID list
	def getQuestions(self):
		return self._questionList;

	#Add a response
	def addResponse(self, newResponse):
		self._responsePool.addResponse(newResponse)

	#Set the responsepool list of objects to the newly given list of objects
	def setResponses(self, newResponses):
		self._responsePool.setResponses(newResponses)

	#Returns the current list of response objects
	def getResponses(self):
		return self._responsePool.getResponses()

	def generateQuestions(self):
		writer = SQLWriter()
		i = 0
		while True:
			query = "SELECT * FROM Questions WHERE rowid = %s" % str(i) 
			retVal = writer.dbselect(query, self.dbName)
			if retVal == []:
				break
			else:
				self._questions.append(int(retVal))
			i++
	def generateResponses(self):
		self._responsePool.generatePool()

	def resetSurvey(self):
		writer = SQLWriter()
		query = "DELETE * FROM Questions"
		dbstring = self._coursename + ".db"
		writer.dbinsert(query, dbstring)
		self._questionList = []
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

	def getAnswerType():
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
	def dbselect(self, query, dbName):
		connection = sqlite3.connect(dbName)
		cursorObj = connection.cursor() #Basically our file handle lol
		rows = cursorObj.execute(query) #Add the query to the command queue, get response
		connection.commit() #Execute the command queue
		results = [] 
		for row in rows: #For every tuple we've beenr eturned
			results.append(row) #Append this to our list of tuples
		cursorObj.close() #Close cursor (like fclose)
		return results #We're done

	def dbinsert(self, query, dbName):
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