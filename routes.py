from flask import Flask, redirect, render_template, request, url_for
from server import app, question_list
import csv

#https://www.w3schools.com/w3css/w3css_templates.asp

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

#NEW SURVEY PAGE
@app.route('/courseSelection')
def newsurvey():
    if True:
        # open course list csv and add to dictionary
	    courses_list = get_list_of_courses()
	    
	    #get semester list
	    semesters = get_sems()
	    
	    #pass though dictionary and sem list
    return render_template('courseselection.html', courses = courses_list, semesters = semesters)

#QUESTION LIST PAGE
@app.route('/QuestionList')
def questionlist():
	with open('questionList.csv','r') as csv_in:
		reader = csv.reader(csv_in)
		question_list = list(reader)
		stringVersion = "<br/>".join(item[0] for item in question_list)
	return render_template('questions.html', questions = stringVersion)
	
	
#List of surveys page
@app.route('/viewSurveysList')
def viewSurveysList():
	
	
	return render_template('viewSurveyList.html')
	
	
@app.route ('/survey/<semestername>/<coursename>', methods=["GET", "POST"])
def survey(course_id):
    with open('questionList.csv','r') as csv_in:
        reader = csv.reader(csv_in)
        question_list = list(reader)
        questions = [item[0] for item in question_list]
    if request.method == 'POST':
        responses = []
        for question in questions:
            responses.append(request.form[question])
            open('responses.txt', 'w').write('\n'.join(responses))
        return render_template('success.html', course_id=course_id)
    else:
        return render_template('survey.html', course_id=course_id, questions = questions)
	
	

