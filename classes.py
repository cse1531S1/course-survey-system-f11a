import sqlite3
import csv
from flask_login import UserMixin
# So what we need to do, is:
# Each database also has a table with a USERSCOMPLETED column
# On submission of a survey, we need to add that user to that completed columnn
# We need a function to:
# Dynamically create this column
# Given a user ID, add it to the column
# Given a user ID, determine whether or not it's in the column

#So we have an issue
#

class Authentication(object):
	def __init__(self):
		self._dbName = "Users.db"

	#Given a username/password, checks to see if it's a legit combination
	def IsValidUser(self, username, password):
		print("Step2")
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
		newUser = User(0,str(username))
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
			for r in response:
				strVersion = str(r[1])
				print("Adding: " + strVersion)
				newUser.addCourse(strVersion)
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

class User(UserMixin):
	def __init__(self, permLevel, idString):
		self._dbName = "Users.db"
		self._permLevel = permLevel
		self._courses = [] #contains list of strings of coursenames
		self._notCompletedSurveys = [] #contains list of survey objects (go with it for now)
		self._closedSurveys = [] #contains list of strings of coursenames
		self._UID = idString
#		self.__unfilled = []

	def addCourse(self,courseID):
		self._courses.append(courseID)
#		self._unfilled.append(courseID)

#	def filledIn(self, courseID):
#		for c in self._unfilled:
#			if c == courseID:
#				self._unfilled.remove(c)

#	def unfilled(self):
#		return self._unfilled

	def addClosedSurveys(self,courseID):
		self._closedSurveys.append(course)

	def getUID(self):
		return self._UID

	#Given a course ID, add it to the list of closed surveys
	################################
	#NOTE: THIS ADDS THE SURVEY TO CLOSED, WHICH IS NOT DECIDED BY ADMIN YET
	################################
	def nowCompleted(self,courseID):
		#print("NOW COMPLETED BEING ENTERED")
		#print("NOTE COMPLETED SURVEYS ARE: ")
		#print(self._notCompletedSurveys)
		#print("TOTAL COURSES ARE: ")
		#print (self._courses)
		i = 0
		for course in self._notCompletedSurveys:
			#print("*************")
			#print("In nowCompleted, we're comparing:")
			#print(course.getCourseName())
			#print(courseID)
			if course.getCourseName() == courseID:
				del self._notCompletedSurveys[i]
			i += 1
		#self._closedSurveys.append(courseID)

		i = 0
		for course in self._courses:
			if course == courseID:
				del self._courses[i]
			i += 1

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

	def populateStudentSurveys(self, surveyList):
		# Presuming that the user course list has properly been set
		#Search through surveyList, checking if course names are within our courseList
		#If so, check their current state, and add them to notCompleted if level 2, or closed if level 3
		allClear = True
		myCourses = self.getCourses() #These are the classes I should grab if they exist
		for s in surveyList: #For each survey currently there
			allClear = True
			print("Checking " + s.getCourseName())
			if s.getCourseName() in myCourses: #It was in our courses :D
				for sv in self._closedSurveys:
					print("We've listed as closed: "+sv)
					if sv == s.getCourseName(): #assumes that closedSurvey has list of strings
						allClear = False
				if(s.hasUser(str(self.getUID()))):
					allClear = False
				if allClear:
					if s.getStage() == 2:
						self._notCompletedSurveys.append(s)
					elif s.getStage():
						self._closedSurveys.append(s.getCourseName())

	def populateStaffSurveys(self, surveyList):
		#in this understanding, notCompleted = to be reviewed surveys, closed = closed surveys
		self.resetCourses()
		myCourses = self.getCourses()
		print(myCourses)
		for s in surveyList:
			print("Checking " ,s.getCourseName(),s.getStage())
			if s.getCourseName() in myCourses:
				print("It was in our courses!")
				print("Stage is", s.getStage())
				if s.getStage() == 1:
					self._notCompletedSurveys.append(s)
				elif s.getStage() == 3:
					self._closedSurveys.append(s)

