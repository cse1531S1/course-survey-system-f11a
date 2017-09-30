from flask import Flask
from classes import SurveyPool, QuestionPool, Survey, Question
app = Flask(__name__)
question_list = []
