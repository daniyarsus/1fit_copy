import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJzdHJpbmciLCJlbWFpbCI6InVzZXJAZXhhbXBsZS5jb20iLCJwaG9uZSI6ODc3NTcxMTE4NDUsImV4cCI6MzkwMzU4OTU2ODl9.vdxlXhrkl7s-AJvuO7FPMg9Hi-55QzrFYNzaYI5K3lE"

# Заголовок запроса с токеном JWT
headers = {
    "Authorization": f"Bearer {token}"
}


# URL защищенного эндпоинта
url = "http://127.0.0.1:8000/api/v1/protected"

# Отправка запроса POST к защищенному эндпоинту с использованием токена JWT и отправкой JSON данных
response = requests.get(url, headers=headers)

print(response.json(), response.status_code)
