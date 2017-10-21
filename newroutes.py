from flask import Flask, redirect, render_template, request, url_for
from newserver import app, Survey, Question, Response, User, Course
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

#LOGIN PAGE
global currentuser
global auth


@app.route('/', methods=["GET","POST"])
def login():
	error = None
	global auth
	auth = -1
	if request.method == 'POST':
		#check for user against database
		global currentuser
		currentuser = User.isValidUser(request.form['zID'], request.form['password'])

		if currentuser == None:
			error = 'Invalid Credentials. Please try again.'
		else:
			if currentuser.permission == 0:
				auth = 0
				return redirect(url_for('admindashboard'))
				
			elif currentuser.permission == 1:
				auth = 1
				return redirect(url_for('staffdashboard'))
				
			else:
				auth = 2
				return redirect(url_for('studentdashboard'))
			
	return render_template('login.html', error=error)


#ADMIN DASHBOARD
@app.route('/admin/dashboard')
def admindashboard():
	global auth
	if auth != 0:
		error = "Invalid Permissions. Please log in and try again."
		return render_template('login.html', error = error)
	else:

		questionlist = Question.getAllQuestions()
		tobereviewed = Survey.getReviewSurveys()
		slive = Survey.getLiveSurveys()
		sclosed = Survey.getClosedSurveys()
		
		metricsViewable = True

		return render_template('adminDashboard.html', qlist = questionlist, sreviewed = tobereviewed, slive = slive, sclosed = sclosed, metricsViewable = metricsViewable)


#NEW QUESTIONS PAGE
@app.route('/admin/addQuestion',methods=["GET","POST"])
def addquestions():
	 #pass option to backend (qtype = mandatory or optional)
	global auth
	if auth != 0:
		error = "Invalid Permissions. Please log in and try again."
		return render_template('login.html', error = error)
	else:
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
	            Question.addNewQuestion(question, entrytype, questiontype)

	        return redirect(url_for('addedquestions'))
	    return render_template('addQuestion.html', status = submitted)
    
#ADDED QUESTIONS PAGE
@app.route('/admin/addedQuestions')
def addedquestions():
	global auth
	if auth != 0:
		error = "Invalid Permissions. Please log in and try again."
		return render_template('login.html', error = error)
	else:
	    return render_template('addedQuestion.html')
    

#QUESTION LIST PAGE
@app.route('/admin/allQuestions',methods=["GET","POST"])
def questionlist():
    # qlist = allQuestions.getVisibleQuestions()
	global auth
	if auth != 0:
		error = "Invalid Permissions. Please log in and try again."
		return render_template('login.html', error = error)
	else:
		mandatoryq = []
		optionalq = []
		if request.method == 'POST':
			Question.removeQuestion(request.form["submit"])
	    	
		mandatoryq = Question.getMandatoryQuestions()
		optionalq = Question.getOptionalQuestions()

		return render_template('allQuestions.html', optionalq = optionalq, mandatoryq = mandatoryq)


#NEW SURVEY PAGE
@app.route('/admin/chooseSession') 
def newsurvey():
	global auth
	if auth != 0:
		error = "Invalid Permissions. Please log in and try again."
		return render_template('login.html', error = error)
	else:	
		courses_list = Course.getCoursesList()
		semesters = Course.getSemesters()

		#pass though dictionary of courses with semester as keys and sem list as key list
		return render_template('chooseSession.html', courses = courses_list, semesters = semesters)
	
#VIEW ACTIVE SURVEYS
@app.route('/admin/viewSurveysList',methods=["GET","POST"]) 
def viewActiveSurveys():
	global auth
	if auth != 0:
		error = "Invalid Permissions. Please log in and try again."
		return render_template('login.html', error = error)
	else:
	    #select surveys to close
	    if request.method == 'POST':
	    	thisSurvey = Survey.getSurvey(request.form["submit"])
	    	Survey.setStage(thisSurvey, 2)
	    	metricsViewable = True

	    slive = Survey.getLiveSurveys()

	    return render_template('viewSurveyList.html', surveyList = slive)

