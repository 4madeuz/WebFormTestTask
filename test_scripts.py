import requests
import re
from datetime import datetime

url = "http://localhost:5000/get_form"

# Тестовые данные для корректных запросов
data1 = {'user_name': 'John Doe', 'order_date': '2022-01-01', 'phone': '+7 999 888 77 66'}
data2 = {'user_name': 'Jane Smith', 'email': 'jane@example.com'}
data3 = {'user_name': 'Alice Wonderland', 'phone': '+7 987 654 32 10', 'order_date': '2022-01-01'}
data4 = {'user_name': 'Bob Builder', 'email': 'bob@example.com', 'order_date': '10.12.2022'}
data5 = {'user_name': 'Charlie Chaplin', 'email': 'charlie@example.com', 'phone': '+7 111 222 33 44', 'order_date': '2021-08-20'}

# Тестовые данные для некорректных запросов
invalid_data1 = {'user_name': 'Invalid User', 'email': 'invalid_email'}  # Некорректный email
invalid_data2 = {'user_name': 'Invalid Order', 'phone': 'invalid_phone'}  # Некорректный телефон
invalid_data3 = {'user_name': 'Invalid Date', 'order_date': 'invalid_date'}  # Некорректная дата

# Отправка POST-запросов
response1 = requests.post(url, data=data1)
response2 = requests.post(url, data=data2)
response3 = requests.post(url, data=data3)
response4 = requests.post(url, data=data4)
response5 = requests.post(url, data=data5)

# Отправка POST-запросов с некорректными данными
invalid_response1 = requests.post(url, data=invalid_data1)
invalid_response2 = requests.post(url, data=invalid_data2)
invalid_response3 = requests.post(url, data=invalid_data3)

# Вывод результатов
print("Response 1 (Valid):", response1.json())
print("Response 2 (Valid):", response2.json())
print("Response 3 (Valid):", response3.json())
print("Response 4 (Valid):", response4.json())
print("Response 5 (Valid):", response5.json())

print("Response 6 (Invalid):", invalid_response1.json())
print("Response 7 (Invalid):", invalid_response2.json())
print("Response 8 (Invalid):", invalid_response3.json())


def validate_phone(phone):
    pattern = r'^\+\d{1,2}\s\d{3}\s\d{3}\s\d{2}\s\d{2}$'
    return bool(re.match(pattern, phone))

# Валидация даты
def validate_date( date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        try:
            datetime.strptime(date, '%d.%m.%Y')
            return True
        except ValueError:
            return False

print(validate_date('10.12.2022'))
print(validate_phone('+7 999 888 77 66'))