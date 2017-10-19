from flask import Flask
from newdb import SurveySystem, Authentication, User, QuestionPool, CoursePool, SurveyPool, ResponsePool, Question, Response, Survey

app = Flask(__name__)
#NEED TO CREATE INSTACES OF OBJECTS
