import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwidXNlcm5hbWUiOiJzdHJpbmciLCJlbWFpbCI6ImtvdGUuZGFuaTAyQGdtYWlsLmNvbSIsInBob25lIjo4ODg4NzY2NjU1NSwic2Vzc2lvbl9pZCI6IjA3NDcyZjkxLTQ3ZDYtNDM1My1iNDUwLTQ3MzRmYTkyZWJhMSIsImV4cCI6MzkwMzU5NTMzMzZ9.NbbLl2yaIBcSgsd7EterOhXbMaQmjQgCmAm6_YdlgLk"

# Заголовок запроса с токеном JWT
headers = {
    "Authorization": f"Bearer {token}"
}


# URL защищенного эндпоинта
url = "http://127.0.0.1:8000/api/v1/protected"

# Отправка запроса POST к защищенному эндпоинту с использованием токена JWT и отправкой JSON данных
response = requests.get(url, headers=headers)

print(response.json(), response.status_code)
