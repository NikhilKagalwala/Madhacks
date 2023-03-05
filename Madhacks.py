from canvasapi import Canvas
import requests
import os

API_URL = "https://canvas.instructure.com/"
API_KEY = "7~ZLz5HcFc2G5nJT5GCswngqzHx3gixHL0tjCQoD4CNlLQIDIQH3mXa6lIkdAeuhXU"
canvas = Canvas(API_URL, API_KEY)
user = canvas.get_user(37896736)
courses = canvas.get_courses()

for course in courses:
        try:
            if ((course.name).find("SP23") > -1):
                # print(type(course.name))
                print(course)
                assignments = course.get_assignments()
                for assignment in assignments:
                    print(assignment)
        except AttributeError:
            pass

course1 = canvas.get_course(6327379)
assignment1 = course.get_assignment(35995341)
documentName = "test.pdf"
command = "curl https://canvas.wisc.edu/api/v1/courses/{0}/assignments/{1}/submissions/self/files \
            -F \'name={2}\' \
            -F \'size={3}\' \
            -F \'parent_folder_path={4}\' \
            -H \"Authorization: Bearer {5}\"".format(course.id, assignments[0].id, documentName, os.path.getsize(documentName), "/", API_KEY)
# print(command)
os.system(command)