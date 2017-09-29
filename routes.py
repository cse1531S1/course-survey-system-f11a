from flask import Flask, redirect, render_template, request, url_for
from server import app, question_list, surveyList
from classes import Authentication, User
import csv

allQuestions = QuestionPool()

#LOGIN PAGE
@app.route('/login', methods=["GET","POST"])
def login():
	#create database of all users
	buildUserBase() 
	error = None
	if request.method == 'POST':
		#check for user against database
		if IsValidUser(request.form['zID'], request.form['password']) == False:
			error = 'Invalid Credentials. Please try again.'
		else:
			#determine type of user
			currentuser = LoginUser(request.form['zID'])
			if currentuser.getPermission() == 0:
				return redirect(url_for('admindashboard'))
				
			elif currentuser.getPermission() == 1:
				return redirect(url_for('staffdashboard'))
				
			else return redirect(url_for('studentdashboard'))
			
	return render_template('login.html', error=error)


#ADMIN DASHBOARD
@app.route('/admin/dashboard')
def admindashboard():
	#need live survey forms, survey to be reviewed, questions in the system
	qlist = allQuestions.getQuestionList()
	return render_template('adminDashboard.html', qlist = qlist)

#STAFF DASHBOARD
@app.route('/staff/dashboard')
def staffdashboard():
	return render_template('staffDashboard.html')

#ADMIN DASHBOARD
@app.route('/student/dashboard')
def studentdashboard():
	return render_template('studentDashboard.html')


#NEW QUESTIONS PAGE
@app.route('/admin/addQuestion',methods=["GET","POST"])
def addquestions():
	 #need to consider if mandatory or optional
	
	 #pass option to backend (qtype = mandatory or optional)
    submitted = None;
    if request.method == 'POST':
        question = request.form['q']
        qtype = request.form['questionType']
        etype = request.form['entryType']
        if(question == ""):
            submitted = "Please enter your question into the box!"
        else:
        	if qtype == 'mandatory':
        		qtype = 1
        	else:
        		qtype = 0

        	#entryType is passed in as a string --> check with implementation
            allQuestions.addQuestion(question, etype, qtype)
            storePool()											#check if needed

            return redirect((url_for('addedQuestions'))
    return render_template('addQuestion.html', status = submitted)
    
#ADDED QUESTIONS PAGE
@app.route('/admin/addedQuestions')
def addQuestion:
    return render_template('adminSurveySubmitted.html')
    

#QUESTION LIST PAGE
@app.route('/admin/allQuestions')
def questionlist():
    qlist = allQuestions.getQuestionList()
    optionalq = []
    mandatoryq = []
    for q in qlist:
    	if q.getIsMandatory():
    		mandatoryq.append(q)
    	else:
    		optionalq.append(q)

    #need to ask about delete question interface

    return render_template('addedQuestions.html', optionalq = optionalq, mandatoryq = mandatoryq)


#NEW SURVEY PAGE goes to /addSurvey
@app.route('/admin/chooseSession') 
def newsurvey():
	courses_list = get_list_of_courses()
	semesters = get_sems()

	#pass though dictionary of courses with semester as keys and sem list as key list
	return render_template('chooseSession.html', courses = courses_list, semesters = semesters)

#SELECT QUESTIONS PAGE
  
#need to change this to /admin/chooseQuestions depending on implementation

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
@app.route('/admin/surveySubmitted', methods=['GET','POST'])
def questionselected():
	if request.method == "POST":
		name = request.form["bt"]
		if name == "createanother":
			return redirect(url_for("newsurvey"))
		
		else if name == "return":
			return redirect(url_for("admindashboard"))
			
	else:
		return render_template('surveySubmitted.html')   
    
#List of surveys page
@app.route('/staff/reviewSurvey')
def reviewSurvey():
	# This function gives the webpage a list of surveys via he SurveyPool object
   return render_template('reviewSurvey.html', SurveyList = surveyList.getSurveyList())
   

#REVIEW FINISHED
@app.route('/staff/finishedReview')
def finishedReview():
	return render_template('finishedReview.html')


	
# SURVEY PAGE

# fix up url based on implementation

@app.route ('/student/survey/<semestername>/<coursename>', methods=["GET", "POST"])
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

#SURVEY COMPLETED	
@app.route ('/student/surveySubmitted')
def completed():
	return render_template('surveySubmitted.html')
	
	
#VIEW METRICS
@app.route('/admin/metricsSelection')
def metrics():
	return render_template('adminMetricsSelection.html')
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
