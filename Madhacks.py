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

# REQUEST 1 --------------------
course1 = canvas.get_course(6327379)
assignment1 = course1.get_assignment(35995341)
documentName = "test.pdf"
content_type = "application/pdf"
url = f'https://canvas.instructure.com/api/v1/courses/{course1.id}/assignments/{assignment1.id}/submissions/{USER_ID}/files'
headers = {'Authorization': f'Bearer {API_KEY}'}
data = {'name': f'{documentName}',
        'size': os.path.getsize(documentName),
        'content_type': f'{content_type}',
        'parent_folder_path': '/'}
response = requests.post(url, headers=headers, data=data)
# print(response.status_code)
# print(response.text)


# REQUEST 2 --------------------
upload_url = response.json()["upload_url"]
upload_params = response.json()["upload_params"]

# 3. Upload file to Canvas
with open(documentName, "rb") as f:
    files = {'file': (documentName, f, f'{content_type}')}
    response = requests.post(upload_url, data=upload_params, files=files)
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
print(response.status_code)
# print(response.text)
