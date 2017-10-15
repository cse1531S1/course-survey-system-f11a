from flask import Flask, redirect, render_template, request, url_for
from newserver import app, reader
# from classes import Survey, Question, Authentication, User
from newdb import Controller
import csv

#THIS IS A COMMENT

#LOGIN PAGE
@app.route('/', methods=["GET","POST"])
def login():
	error = None
	if request.method == 'POST':
		#check for user against database
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

#STAFF DASHBOARD
@app.route('/staff/dashboard')
def staffdashboard():
	# usersurveys = currentuser.getCourses()#list of courses assigned to staff
	# print("usersurveys", usersurveys)
	tobereviewed = []
	sclosed = []
	# tobereviewed = reader.getMyReviewSurveys(currentuser)
	# reviewed = reader.getMyReviewedSurveys()
	# sclosed = reader.getMyClosedSurveys()
	# for survey in usersurveys:
	# 	surveyobj = allSurveys.getSurveyByName(survey)

	# 	#if survey object exists for that course and it is in review phase
	# 	if surveyobj:
	# 		if surveyobj.getStage() == 1:
	# 			print(surveyobj.getCourseName())
	# 			tobereviewed.append(surveyobj)
	# 		if surveyobj.getStage() == 3:
	# 			sclosed.append(surveyobj)

	# print("tobereviewed",tobereviewed)
	# print ("sclosed", sclosed)
	return render_template('staffDashboard.html', sreviewed = tobereviewed, sclosed = sclosed)

#STUDENT DASHBOARD
@app.route('/student/dashboard')
def studentdashboard():
	# print("Calling populateStudentSurveys")
	# currentuser.populateStudentSurveys(allSurveys.getSurveyList())
	# tobeanswered = currentuser.getNotCompleted()
	# global metricsViewable
	surveyclosed = []
	tobeanswered = []
	# allcourses = currentuser.getCourses()
	# print("Allcourse",allcourses)

	# for course in allcourses:
	# 	thisSurvey = allSurveys.getSurveyByName(course)
	# 	if thisSurvey:
	# 		if thisSurvey.getStage() == 3:
	# 			surveyclosed.append(course)
	# 			print("adding",course)

	# sclosed = currentuser.getClosedSurveys()
	

	return render_template('studentDashboard.html', sanswered = tobeanswered, sclosed = surveyclosed)



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
	
# #VIEW ACTIVE SURVEYS
# @app.route('/admin/viewSurveysList',methods=["GET","POST"]) 
# def viewActiveSurveys():
#     slist = allSurveys.getSurveyList()
#     slive = []
    
#     if request.method == 'POST':
#         for s in slist:
#             if(s.getCourseName() == request.form["submit"]):
#                 s.setStage(3)
#                 global metricsViewable 
#                 metricsViewable = True

#     for s in slist:
#         if s.getStage() == 2:
#             slive.append(s)
            
#     #Pass through live surveys list
#     return render_template('viewSurveyList.html', surveyList = slive)

#SELECT QUESTIONS PAGE
  
#need to change this to /admin/chooseQuestions depending on implementation. Look into HTML FORMS 
#in tutorial: localhost/adminSurveyForm?choice=COMP2041+17s2

@app.route('/admin/chooseQuestions/<coursename>/<semestername>',methods=["GET","POST"])
def courseObject(coursename, semestername):
	#If they've submitted, then for each of these, instantiate a questions object, and a data object
	if request.method == "POST":
		surveyname = coursename+semestername
		
		# Implement afterwards
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
    
# #choose optional questions
# @app.route('/staff/reviewSurvey/<surveyName>', methods=["GET","POST"])
# def reviewSurvey(surveyName):

#     thisSurvey = allSurveys.getSurveyByName(surveyName)#get survey object
#     print("The survey we just got is: " + thisSurvey.getCourseName())
#     allqinsurvey = thisSurvey.getQuestions() #list of questionids
#     print("The number of questions in this survey is: " + str(len(allqinsurvey)))
#     allq = allQuestions.getVisibleQuestions()#allq has all quesions from pool
#     print("The number of questions globally is: "+ str(len(allq)))
#     questionlist = []
#     optionallist = []
        
