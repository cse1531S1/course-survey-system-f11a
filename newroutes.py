from flask import Flask, redirect, render_template, request, url_for
from newserver import app, reader
# from classes import Survey, Question, Authentication, User
from newdb import Controller
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import csv

#LOGIN PAGE
global currentuser

@app.route('/', methods=["GET","POST"])
def login():
	error = None
	if request.method == 'POST':
		#check for user against database
		global currentuser
		currentuser = reader.isValidUser(request.form['zID'], request.form['password'])

		if currentuser == None:
			error = 'Invalid Credentials. Please try again.'
		else:
			if currentuser.permission == 0:
				return redirect(url_for('admindashboard'))
				
			elif currentuser.permission == 1:
				return redirect(url_for('staffdashboard'))
				
			else:
				return redirect(url_for('studentdashboard'))
			
	return render_template('login.html', error=error)


#ADMIN DASHBOARD
@app.route('/admin/dashboard')
def admindashboard():
	#need live survey forms, survey to be reviewed, questions in the system
	# slist = allSurveys.getSurveyList()
	questionlist = reader.getAllQuestions()
	tobereviewed = reader.getReviewSurveys()
	slive = reader.getLiveSurveys()
	sclosed = reader.getClosedSurveys()
	
	metricsViewable = True

	return render_template('adminDashboard.html', qlist = questionlist, sreviewed = tobereviewed, slive = slive, sclosed = sclosed, metricsViewable = metricsViewable)


#NEW QUESTIONS PAGE
@app.route('/admin/addQuestion',methods=["GET","POST"])
def addquestions():
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
            reader.addNewQuestion(question, entrytype, questiontype)

        return redirect(url_for('addedquestions'))
    return render_template('addQuestion.html', status = submitted)
    
#ADDED QUESTIONS PAGE
@app.route('/admin/addedQuestions')
def addedquestions():
    return render_template('addedQuestion.html')
    

#QUESTION LIST PAGE
@app.route('/admin/allQuestions',methods=["GET","POST"])
def questionlist():
    # qlist = allQuestions.getVisibleQuestions()
    mandatoryq = []
    optionalq = []
    if request.method == 'POST':
    	reader.removeQuestion(request.form["submit"])
    	
    mandatoryq = reader.getMandatoryQuestions()
    optionalq = reader.getOptionalQuestions()

    return render_template('allQuestions.html', optionalq = optionalq, mandatoryq = mandatoryq)


#NEW SURVEY PAGE
@app.route('/admin/chooseSession') 
def newsurvey():
	courses_list = reader.getCoursesList()
	semesters = reader.getSemesters()

	#pass though dictionary of courses with semester as keys and sem list as key list
	return render_template('chooseSession.html', courses = courses_list, semesters = semesters)
	
#VIEW ACTIVE SURVEYS
@app.route('/admin/viewSurveysList',methods=["GET","POST"]) 
def viewActiveSurveys():
    #select surveys to close
    if request.method == 'POST':
    	thisSurvey = reader.getSurvey(request.form["submit"])
    	reader.setStage(thisSurvey, 2)
    	metricsViewable = True

    slive = reader.getLiveSurveys()

    return render_template('viewSurveyList.html', surveyList = slive)

#SELECT QUESTIONS PAGE
@app.route('/admin/chooseQuestions/<coursename>/<semestername>',methods=["GET","POST"])
def courseObject(coursename, semestername):
	#If they've submitted, then for each of these, instantiate a questions object, and a data object
	if request.method == "POST":
		surveyname = coursename+semestername
		if reader.getSurvey(surveyname):
			reader.deleteSurvey(surveyname)
		
		# Implement afterwards - if creating an existing survey
		# if allSurveys.getSurveyByName(surveyname):
		#     allSurveys.deleteSurvey(surveyname)
			
		thisSurvey = reader.addNewSurvey(surveyname)
		print('survey added')
		for v in request.form:
			thisQuestion = reader.getQuestion(v)
			if thisQuestion != None:
				print(thisSurvey)
				print(thisQuestion)
				reader.addQuestion(thisSurvey, thisQuestion)

		return redirect(url_for('questionselected'))
	
	#Else, get questionlist from pool, and display these onto the screen as checkboxes
	else:
		mandatoryQ = reader.getMandatoryQuestions()	
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




    
#STAFF DASHBOARD
@app.route('/staff/dashboard')
def staffdashboard():
	global currentuser
	tobereviewed = reader.getMyReviewSurveys(currentuser)
	# reviewed = reader.getMyReviewedSurveys()
	sclosed = reader.getMyClosedSurveys(currentuser)

	return render_template('staffDashboard.html', sreviewed = tobereviewed, sclosed = sclosed)

#choose optional questions
@app.route('/staff/reviewSurvey/<surveyName>', methods=["GET","POST"])
def reviewSurvey(surveyName):
	#this takes in all the questions associated with survey so far (assuming these are mandatory)
	#make sure that each survey is only filled out once by any staff
	thisSurvey = reader.getSurvey(surveyName)

	questionlist = thisSurvey.questions
	optionallist = reader.getOptionalQuestions()

	if request.method == "POST":
		for v in request.form:
			thisQuestion = reader.getQuestion(v)
			if thisQuestion != None:
				reader.addQuestion(thisSurvey, thisQuestion)
		reader.setStage(thisSurvey, 1)
		return redirect(url_for('finishedReview'))
          
	return render_template('reviewSurvey.html', manqlist = questionlist, opqlist = optionallist)
        
