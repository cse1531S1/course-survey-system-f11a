from flask import Flask, redirect, render_template, request, url_for
from server import app, allQuestions, allSurveys, authenticate
from classes import Survey, Question, Authentication, User
import csv

#THIS IS A COMMENT

currentuser = User(0)
#LOGIN PAGE
@app.route('/', methods=["GET","POST"])
def login():
	error = None
	if request.method == 'POST':
		#check for user against database
		if authenticate.IsValidUser(request.form['zID'], request.form['password']) == False:
			error = 'Invalid Credentials. Please try again.'
		else:
			#determine type of user
			global currentuser 
			currentuser = authenticate.LoginUser(request.form['zID'])
			if currentuser.getPermission() == 0:
				return redirect(url_for('admindashboard'))
				
			elif currentuser.getPermission() == 1:
				return redirect(url_for('staffdashboard'))
				
			else:
				return redirect(url_for('studentdashboard'))
			
	return render_template('login.html', error=error)


#ADMIN DASHBOARD
@app.route('/admin/dashboard')
def admindashboard():
	#need live survey forms, survey to be reviewed, questions in the system
	slist = allSurveys.getSurveyList()
	tobereviewed = []
	slive = []
	questionlist = []
	
	for s in slist:
		if s.getStage() == 1:
			tobereviewed.append(s)
		if s.getStage() == 2:
			slive.append(s)

	qlist = allQuestions.getQuestionList()
	
	for q in qlist:
		questionlist.append(q)

	return render_template('adminDashboard.html', qlist = questionlist, sreviewed = tobereviewed, slive = slive)

#STAFF DASHBOARD
@app.route('/staff/dashboard')
def staffdashboard():
	usersurveys = currentuser.getNotCompleted()#list of courses assigned to staff
	tobereviewed = []
	for survey in usersurveys:
		surveyobj = allSurveys.getSurveyByName(survey)

		#if survey object exists for that course and it is in review phase
		if surveyobj:
			if surveyobj.getStage() == 1:
				tobereviewed.append(surveyobj)

	return render_template('staffDashboard.html', sreviewed = tobereviewed)

#STUDENT DASHBOARD
@app.route('/student/dashboard')
def studentdashboard():
	usersurveys = currentuser.getNotCompleted()#list of courses assigned to student
	tobeanswered = []
	for survey in usersurveys:
		surveyobj = allSurveys.getSurveyByName(survey)

		#if survey object exists for that course and it is in review phase
		if surveyobj:
			if surveyobj.getStage() == 2:
				tobeanswered.append(surveyobj)

	return render_template('studentDashboard.html', sanswered = tobeanswered)


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
            return render_template('addQuestion.html', status = submitted)
        else:
            #default values: mandatory, MCQ
            questiontype = 1
            entrytype = 1
            if qtype == "optional":
            	questiontype = 0
            if etype == "text":
            	entrytype = 0

            allQuestions.addQuestion(question, entrytype, questiontype)

        return redirect(url_for('addedquestions'))
    return render_template('addQuestion.html', status = submitted)
    
#ADDED QUESTIONS PAGE
@app.route('/admin/addedQuestions')
def addedquestions():
    return render_template('addedQuestion.html')
    

#QUESTION LIST PAGE
@app.route('/admin/allQuestions')
def questionlist():
    qlist = allQuestions.getQuestionList()
    
    mandatoryq = []
    optionalq = []
    
    for q in qlist:
    	if q.getIsMandatory():
    		mandatoryq.append(q)
    	else:
    		optionalq.append(q)

    #need to ask about delete question interface

    return render_template('allQuestions.html', optionalq = optionalq, mandatoryq = mandatoryq)


#NEW SURVEY PAGE
@app.route('/admin/chooseSession') 
def newsurvey():
	courses_list = get_list_of_courses()
	semesters = get_sems()

	#pass though dictionary of courses with semester as keys and sem list as key list
	return render_template('chooseSession.html', courses = courses_list, semesters = semesters)

