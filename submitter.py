import googleHandler as gh
from canvasapi import Canvas
import requests
import os
import pymysql
import mysql.connector

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

def insert_user_info():
    my_connect = mysql.connector.connect(
    host="35.226.41.35",
    user="root",
    passwd="ONTIME123",
    database="main_db"
    )
    ####### end of connection details ####
    my_cursor = my_connect.cursor()

    my_cursor.execute("SELECT * FROM courses")
    my_result = my_cursor.fetchone()
    while my_result is not None:
        print(my_result)
        my_result = my_cursor.fetchone()

    sql = "INSERT INTO user_info (password_hash, name, email, canvas_api_key, canvas_user_id, canvas_website, google_api_key, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = ("password123", "John Doe", "ontimemadhacks@gmail.com", API_KEY, USER_ID, API_URL, "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", "1234567890")
    my_cursor.execute(sql, val)

    my_connect.commit()

    print(my_cursor.rowcount, "record inserted.")

def insert_assignments(assignment_id, course_id, assignment_name, due_date, assignment_link, google_docs_id):
    my_connect = mysql.connector.connect(
    host="35.226.41.35",
    user="root",
    passwd="ONTIME123",
    database="main_db"
    )
    ####### end of connection details ####
    my_cursor = my_connect.cursor()
    user_id = get_user(USER_ID)
    query = "INSERT INTO courses (user_id, assignment_id, due_date, google_docs_id, course_id, assignment_name, assignment_link) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (user_id, assignment_id, due_date, google_docs_id, course_id, assignment_name, assignment_link)
    my_cursor.execute(query, values)

    my_connect.commit()
    print(my_cursor.rowcount, "record inserted.")

def insert_courses():
    my_connect = mysql.connector.connect(
    host="35.226.41.35",
    user="root",
    passwd="ONTIME123",
    database="main_db"
    )
    ####### end of connection details ####
    my_cursor = my_connect.cursor()
    query = f"INSERT INTO courses (user_id, course_id, course_name, notes_link, drive_link) VALUES (%s, %s, %s, %s, %s)"
    values = (1, 'CS101', 'Intro to Computer Science', 'https://notes.com/cs101', 'https://drive.com/cs101')
    my_cursor.execute(query, values)

    my_connect.commit()

    print(my_cursor.rowcount, "record inserted.")

def get_user(USER_ID):
    my_connect = mysql.connector.connect(
    host="35.226.41.35",
    user="root",
    passwd="ONTIME123",
    database="main_db"
    )
    ####### end of connection details ####

    my_cursor = my_connect.cursor()
    query = f"SELECT * FROM user_info WHERE canvas_user_id = {USER_ID}"
    return my_cursor.execute(query)

for course in courses:
        try:
            if ((course.name).find("SP23") > -1):
                assignments = course.get_assignments()
                for assignment in assignments:
                    insert_assignments(assignment.id, course.id, assignment.name, assignment.due_at, API_URL, "google_docs_id")
                    gh.new_assignemnt(course.name, assignment.name)
        except AttributeError:
            pass

course1 = canvas.get_course(6327379)
assignment1 = course1.get_assignment(35995341)

if __name__ == "__main__":
    # gh.createDirectory("course1")
    # gh.setDirectory("course1")
    # gh.createDoc("Assignment1")
    # gh.showCurrentDirectory()
    # gh.updateDoc("Assignment1")
    # gh.export_pdf("Assignment1")
    # google_submit(course1, assignment1, gh.query("Assignment1"), "Assignment1.pdf")
    # local_submit(course1, assignment1, localDocumentName)
    insert_user_info()
    print("Done")