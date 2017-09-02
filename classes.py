#from routes import *

#I don't think we need this object. We can skip directly to the Course object
class Semester(object):
	def __init__(self, semname = ""):
		self.__semname = semname
		#self.addToList()
	
	#setters
	def set_semname(self, name_new):
		#assert(name!=NULL);
		self.__semname = name_new
	
	#getters
	def get_semname(self):
		return self.__semname



class Course(Semester):
	def __init__(self, semestername, coursename):
		self.set_semname(semestername)
		self.__coursename = coursename
		self.questions = []
	
	#setters
	def set_coursename(self, new_name):
		self.__coursename = new_name

	#getters
	def get_coursename(self):
		return self.__coursename
	
	#returns the list of questions for an instance of object
	def get_questions(self):
		return self.questions
		
	
	#saves questions to the instance of object
	def save_questions(self, chosen_questions):
		self.questions = chosen_questions
		
	
	
class Answers(Course):
	no_of_q = 0
	
	#call funtion like this --> answer = Answer("student1"), where answer is the list of response.
	def __init__(self, name):
		self.answers = []
		self.__responsename = name
		no_of_q +=1
		
	#setters
	def set_responsename(self, new_name):
		self.__responsename = new_name
	
	def add_to_answers(line):
		self.answer.append(line)
		
	#getters
	def get_responsename(self):
		return self.__responsename
		
	def get_answers(self):
		return self.answers
		
	# call function like this --> readAnswers("answers.csv")
	def readAnswers(filename):
		with open(filename,'r') as csv_in:
			for row in csv.reader(csv_in):
				add_to_answers(row)


#instantiate object for each semester using a list of objects
#semesters = [Semester(sem) for sem in get_sems()]

#print all sem objects
#for sem in semesters:
#	print (sem.get_semname())
#sem = Semester('a')
#isinstance(), issubclass()