class SurveyPool(object):
	def __init__(self):
		self._dbName = "InitData.db"
		self._surveys = []

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
		newSurvey = Survey(surveyName, 0)
		self._surveys.append(newSurvey)
		writer = SQLWriter()
		writer.dbinserts(self._dbName, surveyName, newSurvey.getStage())
		return newSurvey

	#def deleteSurvey(self,surveyID):
	#	for survey in self._surveys:
	#		if(survey.getSurveyID() == surveyID):
	#			self._surveys.remove(survey)

	def generatePool(self):
		#self.clearPool()
		writer = SQLWriter()
		query = "SELECT * FROM Surveys"
		courseList = writer.dbselect(query, self._dbName) #This is stored in the database as a series of strings
		for item in courseList:
			string = ''.join(item[0])
			newSurvey = Survey(string, item[1]) #, self.getIDCounter()
			self._surveys.append(newSurvey)
			newSurvey.generateQuestions()
			newSurvey.generateResponses()

	def getSurveyList(self):
		return self._surveys

	def clearPool(self):
		writer = SQLWriter()
		query = "DELETE FROM Surveys"
		writer.dbinsert(query, self._dbName)
		self._surveys = []

	def deleteSurvey(self, surveyname):
		for s in self._surveys:
			if s.getCourseName() == surveyname:
				writer = SQLWriter()
				query = "DELETE FROM QUESTIONS"
				writer.dbinsert(query,s.getDBName())
				query = "DELETE FROM RESPONSES"
				writer.dbinsert(query,s.getDBName())
				query = "DELETE FROM USERS"
				writer.dbinsert(query,s.getDBName())
				self._surveys.remove(s)

class QuestionPool(object):
	def __init__(self):
		self._dbName = "InitData.db"
		self._questions = [] #list of question objects

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
		writer = SQLWriter()
		writer.dbinsertq(self._dbName, answerType, isMandatory, qString, 1)
		qid = writer.dbGetNextUniqueID(self._dbName)
		q = Question(qid, qString, answerType, isMandatory, 1)
		self._questions.append(q)

	def generatePool(self):
		#self.clearPool()
		writer = SQLWriter()
		query = "SELECT * FROM QUESTIONS"
		qList = writer.dbselect(query, self._dbName)
		for q in qList:
			newq = Question(q[0], q[3], q[1], q[2], q[4])
			self._questions.append(newq)

	def storePool(self):
		writer = SQLWriter()
		for q in self._questions:
			write.dbinsertq(self._dbName, q.getAnswerType(), q.getIsMandatory(), q.getQuestionString())

	def clearPool(self):
		#print ("CLEAR POOL JUST GOT CALLED :(")
		writer = SQLWriter()
		query = "DELETE FROM Questions"
		writer.dbinsert(query, self._dbName)
		self._questions = []

	def getQuestionList(self):
		return self._questions

	def getVisibleQuestions(self):
		qlist = []
		for q in self._questions:
			if q.isValidQuestion():
				qlist.append(q)
		return qlist

class ResponsePool(object):
	def __init__(self, dbName):
		self._dbName = dbName
		self._responses = []

	#Given a response list, add it to the database and the pool
	def addResponse(self,responseList):
		print("ResponseList is: ")
		print(responseList)
		writer = SQLWriter()
		rid = writer.dbGetNextRUniqueID(self._dbName)
		#So we go through the response object, and pad it out
		#Should work as per https://stackoverflow.com/questions/8316176/insert-list-into-my-database-using-python
		toInsert = []
		for i in range(0,20):
			if i < len(responseList):
				toInsert.append(responseList[i])
			else:
				toInsert.append("")
		print(toInsert)
		query = "INSERT INTO RESPONSES (q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (toInsert[0],toInsert[1],toInsert[2],toInsert[3],toInsert[4],toInsert[5],toInsert[6],toInsert[7],toInsert[8],toInsert[9],toInsert[10],toInsert[11],toInsert[12],toInsert[13],toInsert[14],toInsert[15],toInsert[16],toInsert[17],toInsert[18],toInsert[19])
		writer.dbinsert(query, self._dbName)
		newResponse = Response(responseList,rid)

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
		#self.clearPool()
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
	def __init__(self, coursename, state): #uniqueID
		self._coursename = coursename
		self._dbName = str(coursename + ".db")
		writer = SQLWriter()
		writer.createSurveyDB(self._dbName)
		#self._uniqueID = uniqueID
		self._questionList = [] #The question pool is merely a list of unique numbers
		self._responsePool = ResponsePool(self._dbName)#TBD
		self._stage = state #stage0 = after creation, to be approved, 1 = live, 2 = closed.

	def getCourseName(self):
		return self._coursename

	#Given a question, add the question ID to the pool
	def addQuestion(self, q):
		self._questionList.append(q.getQuestionID())
		writer = SQLWriter()
		query = "INSERT INTO Questions (QIDS) VALUES (%s)" % (str(q.getQuestionID()))
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
		return self._responsePool.getResponseList()

	def setStage(self, stage):
		self._stage = stage
		#Also update the database
		writer = SQLWriter()
		query = "UPDATE SURVEYS SET STATE = %s WHERE SNAME = '%s';" % (stage, self.getCourseName())
		print("Query is: "+query)
		writer.dbinsert(query, "InitData.db")

	def getStage(self):
		return self._stage

	def generateQuestions(self):
		writer = SQLWriter()
		query = "SELECT * FROM QUESTIONS"
		qidList = writer.dbselect(query, self._dbName)
		for qid in qidList:
			self._questionList.append(qid[0])

	def generateResponses(self):
		self._responsePool.generatePool()

	def resetSurvey(self):
		writer = SQLWriter()
		query = "DELETE FROM Questions"
		writer.dbinsert(query, self._dbName)
		self._questionList = []
		self._responsePool.clearPool()

	def getDBName(self):
	    return self._dbName

	def addUser(self, uid):
		writer = SQLWriter()
		query = "INSERT INTO USERS VALUES ('%s')" % uid
		writer.dbinsert(query, self._dbName)

	def hasUser(self, uid):
		writer = SQLWriter()
		query = "SELECT * FROM USERS WHERE UID = '%s';" % uid
		isThere = writer.dbselect(query, self._dbName)
		if(isThere):
			return True
		return False

