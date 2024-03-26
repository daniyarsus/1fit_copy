import requests


token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJiZWJyYTA0MDQwNSIsImVtYWlsIjoiYmVicmFAYmVicmEuY29tIiwicGhvbmUiOjg3Nzc4OTk5NDQ0LCJzZXNzaW9uX2lkIjoiNTZkMTdhMDAtMTlmMy00YTJjLTgxZTMtZWVmYzdiNTc2NmJhIiwiZXhwIjozOTAzNjE2OTg0MX0.MoeaAyWEXJUWooU3EwlOANFGOLeRHFjzVPpTcDV8dJw"


# Заголовок запроса с токеном JWT
headers = {
    "Authorization": f"Bearer {token}"
}


# URL защищенного эндпоинта
url = "http://127.0.0.1:8000/api/v1/logout/del-token"


json = {
    "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJiZWJyYTA0MDQwNSIsImVtYWlsIjoiYmVicmFAYmVicmEuY29tIiwicGhvbmUiOjg3Nzc4OTk5NDQ0LCJzZXNzaW9uX2lkIjoiNTZkMTdhMDAtMTlmMy00YTJjLTgxZTMtZWVmYzdiNTc2NmJhIiwiZXhwIjozOTAzNjE2OTg0MX0.MoeaAyWEXJUWooU3EwlOANFGOLeRHFjzVPpTcDV8dJw"
}


# Отправка запроса POST к защищенному эндпоинту с использованием токена JWT и отправкой JSON данных
response = requests.post(url=url, headers=headers, json=json)


print(response.json(), response.status_code)
