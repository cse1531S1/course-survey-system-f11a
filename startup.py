from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv
from newdb import Users, Courses, users_courses, Base

engine = create_engine('sqlite:///Systemdata.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

with open('passwords.csv', 'r') as csv_in:
    reader = csv.reader(csv_in)
    for row in reader:
        #print (row)
        person = Users(zid = str(row[0]), password = str(row[1]))
        if str(row[2]) == 'student':
            person.permission = 2
        
        elif str(row[2]) == 'staff':
            person.permission = 1
        
        else:
            person.permission = 0

        session.add(person)

with open('courses.csv','r') as csv_in:
    reader = csv.reader(csv_in)
    for row in reader:
        #print (row)
        course = Courses(coursename = str(row[0])+str(row[1]))
        session.add(course)

with open('enrolments.csv', 'r') as csv_in:
    reader = csv.reader(csv_in)
    for row in reader:
        person = session.query(Users).filter_by(zid=str(row[0])).one()
        course = session.query(Courses).filter_by(coursename=str(row[1])+str(row[2])).one()
        person.enrolment.append(course)

        # print(row)
        # statement = users_courses.insert().values(userid=int(row[0]), coursename=str(row[1])+str(row[2]))
        # session.execute(statement)

#add admin user
admin = Users(zid = 'admin', password = 'admin', permission = 0)
session.add(admin)

session.commit()
print("Database built.")
session.close()
