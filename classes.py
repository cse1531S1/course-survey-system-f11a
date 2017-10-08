import sqlite3
import csv

class Authentication(object):
	def __init__(self):
		self._dbName = "Users.db"
	
	#Given a username/password, checks to see if it's a legit combination
	def IsValidUser(self, username, password):
		if(username == "admin" and password == "admin"):
			return True
		else:
			writer = SQLWriter()
			valid = writer.selectuser(self._dbName, (username, password))
			if (valid != []):
				return True
		return False

	#Given a username, will return a user object
	def LoginUser(self, username):
		newUser = User(0)
		if(username == "admin"):
			return newUser
		else:
			writer = SQLWriter()
			#Set permissions
			response = writer.selectid(self._dbName, 'Passwords',(username,))
			if(response[0][2] == "staff"):
				newUser.setPermission(1)
			else:
				newUser.setPermission(2)
			#Set courses
			response = writer.selectid(self._dbName, 'Enrolments',(username,))
			newUser.addCourse(response[0][1])
			#Return user object
			return newUser

	#Fill in the Users table - First, we want to zero it
	def buildUserBase(self):
		self.clearUserBase()
		writer = SQLWriter()
		with open('passwords.csv', 'r') as csv_in:
			reader = csv.reader(csv_in)
			for row in reader:
				query = "INSERT INTO Passwords VALUES ('%s','%s','%s')" % (str(row[0]), str(row[1]),str(row[2]))
				writer.dbinsert(query, self._dbName)
		with open('enrolments.csv','r') as csv_in:
			reader = csv.reader(csv_in)
			for row in reader:
				query = "INSERT INTO Enrolments VALUES ('%s','%s')" % (str(row[0]), (str(row[1])+str(row[2])))
				writer.dbinsert(query, self._dbName)

	def clearUserBase(self):
		writer = SQLWriter()
		query = "DELETE FROM Passwords"
		writer.dbinsert(query, self._dbName)
		query = "DELETE FROM Enrolments"
		writer.dbinsert(query, self._dbName)

class User(object):
	def __init__(self, permLevel):
		self._dbName = "Users.db"
		self._permLevel = permLevel
		self._courses = []
		self._notCompletedSurveys = []
		self._closedSurveys = []

	def addCourse(self,courseID):
		self._courses.append(courseID)
		self._notCompletedSurveys.append(courseID)

	def addClosedSurveys(self,courseID):
		self._closedSurveys.append(course)

	#Given a course ID, add it to the list of closed surveys
	def nowCompleted(self,courseID):
		for course in self._notCompletedSurveys:
			if(course == courseID):
				self._notCompletedSurveys.remove(course)

	def getPermission(self):
		return self._permLevel		

	def getCourses(self):
		return self._courses

	def getNotCompleted(self):
		return self._notCompletedSurveys

	def getClosedSurveys(self):
		return self._closedSurveys

	def setPermission(self,newPermLevel):
		self._permLevel = newPermLevel

	def setCourses(self,courseList):
		self._courses = courseList

	def setNotCompletedSurveys(self,newUntouchedSurveys):
		self._notCompletedSurveys = newUntouchedSurveys

	def setClosedSurveys(self,newClosedSurveys):
		self._closedSurveys = newClosedSurveys

class SurveyPool(object):
	def __init__(self):
		self._dbName = "InitData.db"
		self._surveys = []
		self._idCounter = 0

	def getSurveyByID(self,surveyID):
		retVal = None
		for survey in self._surveys:
			if(survey.getSurveyID() == surveyID):
				retVal = survey
		return retVal

	def getSurveyByName(self,surveyName):
		retVal = None
		for survey in self._surveys:
			if(survey.getCourseName() == surveyName):
				retVal = survey
		return retVal

	def addSurvey(self,surveyName):
		newSurvey = Survey(surveyName, self.getIDCounter())
		self._surveys.append(newSurvey)
		writer = SQLWriter()
		writer.dbinserts(self._dbName, surveyName)
		return newSurvey
		
	def deleteSurvey(self,surveyID):
		for survey in self._surveys:
			if(survey.getSurveyID() == surveyID):
				self._surveys.remove(survey)

	def generatePool(self):
		self.clearPool()
		writer = SQLWriter()
		query = "SELECT * FROM Surveys"
		courseList = writer.dbselect(query, self._dbName) #This is stored in the database as a series of strings
		for item in courseList:
				newSurvey = Survey(str(item), self.getIDCounter())
				newSurvey.generateQuestions()
				newSurvey.responseList.generatePool()

	def getSurveyList(self):
		return self._surveys

	def getIDCounter(self):
		retVal = self._idCounter
		self._idCounter+=1
		return retVal

	def clearPool(self):
		writer = SQLWriter()
		query = "DELETE FROM Surveys"
		writer.dbinsert(query, self._dbName)
		self._surveys = []
		self._idCounter = 0

