from flask import Flask, redirect, render_template, request, url_for
from server import app, question_list, surveyList
from classes import Survey, Question, Data
import csv

#LOGIN PAGE
@app.route('/', methods=["GET","POST"])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			return redirect(url_for('dashboard'))
	return render_template('login.html', error=error)


#ADMIN DASHBOARD
@app.route('/Dashboard')
def dashboard():
	return render_template('dashboard.html')

#NEW QUESTIONS PAGE
@app.route('/NewQuestions',methods=["GET","POST"])
def newquestions():
    submitted = None;
    if request.method == 'POST':
        question = request.form['q']
        if(question == ""):
            submitted = "Please enter your question into the box!"
        else:
            with open('questionList.csv','a') as csv_out:
                writer = csv.writer(csv_out)
                writer.writerow([question]) 
            submitted = "Question submitted!"
    return render_template('newquestions.html', status = submitted)

#QUESTION LIST PAGE
@app.route('/QuestionList')
def questionlist():
    with open('questionList.csv','r') as csv_in:
        reader = csv.reader(csv_in)
        questions_list = list(reader)
        stringVersion = "<br/>".join(item[0] for item in questions_list)
    return render_template('questions.html', questions = stringVersion)


#NEW SURVEY PAGE goes to /addSurvey
@app.route('/courseSelection') 
def newsurvey():
	courses_list = get_list_of_courses()
	semesters = get_sems()

	#pass though dictionary of courses with semester as keys and sem list as key list
	return render_template('courseselection.html', courses = courses_list, semesters = semesters)

#SELECT QUESTIONS PAGE  
@app.route('/addSurvey/<semestername>/<coursename>',methods=["GET","POST"])
def courseObject(semestername, coursename):
	#If they've submitted, then for each of these, instantiate a questions object, and a data object
	if request.method == "POST":
		emptyList = []
		global question_list
		#Retrieve the relevant survey; otherwise, create a new one
		thisSurvey = surveyList.getSurvey(semestername, coursename)
		if thisSurvey == None:
			thisSurvey = Survey(coursename, semestername)
			surveyList.addSurvey(thisSurvey)
			surveyList.saveSurvey(thisSurvey)
		else:
			surveyList.deleteSurvey(semestername, coursename)
			thisSurvey.resetSurvey()
			thisSurvey = Survey(coursename, semestername)
			surveyList.addSurvey(thisSurvey)
			surveyList.saveSurvey(thisSurvey)

		#Create and appennd Question and Data objects
		for q in question_list:
			if request.form.get(q):
				newQObj = Question(str(q))
				thisSurvey.addQuestion(newQObj)

		thisSurvey.storeSurvey()
		return redirect(url_for('questionselected', semesterName = semestername, courseName = coursename))
	
	#Else, read from the question list into the CSV, and display these onto the screen as checkboxes
	elif request.method == "GET":
		question_list = []
		with open('questionList.csv','r') as csv_in:
			for row in csv.reader(csv_in):
				question_list.append(row[0])
		return render_template('choosequestions.html', questions = question_list)


#PAGE AFTER SELECTING QUESTIONS
@app.route('/questionselected', methods=['GET','POST'])
def questionselected():
	if request.method == "POST":
		name = request.form["bt"]
		if name == "createanother":
			return redirect(url_for("newsurvey"))
	else:
		semesterName = request.args['semesterName']
		courseName = request.args['courseName']
		return render_template('questionselected.html', sem = semesterName, course = courseName)   
    
#List of surveys page
@app.route('/viewSurveysList')
def viewSurveysList():
	# This function gives the webpage a list of surveys via he SurveyPool object
	return render_template('viewSurveyList.html', SurveyList = surveyList.getSurveyList())

	
# SURVEY PAGE
@app.route ('/survey/<semestername>/<coursename>', methods=["GET", "POST"])
def survey(semestername, coursename):

	rightSurvey = surveyList.getSurvey(semestername, coursename)
	if request.method == 'POST':
		answerList = []
		for question in rightSurvey.getQuestions():
			#print("What we're trying to get is: ")
			#print(question.getQuestionName())
			#print(request.form.get(question.getQuestionName()))
			#For some reason, request.form.get(question) is empty
			if request.form.get(question.getQuestionName()):
				answerList.append(request.form.get(question.getQuestionName()))
		newDataObj = Data(answerList)
		rightSurvey.addResponse(newDataObj)
		rightSurvey.storeResponse(newDataObj)
		return redirect(url_for("completed"))
	else:
		listRecieved = rightSurvey.getQuestions()
		listToSend = []
		for item in listRecieved:
			listToSend.append(item.getQuestionName())
		return render_template('survey.html', sem = semestername, course = coursename, questions = listToSend)
	
@app.route ('/completed', methods = ["GET","POST"])
def completed():
	return render_template('success.html')
#--------------------------functions for constructing courses --------------------------------------
#---------------------------------------------------------------------------------------------------
def inList(list_current, to_find):
   # Takes in a list and a item
   # Determines if the item is in the list
    found = False
    for item in list_current:
        if(item == to_find):
            found = True
            return found #early exit
    return found
         
         
def get_list_of_courses():
    # Get a list of ordered semester and creates a dictionary so that
    # each semester has a list of it's associated courses
    semesters = get_sems()
    courses = {}
    for sem in semesters:
        courses[sem] = get_courses(sem)
    return courses
    

def get_sems():
    # This function reads from the courses csv and gets an ordered list of unique semesters
    semesters = []
    found = True
    while(found): #while a unique course has not been added
        found = False
        with open('courses.csv','r') as csv_in: #open the csv
            reader = csv.reader(csv_in)
            next_min = "zzzzz"
            for row in reader: #for each row in the csv
                 if(row != [] and row[1] < next_min): #if the current semester is less than the minimum
                    if(inList(semesters, row[1]) == False): #check not already in 
                        next_min = row[1]
                        found = True
            if(found):
                semesters.append(next_min)
    return semesters
    
def get_courses(semester):
    # This function takes in a semester and returns a list of its courses
    courses = []
    with open('courses.csv','r') as csv_in: #open the csv
        reader = csv.reader(csv_in)
        for row in reader: #for each row in the csv
            if(row != [] and row[1] == semester):
                courses.append(row[0])
    return courses
