from flask import Flask
from newdb import Surveys, Questions, Responses, Courses, Users

app = Flask(__name__)
Survey = Surveys()
Question = Questions()
Response = Responses()
Course = Courses()
User = Users()