#SELECT QUESTIONS PAGE
  
#need to change this to /admin/chooseQuestions depending on implementation. Look into HTML FORMS 
#in tutorial: localhost/adminSurveyForm?choice=COMP2041+17s2

@app.route('/admin/chooseQuestions/<semestername>/<coursename>',methods=["GET","POST"])
def courseObject(semestername, coursename):
	#If they've submitted, then for each of these, instantiate a questions object, and a data object
	questions = []
	if request.method == "POST":
		surveyname = coursename+semestername
		print(surveyname)
		thisSurvey = allSurveys.addSurvey(surveyname)
		thisSurvey.setStage(1)
		for q in questions:
			if request.form[q] != NULL:
				thisSurvey.addQuestion(q)


		return redirect(url_for('questionselected'))
	
	#Else, get questionlist from pool, and display these onto the screen as checkboxes
	else:
		qlist = allQuestions.getQuestionList()
		
		mandatoryQ = []
		TEXTquestions = []
		for q in qlist:
			if q.getIsMandatory():
			        mandatoryQ.append(q)
		return render_template('choosequestions.html', questions = mandatoryQ)


#PAGE AFTER SELECTING QUESTIONS
@app.route('/admin/surveySubmitted', methods=['GET','POST'])
def questionselected():
	if request.method == "POST":
		name = request.form["bt"]
		if name == "createanother":
			return redirect(url_for("newsurvey"))
		
		elif name == "return":
			return redirect(url_for("admindashboard"))
			
	else:
		return render_template('adminSurveySubmitted.html')   
    
#choose optional questions
@app.route('/staff/reviewSurvey/<surveyName>')
def reviewSurvey(surveyName):
	thisSurvey = allSurveys.getSurveyByName(surveyName)#get survey object
	allqinsurvey = thisSurvey.getQuestions() #list of questionids
	allq = allQuestions.getQuestionList()#allq has all quesions from pool
	questionlist = []
	optionallist = []

	#find out all mandatory questions for this survey
	for manq in allqinsurvey:
		questionlist.append(allQuestions.getQuestion(manq))

	#pick all optional questions
	for opq in allq:
		if opq.getIsMandatory() == 0:
			optionallist.append(opq)
	print("manlist", questionlist)
	print("optionallist", optionallist)
	if request.method == 'POST':
		for q in opqlist:
			if request.form[q] != NULL:
				thisSurvey.addQuestion(q)
		
		thisSurvey.setStage(1)
		currentuser.nowCompleted(surveyName)

		return redirect(url_for('finishedReview'))
	return render_template('reviewSurvey.html', manqlist = questionlist, opqlist = optionallist)
   

#REVIEW FINISHED
@app.route('/staff/finishedReview')
def finishedReview():
	return render_template('finishedReview.html')


	
# SURVEY PAGE

# fix up url based on implementation

@app.route ('/student/survey/<surveyName>', methods=["GET", "POST"])
def survey(surveyName):
	thisSurvey = allSurveys.getSurveyByName(surveyName)
	allqinsurvey = thisSurvey.getQuestions() #list of questionids
	questionlist = []
	resplist = [] #list of all responses

	#find out all questions for this survey
	for q in allqinsurvey:
		questionlist.append(allQuestions.getQuestion(q))


	if request.method == 'POST':
		#for each qid
		for question in thisSurvey.getQuestions():
			if request.form.get(question.getQuestionString(question)):
				resplist.append(request.form.get(question.getQuestionName()))
		
		thisSurvey.responsePool.addResponse(resplist)
		currentuser.nowCompleted(surveyName)
		return redirect(url_for("studentSurveySubmitted"))

	return render_template('survey.html', qlist = questionlist)

#SURVEY COMPLETED	
@app.route ('/student/surveySubmitted')
def studentSurveySubmitted():
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
