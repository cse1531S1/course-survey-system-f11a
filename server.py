from flask import Flask
from classes import SurveyPool

app = Flask(__name__)
question_list = []

surveyList = SurveyPool()
surveyList.generatePool()