class QuestionPool(object):
	def __init__(self):
		self._dbName = "InitData.db"
		self._questions = [] #list of question objects
		self._questionCounter = 0

	def getQuestion(self,questionID):
		retVal = None
		for question in self._questions:
			if(question.getQuestionID() == questionID):
				retVal = question
		return retVal

	def deleteQuestion(self,questionID):
		for question in self._questions:
			if(question.getQuestionID() == questionID):
				self._questions.remove(question)

	def addQuestion(self, qString, answerType, isMandatory):
		q = Question(self._questionCounter, qString, answerType, isMandatory)
		self._questions.append(q)
		self._questionCounter+=1
		writer = SQLWriter()
		writer.dbinsertq(self._dbName, self._questionCounter, answerType, isMandatory, qString)	

	def generatePool(self):
		self.clearPool()
		writer = SQLWriter()
		i = 0
		while True:
			query = "SELECT * FROM Questions WHERE rowid = %s" % str(i) 
			retVal = writer.dbselect(query, self._dbName)
			if retVal == []:
				break
			else:
				newq = Question(retVal[0], retVal[1], retVal[2], retVal[3])
				self._questions.append(newq)
				if int(retVal[0]) > self._questionCounter:
					self._questionCounter = int(retVal[0])
					self._questionCounter +=1
			i+=1

	def storePool(self):
		writer = SQLWriter()
		for q in self._questions:
			write.dbinsertq(self._dbName, q.getQuestionID(), q.getAnswerType(), q.getIsMandatory(), q.getQuestionString())
			writer.dbinsert(query, self._dbName)

	def clearPool(self):
		writer = SQLWriter()
		query = "DELETE FROM Questions"
		writer.dbinsert(query, self._dbName)
		self._questions = []
		self._questionCounter = 0

	def getQuestionList(self):
		return self._questions

class ResponsePool(object):
	def __init__(self, dbName):
		self._dbName = dbName
		self._currentID = 0
		self._responses = []

	#Given a response list, add it to the database and the pool
	def addResponse(self,responseList):
		newResponse = Response(responseList, self._currentID)
		self._currentID+=1
		writer = SQLWriter()
		#So we go through the response object, and pad it out
		#Should work as per https://stackoverflow.com/questions/8316176/insert-list-into-my-database-using-python
		toInsert = []
		for i in range(0,20):
			if(i < len(newResponse.getResponses())):
				toInsert.append(newResponse.getResponses()[i])
			else:
				toInsert.append("")
		query = "INSERT INTO Responses (q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20) VALUES %r" % (tuple(toInsert))
		writer.dbinsert(query, self._dbName)
		self._responses.append(newResponse)

	def getResponse(self,responseID):
		retVal = None
		for resp in self._responses:
			if(resp.getResponseID() == responseID):
				retVal = resp
		return retVal

	def deleteResponse(self,responseID):
		for resp in self._responses:
			if(resp.getResponseID() == responseID):
				self._responses.remove(resp)

	def generatePool(self):
		self.clearPool()
		writer = SQLWriter()
		i = 0
		while True:
			query = "SELECT * FROM Responses WHERE rowid = %s" % str(i) 
			retVal = writer.dbselect(query, self._dbName)
			if retVal == []:
				break
			else:
				newResp = Repsonse(retVal, self._currentID)
				self._currentID+=1
				self._responses.append(newResp)
			i+=1

	def getResponseList(self):
		return self._responses

	def clearPool(self):
		writer = SQLWriter()
		query = "DELETE FROM Responses"
		writer.dbinsert(query)
		self._responses = []
		self._currentID = 0

