import googleHandler as gh
from canvasapi import Canvas
import requests
import os
import pymysql

API_URL = "https://canvas.instructure.com/"
API_KEY = "7~ZLz5HcFc2G5nJT5GCswngqzHx3gixHL0tjCQoD4CNlLQIDIQH3mXa6lIkdAeuhXU"
USER_ID = 37896736
googleDocumentName = "YO.pdf"
documentId = "1HL8b13b9HKAG7tj95kXzWafZc8BH6BJ0WPv3K_21wjU"
localDocumentName = "test.pdf"
content_type = "application/pdf"

canvas = Canvas(API_URL, API_KEY)
user = canvas.get_user(USER_ID)
courses = canvas.get_courses()
courses_hash = {}
assignments_hash = {}

for course in courses:
        try:
            if ((course.name).find("SP23") > -1):
                courses_hash[course.id] = course.name
                assignments = course.get_assignments()
                for assignment in assignments:
                    assignments_hash[assignment.id] = assignment.name
        except AttributeError:
            pass
print(courses_hash)
print(assignments_hash)
course1 = canvas.get_course(6327379)
assignment1 = course1.get_assignment(35995341)

def google_submit(course, assignment, docid, docname):
    # REQUEST 1 -------------------- Get upload url
    url = f'https://canvas.instructure.com/api/v1/courses/{course.id}/assignments/{assignment.id}/submissions/{USER_ID}/files'
    docurl = f'https://docs.google.com/document/d/{docid}/export?format=pdf'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    data = {'url': f'{docurl}',
            'name': f'{docname}',
            'content_type': f'{content_type}'}
    response = requests.post(url, data=data, headers=headers)

    # REQUEST 2 -------------------- Upload file from Google Drive
    upload_url = response.json()["upload_url"]
    upload_params = response.json()["upload_params"]
    # 3. Upload file to Canvas
    response = requests.post(upload_url, data=upload_params)
    # 4. Follow the redirect to complete upload
    redirect_url = response.headers['Location']
    response = requests.get(redirect_url, headers=headers)

    # REQUEST 3 -------------------- Submitting the assignment
    url = f'https://canvas.instructure.com/api/v1/courses/{course.id}/assignments/{assignment.id}/submissions'
    response = requests.post(url, headers=headers, data={'submission[submission_type]': 'online_upload', 'submission[file_ids][]': f'{response.json()["id"]}'})
    # print(response.status_code)
    # print(response.text)
    if response.status_code == 201:
        print("Success")

def local_submit(course, assignment, docname):
    # REQUEST 1 -------------------- Get upload url
    url = f'https://canvas.instructure.com/api/v1/courses/{course.id}/assignments/{assignment.id}/submissions/{USER_ID}/files'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    data = {'name': f'{docname}',
            'size': os.path.getsize(docname),
            'content_type': f'{content_type}',
            'parent_folder_path': '/'}
    response = requests.post(url, headers=headers, data=data)

    # REQUEST 2 -------------------- Upload file from Local Drive
    upload_url = response.json()["upload_url"]
    upload_params = response.json()["upload_params"]
    # 3. Upload file to Canvas
    with open(docname, "rb") as f:
        files = {'file': (docname, f, f'{content_type}')}
        response = requests.post(upload_url, data=upload_params, files=files)
    # 4. Follow the redirect to complete upload
    redirect_url = response.headers['Location']
    response = requests.get(redirect_url, headers=headers)

    # REQUEST 3 -------------------- Submitting the assignment
    url = f'https://canvas.instructure.com/api/v1/courses/{course.id}/assignments/{assignment.id}/submissions'
    response = requests.post(url, headers=headers, data={'submission[submission_type]': 'online_upload', 'submission[file_ids][]': f'{response.json()["id"]}'})
    # print(response.status_code)
    # print(response.text)
    if response.status_code == 201:
        print("Success")

def connect_database():
    # Set the Cloud SQL connection parameters
    connection_name = "timely-initial:us-central1:studocs-db-test"
    db_user = "root"
    db_password = ""
    db_name = "studocs-db-test"

    # Establish a connection to the database
    connection = pymysql.connect(
        unix_socket=f"/cloudsql/{connection_name}",
        user=db_user,
        password=db_password,
        db=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection.cursor() as cursor:
        # Execute a SQL query
        sql = "SELECT * FROM mytable"
        cursor.execute(sql)
    # Fetch the results
    results = cursor.fetchall()
    for row in results:
        print(row)

if __name__ == "__main__":
    # gh.createDirectory("course1")
    # gh.setDirectory("course1")
    # gh.createDoc("Assignment1")
    # gh.showCurrentDirectory()
    # gh.updateDoc("Assignment1")
    # gh.export_pdf("Assignment1")
    google_submit(course1, assignment1, gh.query("Assignment1"), "Assignment1.pdf")
    # local_submit(course1, assignment1, localDocumentName)
    # connect_database()
    print("Done")