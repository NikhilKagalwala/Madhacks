from canvasapi import Canvas
import requests
import os

API_URL = "https://canvas.instructure.com/"
API_KEY = "7~ZLz5HcFc2G5nJT5GCswngqzHx3gixHL0tjCQoD4CNlLQIDIQH3mXa6lIkdAeuhXU"
USER_ID = 37896736
canvas = Canvas(API_URL, API_KEY)
user = canvas.get_user(USER_ID)
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
assignment1 = course1.get_assignment(35995341)
documentName = "YO.pdf"
content_type = "application/pdf"
documentId = "1HL8b13b9HKAG7tj95kXzWafZc8BH6BJ0WPv3K_21wjU"
docurl = f'https://docs.google.com/document/d/{documentId}/export?format=pdf'

# REQUEST 1 -------------------- Get upload url
url = f'https://canvas.instructure.com/api/v1/courses/{course1.id}/assignments/{assignment1.id}/submissions/{USER_ID}/files'
headers = {'Authorization': f'Bearer {API_KEY}'}
data = {'url': f'{docurl}',
        'name': f'{documentName}',
        'content_type': f'{content_type}'}
response = requests.post(url, data=data, headers=headers)
# print(response.status_code)
# print(response.text)


# REQUEST 2 -------------------- Upload file from Google Drive
upload_url = response.json()["upload_url"]
upload_params = response.json()["upload_params"]

# 3. Upload file to Canvas
data = {'target_url': f'{docurl}'}
response = requests.post(upload_url, data=upload_params)
# print(response.status_code)
# print(response.text)

# 4. Follow the redirect to complete upload
redirect_url = response.headers['Location']
print(redirect_url)
response = requests.get(redirect_url, headers=headers)
# print(response.status_code)
# print(response.text)


# REQUEST 3 -------------------- Submitting the assignment
url = f'https://canvas.instructure.com/api/v1/courses/{course1.id}/assignments/{assignment1.id}/submissions'
response = requests.post(url, headers=headers, data={'submission[submission_type]': 'online_upload', 'submission[file_ids][]': f'{response.json()["id"]}'})
# print(response.status_code)
# print(response.text)
