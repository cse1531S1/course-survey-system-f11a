from flask import Flask, redirect, render_template, request, url_for
from server import app, question_list
import csv

#https://www.w3schools.com/w3css/w3css_templates.asp

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
	# TODO
	return render_template('newsurvey.html')

#QUESTION LIST PAGE
@app.route('/QuestionList')
def questionlist():
	with open('questionList.csv','r') as csv_in:
		reader = csv.reader(csv_in)
		question_list = list(reader)
		string = "\n".join(item[0] for item in question_list)
	return render_template('questions.html', questions = string)