from flask import Flask
from classes import SurveyPool, Survey, Question, Data

app = Flask(__name__)
question_list = []

surveyList = SurveyPool("surveys")
surveyList.generatePool()