class Question(object):
	def __init__(self, questionID, qString, answerType, isMandatory, isVisible):
		self._questionID = questionID
		self._question = qString
		self._answerType = answerType
		self._isMandatory = isMandatory
		self._isVisible = isVisible

	def getQuestionID(self):
		return self._questionID

	def getQuestionString(self):
		return self._question

	def getAnswerType(self):
		return self._answerType

	def getIsMandatory(self):
		return self._isMandatory

	def disableQuestion(self):
		self._isVisible = 0
		writer = SQLWriter()
		query = "UPDATE QUESTIONS SET VISIBILITY = 0 WHERE QID = %d;" % self.getQuestionID()
		writer.dbinsert(query, "InitData.db")

	def isValidQuestion(self):
		return self._isVisible

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

	def dbinserts(self, dbName, surveyname, state):
		connection = sqlite3.connect(dbName)
		cursorObj = connection.cursor()
		cursorObj.execute("INSERT OR REPLACE INTO Surveys (SNAME, STATE) VALUES (?,?)", (surveyname,state))
		connection.commit()
		cursorObj.close()

	def dbinsertq(self, dbName, mc, man, qstr, vis):
		connection = sqlite3.connect(dbName)
		cursorObj = connection.cursor()
		cursorObj.execute("INSERT INTO Questions (ISMCFLAG, ISMANFLAG, QSTRING, VISIBILITY) VALUES(?, ?, ?,?)", (mc, man, qstr,vis))
		connection.commit()
		cursorObj.close()

	def dbGetRows(self, query, dbName):
		connection = sqlite3.connect(dbName)
		cursorObj = connection.cursor()
		retVal = cursorObj.execute(query)
		connection.commit()
		cursorObj.close()
		return retVal

	def dbGetNextUniqueID(self, dbName):
		connection = sqlite3.connect(dbName)
		cursorObj = connection.cursor()
		temp = cursorObj.execute("SELECT max(QID) FROM QUESTIONS")
		retVal = cursorObj.fetchone()[0]
		retVal +=1
		connection.commit()

		cursorObj.close()
		return retVal

	def dbGetNextRUniqueID(self, dbName):
		connection = sqlite3.connect(dbName)
		cursorObj = connection.cursor()
		temp = cursorObj.execute("SELECT max(RID) FROM RESPONSES")
		retVal = cursorObj.fetchone()[0]
		if not retVal:
			retVal = 0
		else:
			retVal +=1
		connection.commit()

		cursorObj.close()
		return retVal

	def createSurveyDB(self, dbName):
		connection = sqlite3.connect(dbName);
		cursorObj = connection.cursor();
		cursorObj.execute('''CREATE TABLE IF NOT EXISTS QUESTIONS
				(QIDS INT)
		''')
		cursorObj.execute(''' CREATE TABLE IF NOT EXISTS RESPONSES
				(RID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
				Q1 TEXT,
				Q2 TEXT,
				Q3 TEXT,
				Q4 TEXT,
				Q5 TEXT,
				Q6 TEXT,
				Q7 TEXT,
				Q8 TEXT,
				Q9 TEXT,
				Q10 TEXT,
				Q11 TEXT,
				Q12 TEXT,
				Q13 TEXT,
				Q14 TEXT,
				Q15 TEXT,
				Q16 TEXT,
				Q17 TEXT,
				Q18 TEXT,
				Q19 TEXT,
				Q20 TEXT)
		''')
		cursorObj.execute(''' CREATE TABLE IF NOT EXISTS USERS (UID TEXT)''')
		connection.commit();
		cursorObj.close();
