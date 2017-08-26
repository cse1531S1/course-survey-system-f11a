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
         
         
def get_courses():
    courses = get_sems()
    return courses
    
def get_sems():
    semesters = []
    found = True
    while(found): #while a unique course has not been added
        found = False
        with open('courses.csv','r') as csv_in: #open the csv
            reader = csv.reader(csv_in)
            next_min = "zzzzz"
            for row in reader: #for each row in the csv
                if(row != []):
                    if(row[1] < next_min): #if the current semester is less than the minimum
                        if(inList(semesters, row[1]) == False): #check not already in 
                            next_min = row[1]
                            found = True
            print("Newest course is " + next_min)
            if(found):
                semesters.append(next_min)
        #found = True
    return semesters


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
    if request.method == 'POST':
        question = request.form['q']
        with open('questionList.csv','a') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow([question])
    return render_template('newquestions.html')

#NEW SURVEY PAGE
@app.route('/NewSurvey')
def newsurvey():
    courses_list = []
    if True:
        # open course list csv and add to list of lists
	    courses_list = get_courses()
	    #pass though list of lists
    return render_template('newsurvey.html', courses = courses_list)

#QUESTION LIST PAGE
@app.route('/QuestionList')
def questionlist():
	with open('questionList.csv','r') as csv_in:
		reader = csv.reader(csv_in)
		question_list = list(reader)
		stringVersion = "<br/>".join(item[0] for item in question_list)
	return render_template('questions.html', questions = stringVersion)
	
	
	
	
	
	
	
	
	

