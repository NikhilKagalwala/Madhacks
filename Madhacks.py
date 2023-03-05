from canvasapi import Canvas
import json
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

# REQUEST 1 --------------------
course1 = canvas.get_course(6327379)
assignment1 = course1.get_assignment(35995341)
documentName = "test.pdf"
url = 'https://canvas.instructure.com/api/v1/courses/{0}/assignments/{1}/submissions/self/files'.format(course.id, assignments[0].id)
headers = {'Authorization': 'Bearer {0}'.format(API_KEY)}
data = {'name': '{0}'.format(documentName),
        'size': os.path.getsize(documentName),
        'content_type': 'application/pdf',
        'parent_folder_path': '/'}

response = requests.post(url, headers=headers, data=data)

print(response.status_code)
print(response.text)

# REQUEST 2 --------------------
upload_url = response.json()['upload_url'].strip()
filename = response.json()['upload_params']['filename']
content_type = response.json()['upload_params']['content_type']
data2 = {'key': (None, documentName),
         'filename': filename,
         'content_type': content_type,
         'file': open('test.pdf', 'rb')}

response2 = requests.post(upload_url, data=data2)

print(response2.status_code)
print(response2.text)
