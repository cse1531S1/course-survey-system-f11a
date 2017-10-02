from flask import Flask
from classes import SurveyPool, QuestionPool

app = Flask(__name__)
question_list = []

allSurveys = SurveyPool()
allSurveys.generatePool()

allQuestions = QuestionPool()
allQuestions.generatePool()