class Survey(object):
	def __init__(self, coursename, uniqueID):
		self._coursename = coursename
		self._dbName = coursename + ".db"
		self._uniqueID = uniqueID
		self._questionList = [] #The question pool is merely a list of unique numbers
		self._responsePool = ResponsePool(self._dbName)#TBD
		self._stage = 0 #stage0 = after creation, to be approved, 1 = live, 2 = closed.

	
	def getCourseName(self):
		return self._coursename

	def getSurveyID(self):
		return self._uniqueID

	#Given a question, add the question ID to the pool
	def addQuestion(self, q):
		self._questionList.append(q.getQuestionID())
		writer = SQLWriter()
		query = "INSERT INTO Questions VALUES %s" % (str(q.getQuestionID()))
		writer.dbinsert(query, self._dbName)
	
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

	def setStage(self, stage):
		self._stage = stage

	def getStage(self):
		return self._stage

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
			i+=1

	def generateResponses(self):
		self._responsePool.generatePool()

	def resetSurvey(self):
		writer = SQLWriter()
		query = "DELETE FROM Questions"
		writer.dbinsert(query, self._dbName)
		self._questionList = []
		self._responsePool.clearPool()

class Question(object):
	def __init__(self, questionID, qString, answerType, isMandatory):
		self._questionID = questionID
		self._question = qString
		self._answerType = answerType
		self._isMandatory = isMandatory

	def getQuestionID(self):
		return self._questionID

	def getQuestionString(self):
		return self._question

	def getAnswerType(self):
		return self._answerType

	def getIsMandatory(self):
		return self._isMandatory

class Response(object):
	def __init__(self, responses, ID):
		self._responses = responses
		self._responseID = ID

	def getResponse(self):
		return self._responses

	def setResponse(self,newResponseList):
		self._responses = newResponseList

	def addResponse(self,newResponse):
		self._responses.append(newResponse)

	def getResponseID(self):
		return self._responseID

class SQLWriter(object):
	def dbselect(self, query, dbName):
		connection = sqlite3.connect(dbName)
		cursorObj = connection.cursor() #Basically our file handle lol
		rows = cursorObj.execute(query) #Add the query to the command queue, get responses
		connection.commit() #Execute the command queue
		results = [] 
		for row in rows: #For every tuple we've beenr eturned
			results.append(row) #Append this to our list of tuples
		cursorObj.close() #Close cursor (like fclose)
		return results #We're done

	def selectuser(self, dbName, tupval):
		connection = sqlite3.connect(dbName)
		cursorObj = connection.cursor()
		cursorObj.execute('SELECT * FROM Passwords WHERE ZID = (?) AND PASSWORD = (?)', tupval)
		results = cursorObj.fetchall()
		connection.commit()
		cursorObj.close()
		return results #We're done

	def selectid(self, dbName, location, tupval):
		connection = sqlite3.connect(dbName)
		cursorObj = connection.cursor()
		cursorObj.execute('SELECT * FROM %s WHERE ZID = (?)'%location, tupval)
		results = cursorObj.fetchall()
		connection.commit()
		cursorObj.close() #Close cursor (like fclose)
		return results #We're done		

	def dbinsert(self, query, dbName):
		connection = sqlite3.connect(dbName)
		cursorObj = connection.cursor()
		cursorObj.execute(query)
		connection.commit()
		cursorObj.close()

	def dbinserts(self, dbName, surveyname):
		connection = sqlite3.connect(dbName)
		cursorObj = connection.cursor()
		cursorObj.execute("INSERT INTO Surveys VALUES (?)", (surveyname,))
		connection.commit()
		cursorObj.close()

	def dbinsertq(self, dbName, qid, mc, man, qstr):
		connection = sqlite3.connect(dbName)
		cursorObj = connection.cursor()
		cursorObj.execute("INSERT INTO Questions (QID, ISMCFLAG, ISMANFLAG, QSTRING) VALUES(?, ?, ?, ?)", (qid, mc, man, qstr))
		connection.commit()
		cursorObj.close()

	def dbGetRows(self, query, dbName):
		connection = sqlite3.connect(dbName)
		cursorObj = connection.cursor()
		retVal = cursorObj.execute(query)
		connection.commit()
		cursorObj.close()
		return retVal
