class User():
	def __init__(self, newID, permLevel):
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
	def __init__(self):

class QuestionPool(Object):
	def __init__(self):

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