import mimetypes

import requests


def upload_audio(file_path, token, transcript):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "application/octet-stream"
    upload_url = "https://topshur-backend.onrender.com/upload-audio"
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file, mime_type)}
        data = {"transcript": transcript}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(upload_url, files=files, data=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print("Response JSON:", response.json())


def register(username, password, disorder):
    url = "https://topshur-backend.onrender.com/register"
    user_data = {"username": username, "password": password, "disorder": disorder}
    response = requests.post(url, json=user_data)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:", response.json())
    print(response.json().get("access_token"))


def login(username, password):
    login_url = "https://topshur-backend.onrender.com/login/token"
    login_data = {"username": username, "password": password}
    login_response = requests.post(login_url, data=login_data)
    token = login_response.json().get("access_token")
    print(token)


def add_disorder(username, disorder):
    url = "https://topshur-backend.onrender.com/add_disorder"
    disorder_data = {"username": username, "disorder": disorder}
    response = requests.post(url, json=disorder_data)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:", response.json())


# register("username", "password", "disorder")

# upload_audio(
#     "audio_file_path",
#     "login_token",
#     "transcript_text",
# )
# login("username", "password")

# add_disorder("username", "sohuf")
