Section 1

1. unittest
	Unit test functionality suite
2. os
	Operating system interface for file creation/deletion
3. csv
	File interface for comma seperate values files
4. sqlalchemy
	Object relational mapper and database interface
5. Flask
	Interface and template engine for website development
6. plotly
	Creates beautiful plots


Section 2
	If this is the first time you're running the server:
		1. Ensure that Systemdatabase.db doesn't exist; if it does, run the command $rm Systemdatabase.db
		2. $python3 startup.py 
		3. $python3 run.py 
		4. Project URL: http://localhost:5000
	If you've previously run the server:
		1. $python3 run.py 
		2. Project URL: http://localhost:5000


Section 3
	Note: The use of the testing suite will remove all data from the database. Please think carefully before running this script.
	1. $python3 testcases.py
	
	Note: List of tests:
		test_validity_with_false_user
		test_validity_with_real_user
		test_add_new_optional_question
		test_add_new_mandatory_question
		test_purity_of_mandatory_fetch
		test_purity_of_optional_fetch
		test_question_deletion
		test_add_new_survey
		test_add_question_to_survey
		test_purity_of_mandatory_fetch
		test_purity_of_review_fetch
		test_purity_of_live_fetch
		test_purity_of_closed_fetch
		test_purity_of_my_review_fetch
		test_purity_of_my_live_fetch
		test_purity_of_my_closed_fetch
		test_add_empty_question
		test_add_empty_response_to_question
		test_remove_empty_question
		test_add_empty_survey
		test_add_empty_question
		test_empty_set_stage