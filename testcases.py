import unittest
import os
from newdb import *
from sqlalchemy import exc, orm
import subprocess

class TestUserLogin(unittest.TestCase):

	def setUp(self):
		self.user = Users()

	def test_validity_with_false_user(self):
		testVal = self.user.isValidUser("fake", "news")
		self.assertEqual(None, testVal)

	def test_validity_with_real_user(self):
		user = self.user.isValidUser("161", "student563")
		self.assertEqual(user.zid, "161")
		self.assertEqual(user.password, "student563")
		self.assertEqual(user.permission, 2)

class TestQuestionInsertion(unittest.TestCase):

	def setUp(self):
		self.questions = Questions()

	def test_add_new_question(self):
		self.questions.addNewQuestion("Why is a duck?",0,0)
		q = self.questions.getQuestionFromId(1)
		self.assertNotEqual(q,None)
		self.assertEqual(q.string, "Why is a duck?")
		self.assertEqual(q.isMCQ, 0)
		self.assertEqual(q.isMan, 0)

	def test_purity_of_mandatory_fetch(self):
		qlist = self.questions.getMandatoryQuestions()
		for q in qlist:
			self.assertEqual(q.isMan, 1)

	def test_purity_of_optional_fetch(self):
		qlist = self.questions.getOptionalQuestions()
		for q in qlist:
			self.assertEqual(q.isMan, 0)

	def test_question_deletion(self):
		self.questions.addNewQuestion("This should be deleted",1,1)
		q = self.questions.getQuestion("This should be deleted")
		self.assertNotEqual(q,None)	
		self.questions.removeQuestion(q.qid)
		q = self.questions.getQuestion("This should be deleted")
		self.assertEqual(q,None)

class TestSurveys(unittest.TestCase):

	def setUp(self):
		self.user = Users()
		self.myStudentOne = self.user.isValidUser("161","student563")
		self.myStaffOne = self.user.isValidUser("74","staff461")
		self.myStudentTwo = self.user.isValidUser("125","student729")
		self.myStaffTwo = self.user.isValidUser("50","staff670") #COMP493118S1
		self.myStudentThree = self.user.isValidUser("114","student668")
		self.myStaffThree = self.user.isValidUser("52","staff342")# COMP951717S2


		self.surveys = Surveys()
		self.questions = Questions()

	def test_add_new_survey(self):
		s = self.surveys.addNewSurvey("COMP490418S2")
		self.assertNotEqual(s,None)
		self.assertEqual(s.course,"COMP490418S2")
	def test_add_empty_survey(self):
		with self.assertRaises(Exception):
			s = self.surveys.addNewSurvey("")
	def test_add_question_to_survey(self):
		s = self.surveys.addNewSurvey("COMP212117S2")
		self.assertNotEqual(s,None)
		self.assertEqual(s.course,"COMP212117S2")
		self.questions.addNewQuestion("Why is an owl?",0,0)
		q = self.questions.getQuestion("Why is an owl?")
		self.surveys.addQuestion(s, q)
		qlist = self.surveys.getQuestionsInSurvey(s)
		self.assertNotEqual(qlist, None)

	def test_purity_of_mandatory_fetch(self):
		s = self.surveys.addNewSurvey("COMP490417S2")
		self.questions.addNewQuestion("MANDATORY MCQ",1,1)
		self.questions.addNewQuestion("MANDATORY TEXT",0,1)
		self.questions.addNewQuestion("OPTIONAL MCQ",1,0)
		self.questions.addNewQuestion("OPTIONAL TEXT",0,0)
		
		q = self.questions.getQuestion("MANDATORY MCQ")
		self.surveys.addQuestion(s, q)
		q = self.questions.getQuestion("MANDATORY TEXT")
		self.surveys.addQuestion(s, q)
		q = self.questions.getQuestion("OPTIONAL MCQ")
		self.surveys.addQuestion(s, q)
		q = self.questions.getQuestion("OPTIONAL TEXT")
		self.surveys.addQuestion(s, q)

		qlist = self.surveys.getMandatorySurveyQuestions(s)
		self.assertNotEqual(qlist, None)
		for q in qlist:
			self.assertEqual(q.isMan, 1)

	def test_purity_of_review_fetch(self):
		s = self.surveys.addNewSurvey("COMP152117S2")
		s = self.surveys.getSurvey("COMP152117S2")
		self.assertNotEqual(s, None)
		self.surveys.setStage(s,0)

		sList = self.surveys.getReviewSurveys()
		self.assertNotEqual(sList, None)
		for s in sList:
			self.assertEqual(s.stage, 0)

	def test_purity_of_live_fetch(self):
		s = self.surveys.addNewSurvey("COMP153117S2")
		s = self.surveys.getSurvey("COMP153117S2")
		self.assertNotEqual(s, None)
		self.surveys.setStage(s,1)

		sList = self.surveys.getLiveSurveys()
		self.assertNotEqual(sList, None)
		for s in sList:
			self.assertEqual(s.stage, 1)



	def test_purity_of_closed_fetch(self):
		s = self.surveys.addNewSurvey("COMP140017S2")
		s = self.surveys.getSurvey("COMP140017S2")
		self.assertNotEqual(s, None)
		self.surveys.setStage(s,2)

		sList = self.surveys.getClosedSurveys()
		self.assertNotEqual(sList, None)
		for s in sList:
			self.assertEqual(s.stage, 2)



	def test_purity_of_my_review_fetch(self):
		s = self.surveys.getSurvey("COMP490417S2")
		self.assertNotEqual(s, None)
		self.surveys.setStage(s,0)

		sList = self.surveys.getMyReviewSurveys(self.myStaffOne)
		self.assertNotEqual(None, sList)
		for s in sList:
			self.assertEqual(s.stage,0)


	def test_purity_of_my_live_fetch(self):
		s = self.surveys.addNewSurvey("COMP493118S1")
		s = self.surveys.getSurvey("COMP493118S1")
		self.assertNotEqual(s, None)
		self.surveys.setStage(s,1)

		sList = self.surveys.getMyReviewSurveys(self.myStudentTwo)
		self.assertNotEqual(None, sList)
		for s in sList:
			self.assertEqual(s.stage,1)

	def test_purity_of_my_closed_fetch(self):
		s = self.surveys.addNewSurvey("COMP951717S2")
		s = self.surveys.getSurvey("COMP951717S2")
		self.assertNotEqual(s, None)
		self.surveys.setStage(s,2)

		sList = self.surveys.getMyReviewSurveys(self.myStudentThree)
		self.assertNotEqual(None, sList)
		for s in sList:
			self.assertEqual(s.stage,2)

if __name__ == '__main__':
	try: 
		os.remove('SystemData.db')
	except:
		pass
	subprocess.call(["python3", "startup.py"])
	unittest.main()
	os.remove('SystemData.db')
