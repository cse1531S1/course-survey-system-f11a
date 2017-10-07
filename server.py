from flask import Flask
from classes import SurveyPool, Authentication, QuestionPool

app = Flask(__name__)
question_list = []

allSurveys = SurveyPool()
allSurveys.generatePool()
authenticate = Authentication()
allQuestions = QuestionPool()
allQuestions.generatePool()