#     #find out all mandatory questions for this survey
#     for manq in allqinsurvey:
#         questionlist.append(allQuestions.getQuestion(manq))

#     #pick all optional questions
#     for opq in allq:
#         if opq.getIsMandatory() == 0:
#             optionallist.append(opq)

#     if request.method == "POST": 
#         print("The information being sent is: ")
#         print(request.form) 
#         for v in request.form:
#             for q in optionallist:
#                 if v == str(q.getQuestionID()):
#                 	print("*************YAAAHS************")
#                 	thisSurvey.addQuestion(q)

#         thisSurvey.setStage(2)
#         #currentuser.nowCompleted(surveyName)
        
#         return redirect(url_for('finishedReview'))
           
#     return render_template('reviewSurvey.html', manqlist = questionlist, opqlist = optionallist)
        
# #REVIEW FINISHED
# @app.route('/staff/finishedReview')
# def finishedReview():
    
#     message = "Survey was sucessfully reviewed." #Make this display if the survey was sucessful or not 
    
#     return render_template('staffSurveySubmitted.html', message = message)

	
# # SURVEY PAGE
# @app.route ('/student/survey/<surveyName>', methods=["GET", "POST"])
# def survey(surveyName):
# 	thisSurvey = allSurveys.getSurveyByName(surveyName)
# 	#print("We've identified survey as: "+ thisSurvey.getCourseName()) #ALL CLEAR
# 	allqinsurvey = thisSurvey.getQuestions() #list of questionids
# 	#print("Number of questions identified is: " + str(len(allqinsurvey))) #ALL CLEAR
# 	questionlist = []
# 	resplist = [] #list of all responses

# 	#find out all questions for this survey
# 	for qId in allqinsurvey:
# 		questionlist.append(allQuestions.getQuestion(qId))
		
# 	#print("Number of questions after scan is: " + str(len(questionlist))) #ALL CLEAR

# 	if request.method == 'POST':
# 		#print("********")
# 		#print(request.form)
# 		#print("********")
		
# 		#for each qid
# 		for v in request.form:
# 			failedQuestion = True #assume true
# 			for q in questionlist:
# 				if str(v) == str(q.getQuestionID()):
# 					if(request.form[str(q.getQuestionID())]):
# 						resplist.append(request.form[str(q.getQuestionID())])
# 						failedQuestion = False

# 			if (failedQuestion == True):
# 					print("Failed survey on question: " + allQuestions.getQuestion(int(qId)).getQuestionString() )
# 					message = "ERROR: Please enter a response to all questions"
# 					return render_template('survey.html', questions = questionlist, surveyName = surveyName, message = message)
		
# 		# sucessful survey entry 		
# 		thisSurvey.addResponse(resplist)
# 		print("CURRENT UID IS: " + str(currentuser.getUID()))
# 		thisSurvey.addUser(str(currentuser.getUID()))
# 		currentuser.nowCompleted(surveyName)
# 		return redirect(url_for("studentSurveySubmitted"))

# 	return render_template('survey.html', questions = questionlist, surveyName = surveyName)

# #SURVEY COMPLETED	
# @app.route ('/student/surveySubmitted')
# def studentSurveySubmitted():
# 	return render_template('surveySubmitted.html')
	
	
# #VIEW METRICS
# @app.route('/metrics/<surveyName>')
# def metrics(surveyName):
# 	thisSurvey = allSurveys.getSurveyByName(surveyName)
# 	allresponses = []
# 	if (thisSurvey.getStage() == 3) or (thisSurvey.getStage() == 2 and currentuser.getPermission() == 0):
# 		resplist = thisSurvey.getResponses()
# 		print("all responses object", resplist)
# 	return render_template('metrics.html', resplist = resplist)


# @app.route('/student/metrics/<surveyName>')
# def studentMetrics(surveyName):
# 	thisSurvey = allSurveys.getSurveyByName(surveyName)
# 	allresponses = []
# 	if (thisSurvey.getStage() == 3) or (thisSurvey.getStage() == 2 and currentuser.getPermission() == 0):
# 		resplist = thisSurvey.getResponses()
# 		print("all responses object", resplist)
# 	return render_template('studentmetrics.html', resplist = resplist)
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
