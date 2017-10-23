from flask import Flask, redirect, render_template, request, url_for
from newserver import app, Survey, Question, Response, User, Course
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

#LOGIN PAGE
global currentuser
global auth
auth = -1

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


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
			if currentuser.getpermission() == 0:
				auth = 0
				return redirect(url_for('admindashboard'))
				
			elif currentuser.getpermission() == 1:
				auth = 1
				return redirect(url_for('staffdashboard'))
				
			else:
				auth = 2
				return redirect(url_for('studentdashboard'))
			
	return render_template('login.html', error=error)
	
@app.route('/login/error', methods=["GET","POST"])
def login_error():
	error = 'Invalid Credentials. Please try again.'
	global auth
	auth = -1
	if request.method == 'POST':
		#check for user against database
		global currentuser
		currentuser = User.isValidUser(request.form['zID'], request.form['password'])

		if currentuser == None:
			error = 'Invalid Credentials. Please try again.'
		else:
			if currentuser.getpermission() == 0:
				auth = 0
				return redirect(url_for('admindashboard'))
				
			elif currentuser.getpermission() == 1:
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
		return redirect(url_for('login_error'))
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
		return redirect(url_for('login_error'))
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
		return redirect(url_for('login_error'))
	else:
	    return render_template('addedQuestion.html')
    

#QUESTION LIST PAGE
@app.route('/admin/allQuestions',methods=["GET","POST"])
def questionlist():
    # qlist = allQuestions.getVisibleQuestions()
	global auth
	if auth != 0:
		error = "Invalid Permissions. Please log in and try again."
		return redirect(url_for('login_error'))
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
		return redirect(url_for('login_error'))
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
		return redirect(url_for('login_error'))
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
	surveyname = coursename+semestername
	if auth != 0:
		error = "Invalid Permissions. Please log in and try again."
		return redirect(url_for('login_error'))
	else:
		message = ""
		if request.method == "POST":
			thisSurvey = Survey.addNewSurvey(surveyname)
			for v in request.form:
				thisQuestion = Question.getQuestion(v)
				if thisQuestion != None:
					Survey.addQuestion(thisSurvey, thisQuestion)

			return redirect(url_for('questionselected'))
		
		#Else, get questionlist from pool, and display these onto the screen as checkboxes
		else:
			if Survey.getSurvey(surveyname):
				message = "Survey already exists! Please select a different survey"
			mandatoryQ = Question.getMandatoryQuestions()	
			return render_template('choosequestions.html', questions = mandatoryQ, message = message)


#PAGE AFTER SELECTING QUESTIONS
@app.route('/admin/surveySubmitted', methods=['GET','POST'])
def questionselected():
	global auth
	if auth != 0:
		error = "Invalid Permissions. Please log in and try again."
		return redirect(url_for('login_error'))
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
		return redirect(url_for('login_error'))
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
		return redirect(url_for('login_error'))
	else:
		#this takes in all the questions associated with survey so far (assuming these are mandatory)
		#make sure that each survey is only filled out once by any staff
		thisSurvey = Survey.getSurvey(surveyName)

		questionlist = Survey.getQuestionsInSurvey(thisSurvey)
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
		return redirect(url_for('login_error'))
	else:
		message = "Survey was sucessfully reviewed." #Make this display if the survey was sucessful or not 
		return render_template('staffSurveySubmitted.html', message = message)




#STUDENT DASHBOARD
@app.route('/student/dashboard')
def studentdashboard():
	global auth
	if auth != 2:
		error = "Invalid Permissions. Please log in and try again."
		return redirect(url_for('login_error'))
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
		return redirect(url_for('login_error'))
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
				Question.addResponseToQuestion(thisQuestion, thisResponse)
				

			print(len(manquestions))
			if len(manquestions):
				message = "ERROR: Please enter a response to all mandatory questions"
				Response.removeResponsesToSurvey(thisSurvey)
				manquestions = Survey.getMandatorySurveyQuestions(thisSurvey)
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
		return redirect(url_for('login_error'))
	else:
		return render_template('surveySubmitted.html')
	
	
