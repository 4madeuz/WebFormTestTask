from flask import Flask, request, jsonify
from pymongo import MongoClient
import re
from datetime import datetime

app = Flask(__name__)
client = MongoClient('mongo', 27017)  # Имя хоста соответствует имени сервиса в docker-compose.yml
db = client['form_templates']
templates = db['templates']


class Validator():
    # Валидация email
    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    # Валидация телефона
    def validate_phone(self, phone):
        pattern = r'^\+\d{1,2}\s\d{3}\s\d{3}\s\d{2}\s\d{2}$'
        return bool(re.match(pattern, phone))

    # Валидация даты
    def validate_date(self, date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            try:
                datetime.strptime(date, '%d.%m.%Y')
                return True
            except ValueError:
                return False

    # Функция для валидации формы
    def validate_form(self, template, form_data):
        print(form_data.keys())
        print(template)
        for key in form_data.keys():
            if template[key] == 'date' and self.validate_date(form_data[key]) is False:
                return False
            elif template[key] == 'phone' and self.validate_phone(form_data[key]) is False:
                return False
            elif template[key] == 'email' and self.validate_email(form_data[key]) is False:
                return False
        print('True')
        return True

    def determine_types(self, elements):
        type_dict = {}

        for element in elements:
            if self.validate_date(element):
                type_dict[element] = 'date'
            elif self.validate_phone(element):
                type_dict[element] = 'phone'
            elif self.validate_email(element):
                type_dict[element] = 'email'
            else:
                type_dict[element] = 'text'

        return type_dict


def check_lists(list1, list2):

    for element in list1:
        if element not in list2:
            return False

    return True


@app.route('/get_form', methods=['POST'])
def get_form():
    form_data = request.form.to_dict()
    validator = Validator()
    print(templates.count_documents({}))
    for template in templates.find():
        if check_lists(form_data.keys(), template.keys()):
            if validator.validate_form(template, form_data):
                return jsonify({'form_name': template['form_name']})
    return jsonify(**validator.determine_types(form_data.keys()))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    db = client['form_templates']
    templates = db['templates']
    templates.delete_many({})
    # Пример данных в базе
    results = templates.insert_many([
        {
            "form_name": "MyForm",
            "user_name": "text",
            "email": "email"
        },
        {
            "form_name": "OrderForm",
            "user_name": "text",
            "order_date": "date",
            "phone": "phone"
        },
        {
            "form_name": "AnotherForm",
            "user_name": "text",
            "phone": "phone",
            "email": "email",
            "order_date": "date"
        },
        {
            "form_name": "ContactForm",
            "user_name": "text",
            "full_name": "text",
            "phone": "phone",
            "email": "email",
            "order_date": "date"
        }
    ])
