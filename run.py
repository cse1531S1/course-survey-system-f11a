from routes import app
import classes.py

surveyList = SurveyPool("surveys")
surveyList.generatePool()

app.run(debug = True)