#VIEW METRICS
@app.route('/metrics/<surveyName>')
def metrics(surveyName):
	global auth
	if auth != 0 :
		error = "Invalid Permissions. Please log in and try again."
		return redirect(url_for('login_error'))
	else:
		# Information taken from https://plot.ly/python/bar-charts/
		message = ""
		global currentuser
		resplist = Survey.getSurveyMetrics(currentuser, surveyName)
		sid = Survey.getSurveyID(surveyName)
		qid_list = []
		plots = [] #this will be a list of graphs
		textQuestions = [] #this will hold question and responses
		x = ['Strongly disagree', 'Disagree', 'Pass', 'Agree', 'Strongly agree']
		
		for response in resplist:
			qid = response.getResponseQID()
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
					if response.getResponseQID() == qid:
						y[int(response.getResponseString())] = y[int(response.getResponseString())] + 1
				
				print(question.getQuestionString())
				print(x)
				print(y)
				
				#data = []
				data = [go.Bar(x=x, y=y)]
				extension = plotly.offline.plot(data, filename=('templates/basic-bar-qid='+str(qid))+'.html')
				extension = extension.split('/')[-1]
				
				#plots.append([question.string, py.iplot(data, filename='basic bar')])
				plots.append([question.getQuestionString(), extension])
				
			else : #text responses
				answerlist = []
				for response in resplist:
					if response.getResponseQID() == qid:
						answerlist.append(response.getResponseString())
				textQuestions.append([question.getQuestionString() , answerlist])
				
		
		return render_template('metrics.html',  plots = plots, textQuestions = textQuestions, message = message)	

#VIEW METRICS
@app.route('/staff/metrics/<surveyName>')
def staffMetrics(surveyName):
	global auth
	if auth != 1 :
		error = "Invalid Permissions. Please log in and try again."
		return redirect(url_for('login_error'))
	else:
		# Information taken from https://plot.ly/python/bar-charts/
		message = ""
		global currentuser
		resplist = Survey.getSurveyMetrics(currentuser, surveyName)
		sid = Survey.getSurveyID(surveyName)
		qid_list = []
		plots = [] #this will be a list of graphs
		textQuestions = [] #this will hold question and responses
		x = ['Strongly disagree', 'Disagree', 'Pass', 'Agree', 'Strongly agree']
		
		for response in resplist:
			qid = response.getResponseQID()
			try: #check if in list
				index = qid_list.index(qid)
			except: #if not in list 
				qid_list.append(qid)
		
		for qid in qid_list:
			question = Question.getQuestionFromId(qid)
			if question.getMCQ():
				# add MCQ info to plot format
				y = [0, 0, 0, 0, 0]
				for response in resplist:
					if response.getResponseQID() == qid:
						y[int(response.getResponseString())] = y[int(response.getResponseString())] + 1
				
				print(question.getQuestionString())
				print(x)
				print(y)
				
				#data = []
				data = [go.Bar(x=x, y=y)]
				extension = plotly.offline.plot(data, filename=('templates/basic-bar-qid='+str(qid))+'.html')
				extension = extension.split('/')[-1]
				
				#plots.append([question.string, py.iplot(data, filename='basic bar')])
				plots.append([question.getQuestionString(), extension])
				
			else : #text responses
				answerlist = []
				for response in resplist:
					if response.getResponseQID() == qid:
						answerlist.append(response.getResponseString())
				textQuestions.append([question.getQuestionString() , answerlist])
				
		
		return render_template('staffMetrics.html',  plots = plots, textQuestions = textQuestions, message = message)

@app.route('/student/metrics/<surveyName>')
def studentMetrics(surveyName):
	global auth
	if auth != 2:
		error = "Invalid Permissions. Please log in and try again."
		return redirect(url_for('login_error'))
	else:	
		global currentuser
		# Information taken from https://plot.ly/python/bar-charts/
		message = ""
		global currentuser
		resplist = Survey.getSurveyMetrics(currentuser, surveyName)
		sid = Survey.getSurveyID(surveyName)
		qid_list = []
		plots = [] #this will be a list of graphs
		textQuestions = [] #this will hold question and responses
		x = ['Strongly disagree', 'Disagree', 'Pass', 'Agree', 'Strongly agree']
		
		for response in resplist:
			qid = response.getResponseQID()
			try: #check if in list
				index = qid_list.index(qid)
			except: #if not in list 
				qid_list.append(qid)
		
		for qid in qid_list:
			question = Question.getQuestionFromId(qid)
			if question.getMCQ():
				# add MCQ info to plot format
				y = [0, 0, 0, 0, 0]
				for response in resplist:
					if response.getResponseQID() == qid:
						y[int(response.getResponseString())] = y[int(response.getResponseString())] + 1
				
				print(question.getQuestionString())
				print(x)
				print(y)
				
				#data = []
				data = [go.Bar(x=x, y=y)]
				extension = plotly.offline.plot(data, filename=('templates/basic-bar-qid='+str(qid))+'.html')
				extension = extension.split('/')[-1]
				
				#plots.append([question.string, py.iplot(data, filename='basic bar')])
				plots.append([question.getQuestionString(), extension])
				
			else : #text responses
				answerlist = []
				for response in resplist:
					if response.q_id == qid:
						answerlist.append(response.getResponseString())
				textQuestions.append([question.getQuestionString() , answerlist])
				
		
		return render_template('studentmetrics.html',  plots = plots, textQuestions = textQuestions, message = message)
