from flask import Flask
from newdb import Controller

app = Flask(__name__)
reader = Controller()