#SELECT QUESTIONS PAGE
@app.route('/admin/chooseQuestions/<coursename>/<semestername>',methods=["GET","POST"])
def courseObject(coursename, semestername):
	#If they've submitted, then for each of these, instantiate a questions object, and a data object
	global auth
	if auth != 0:
		error = "Invalid Permissions. Please log in and try again."
		return render_template('login.html', error = error)
	else:
		if request.method == "POST":
			surveyname = coursename+semestername
			if Survey.getSurvey(surveyname):
				Survey.deleteSurvey(surveyname)
				
			thisSurvey = Survey.addNewSurvey(surveyname)
			for v in request.form:
				thisQuestion = Question.getQuestion(v)
				if thisQuestion != None:
					Survey.addQuestion(thisSurvey, thisQuestion)

			return redirect(url_for('questionselected'))
		
		#Else, get questionlist from pool, and display these onto the screen as checkboxes
		else:
			mandatoryQ = Question.getMandatoryQuestions()	
			return render_template('choosequestions.html', questions = mandatoryQ)


#PAGE AFTER SELECTING QUESTIONS
@app.route('/admin/surveySubmitted', methods=['GET','POST'])
def questionselected():
	global auth
	if auth != 0:
		error = "Invalid Permissions. Please log in and try again."
		return render_template('login.html', error = error)
	else:
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
	global auth
	if auth != 1:
		error = "Invalid Permissions. Please log in and try again."
		return render_template('login.html', error = error)
	else:
		global currentuser
		tobereviewed = Survey.getMyReviewSurveys(currentuser)
		# reviewed = reader.getMyReviewedSurveys()
		sclosed = Survey.getMyClosedSurveys(currentuser)

		return render_template('staffDashboard.html', sreviewed = tobereviewed, sclosed = sclosed)

#choose optional questions
@app.route('/staff/reviewSurvey/<surveyName>', methods=["GET","POST"])
def reviewSurvey(surveyName):
	global auth
	if auth != 1:
		error = "Invalid Permissions. Please log in and try again."
		return render_template('login.html', error = error)
	else:
		#this takes in all the questions associated with survey so far (assuming these are mandatory)
		#make sure that each survey is only filled out once by any staff
		thisSurvey = Survey.getSurvey(surveyName)

		questionlist = thisSurvey.questions
		optionallist = Question.getOptionalQuestions()

		if request.method == "POST":
			for v in request.form:
				thisQuestion = Question.getQuestion(v)
				if thisQuestion != None:
					Survey.addQuestion(thisSurvey, thisQuestion)
			Survey.setStage(thisSurvey, 1)
			return redirect(url_for('finishedReview'))
	          
		return render_template('reviewSurvey.html', manqlist = questionlist, opqlist = optionallist)
        
#REVIEW FINISHED
@app.route('/staff/finishedReview')
def finishedReview():
	global auth
	if auth != 1:
		error = "Invalid Permissions. Please log in and try again."
		return render_template('login.html', error = error)
	else:
		message = "Survey was sucessfully reviewed." #Make this display if the survey was sucessful or not 
		return render_template('staffSurveySubmitted.html', message = message)




#STUDENT DASHBOARD
@app.route('/student/dashboard')
def studentdashboard():
	global auth
	if auth != 2:
		error = "Invalid Permissions. Please log in and try again."
		return render_template('login.html', error = error)
	else:
		# global metricsViewable
		global currentuser
		surveyclosed = Survey.getMyClosedSurveys(currentuser)
		tobeanswered = Survey.getMyLiveSurveys(currentuser)
		#print(tobeanswered)
		return render_template('studentDashboard.html', sanswered = tobeanswered, sclosed = surveyclosed)
	
# SURVEY PAGE
@app.route ('/student/survey/<surveyName>', methods=["GET", "POST"])
def survey(surveyName):
	global auth
	if auth != 2:
		error = "Invalid Permissions. Please log in and try again."
		return render_template('login.html', error = error)
	else:
		thisSurvey = Survey.getSurvey(surveyName)
		questionlist = Survey.getQuestionsInSurvey(thisSurvey)
		print('allQuestions in survey page', questionlist)
		manquestions = Survey.getMandatorySurveyQuestions(thisSurvey)

		if request.method == 'POST':
			#for each question object
			for v in request.form:
				print('question',str(v))
				print('ans',request.form[v])
				
				thisQuestion = Question.getQuestion(str(v))
				if request.form[v] != "":
					if thisQuestion in manquestions:
						manquestions.remove(thisQuestion)

				global currentuser
				thisResponse = Response.addNewResponse(str(request.form[v]), thisQuestion.qid, thisSurvey, currentuser)
				print(thisResponse.string)
				Question.addResponseToQuestion(thisQuestion, thisResponse)
				

			print(len(manquestions))
			if len(manquestions):
				message = "ERROR: Please enter a response to all mandatory questions"
				Response.removeResponsesToSurvey(thisSurvey)
				manquestions = Survey.getMandatorySurveyQuestions(thisSurvey)
				print("reloaded manquestions", manquestions)
				questionlist = Survey.getQuestionsInSurvey(thisSurvey)
				return render_template('survey.html', questions = questionlist, surveyName = surveyName, message = message)

			
			return redirect(url_for("studentSurveySubmitted"))

		return render_template('survey.html', questions = questionlist, surveyName = surveyName)