#REVIEW FINISHED
@app.route('/staff/finishedReview')
def finishedReview():
    
    message = "Survey was sucessfully reviewed." #Make this display if the survey was sucessful or not 
    
    return render_template('staffSurveySubmitted.html', message = message)




#STUDENT DASHBOARD
@app.route('/student/dashboard')
def studentdashboard():

	# global metricsViewable
	global currentuser
	surveyclosed = reader.getMyClosedSurveys(currentuser)
	tobeanswered = reader.getMyLiveSurveys(currentuser)
	#print(tobeanswered)
	

	return render_template('studentDashboard.html', sanswered = tobeanswered, sclosed = surveyclosed)
	
# SURVEY PAGE
@app.route ('/student/survey/<surveyName>', methods=["GET", "POST"])
def survey(surveyName):

	thisSurvey = reader.getSurvey(surveyName)
	questionlist = thisSurvey.questions

	if request.method == 'POST':
		#for each question object
		count = 0
		for v in request.form:
			count+=1
			print('question',str(v))
			print('ans',request.form[v])
			
			#ISSUE: how to check if 
			thisQuestion = reader.getQuestion(v)
			global currentuser
			thisResponse = reader.addNewResponse(request.form[v], thisQuestion.qid, thisSurvey, currentuser)
			print(thisResponse.string)
			thisQuestion.responses.append(thisResponse)

		if count != len(questionlist):
			message = "ERROR: Please enter a response to all questions"
			reader.removeNullResponses(thisSurvey)
			return render_template('survey.html', questions = questionlist, surveyName = surveyName, message = message)

		
		return redirect(url_for("studentSurveySubmitted"))

	return render_template('survey.html', questions = questionlist, surveyName = surveyName)

#SURVEY COMPLETED	
@app.route ('/student/surveySubmitted')
def studentSurveySubmitted():
	return render_template('surveySubmitted.html')
	
	
#VIEW METRICS
@app.route('/metrics/<surveyName>')
def metrics(surveyName):
	# Information taken from https://plot.ly/python/bar-charts/
	plot = [] #this will be a list of graphs
	textQuestions = [] #this will hold question and responses
	thisSurvey = allSurveys.getSurveyByName(surveyName)
	questionList = getQuestionsForSurvey(thisSurvey.sid) 
	allresponses = []
	if (thisSurvey.getStage() == 3) or (thisSurvey.getStage() == 2 and currentuser.getPermission() == 0):
		for question in questionList:
			if question.getAnswerType(): #MCQ question
				data = [go.Bar(x = ['Strongly disagree', 'Disagree', 'Pass', 'Agree', 'Strognly agree'], y = [getResponsesForQinS(thisSurvey.sid, question.qid)])]
				plot.append([question.getQuestionString(), py.iplot(data, filename='basic bar')])
			else:	#Text question
				textQuestions.append([question.getQuestionString(), getResponsesForQinS(thisSurvey.sid, question.qid)])
	else:
		message = "Metrics are not available for this survey."
	return render_template('metrics.html', plots = plot, textQuestions = textQuestions, message = message)


@app.route('/student/metrics/<surveyName>')
def studentMetrics(surveyName):
	global currentuser
	resplist = reader.getMetrics(currentuser, surveyName)
	return render_template('studentmetrics.html', resplist = resplist)
# #--------------------------functions for constructing courses --------------------------------------
# #---------------------------------------------------------------------------------------------------
# def inList(list_current, to_find):
#    # Takes in a list and a item
#    # Determines if the item is in the list
#     found = False
#     for item in list_current:
#         if(item == to_find):
#             found = True
#             return found #early exit
#     return found
         
         
# def get_list_of_courses():
#     # Get a list of ordered semester and creates a dictionary so that
#     # each semester has a list of it's associated courses
#     semesters = get_sems()
#     courses = {}
#     for sem in semesters:
#         courses[sem] = get_courses(sem)
#     return courses
    

# def get_sems():
#     # This function reads from the courses csv and gets an ordered list of unique semesters
#     semesters = []
#     found = True
#     while(found): #while a unique course has not been added
#         found = False
#         with open('courses.csv','r') as csv_in: #open the csv
#             reader = csv.reader(csv_in)
#             next_min = "zzzzz"
#             for row in reader: #for each row in the csv
#                  if(row != [] and row[1] < next_min): #if the current semester is less than the minimum
#                     if(inList(semesters, row[1]) == False): #check not already in 
#                         next_min = row[1]
#                         found = True
#             if(found):
#                 semesters.append(next_min)
#     return semesters
    
# def get_courses(semester):
#     # This function takes in a semester and returns a list of its courses
#     courses = []
#     with open('courses.csv','r') as csv_in: #open the csv
#         reader = csv.reader(csv_in)
#         for row in reader: #for each row in the csv
#             if(row != [] and row[1] == semester):
#                 courses.append(row[0])
#     return courses