from flask import Flask
from classes import SurveyPool, Authentication, QuestionPool

app = Flask(__name__)
question_list = []

surveyList = SurveyPool()
surveyList.generatePool()
authenticate = Authentication()
authenticate.buildUserBase() 
allQuestions = QuestionPool()