#SURVEY COMPLETED	
@app.route ('/student/surveySubmitted')
def studentSurveySubmitted():
	global auth
	if auth != 2:
		error = "Invalid Permissions. Please log in and try again."
		return render_template('login.html', error = error)
	else:
		return render_template('surveySubmitted.html')
	
	
#VIEW METRICS
@app.route('/metrics/<surveyName>')
def metrics(surveyName):
	global auth
	if auth != 0 :
		error = "Invalid Permissions. Please log in and try again."
		return render_template('login.html', error = error)
	else:
		# Information taken from https://plot.ly/python/bar-charts/
		message = ""
		global currentuser
		resplist = Survey.getSurveyMetrics(currentuser, surveyName)
		sid = Survey.getSurvey(surveyName).sid
		qid_list = []
		plots = [] #this will be a list of graphs
		textQuestions = [] #this will hold question and responses
		x = ['Strongly disagree', 'Disagree', 'Pass', 'Agree', 'Strognly agree']
		
		for response in resplist:
			qid = response.q_id
			try: #check if in list
				index = qid_list.index(qid)
			except: #if not in list 
				qid_list.append(qid)
		
		for qid in qid_list:
			question = Question.getQuestionFromId(qid)
			if question.isMCQ:
				# add MCQ info to plot format
				y = [0, 0, 0, 0, 0]
				for response in resplist:
					if response.q_id == qid:
						y[int(response.string)] = y[int(response.string)] + 1
				
				print(question.string)
				print(x)
				print(y)
				
				#data = []
				data = [go.Bar(x=x, y=y)]
				extension = plotly.offline.plot(data, filename=('templates/basic-bar-qid='+str(qid))+'.html')
				extension = extension.split('/')[-1]
				
				#plots.append([question.string, py.iplot(data, filename='basic bar')])
				plots.append([question.string, extension])
				
			else : #text responses
				answerlist = []
				for response in resplist:
					if response.q_id == qid:
						answerlist.append(response.string)
				textQuestions.append([question.string , answerlist])
				
		
		return render_template('metrics.html',  plots = plots, textQuestions = textQuestions, message = message)	


@app.route('/student/metrics/<surveyName>')
def studentMetrics(surveyName):
	global auth
	if auth != 2:
		error = "Invalid Permissions. Please log in and try again."
		return render_template('login.html', error = error)
	else:	
		global currentuser
		# Information taken from https://plot.ly/python/bar-charts/
		message = ""
		global currentuser
		resplist = Survey.getSurveyMetrics(currentuser, surveyName)
		sid = Survey.getSurvey(surveyName).sid
		qid_list = []
		plots = [] #this will be a list of graphs
		textQuestions = [] #this will hold question and responses
		x = ['Strongly disagree', 'Disagree', 'Pass', 'Agree', 'Strongly agree']
		
		for response in resplist:
			qid = response.q_id
			try: #check if in list
				index = qid_list.index(qid)
			except: #if not in list 
				qid_list.append(qid)
		
		for qid in qid_list:
			question = Question.getQuestionFromId(qid)
			if question.isMCQ:
				# add MCQ info to plot format
				y = [0, 0, 0, 0, 0]
				for response in resplist:
					if response.q_id == qid:
						y[int(response.string)] = y[int(response.string)] + 1
				
				print(question.string)
				print(x)
				print(y)
				
				#data = []
				data = [go.Bar(x=x, y=y)]
				extension = plotly.offline.plot(data, filename=('templates/basic-bar-qid='+str(qid))+'.html')
				extension = extension.split('/')[-1]
				
				#plots.append([question.string, py.iplot(data, filename='basic bar')])
				plots.append([question.string, extension])
				
			else : #text responses
				answerlist = []
				for response in resplist:
					if response.q_id == qid:
						answerlist.append(response.string)
				textQuestions.append([question.string , answerlist])
				
		
		return render_template('studentmetrics.html',  plots = plots, textQuestions = textQuestions, message = message)	

		
		

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
