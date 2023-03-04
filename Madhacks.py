from canvasapi import Canvas

API_URL = "https://canvas.wisc.edu/"
API_KEY = "<API_KEY>"

canvas = Canvas(API_URL, API_KEY)
user = canvas.get_user(<USER_ID>)
courses = canvas.get_courses()
print(courses[0])
