from flask import Flask, render_template, request, make_response

app = Flask(__name__)
application = app

# Определение маршрута для главной страницы
@app.route('/')
def index():
    # Получаем текущий URL запроса
    url = request.url
    # Возвращаем шаблон index.html с передачей URL в качестве аргумента
    return render_template('index.html', url=url)

# Определение маршрута для страницы с параметрами URL
@app.route('/args')
def args():
    # Возвращаем шаблон args.html
    return render_template('args.html')

# Определение маршрута для страницы с заголовками запроса
@app.route('/headers')
def headers():
    # Возвращаем шаблон headers.html
    return render_template('headers.html')

# Определение маршрута для страницы с куки
@app.route('/cookies')
def cookies():
    # Создаем ответ на запрос с использованием шаблона cookies.html
    response = make_response(render_template('cookies.html'))
    # Проверяем, есть ли куки 'username' в запросе
    if 'username' in request.cookies:
        # Если есть, удаляем куки 'username' из ответа
        response.delete_cookie(key='username')
    else:
        # Если нет, устанавливаем куки 'username' в 'student'
        response.set_cookie('username', 'student')
    # Проверяем, есть ли куки 'password' в запросе
    if 'password' in request.cookies:
        # Если есть, удаляем куки 'password' из ответа
        response.delete_cookie(key='password')
    else:
        # Если нет, устанавливаем куки 'password' в '12345678'
        response.set_cookie('password', '12345678')
    # Возвращаем ответ
    return response 

# Определение маршрута для страницы с формой отправки
@app.route('/form', methods=['get',"post"])
def form():
    # Возвращаем шаблон form.html
    return render_template('form.html')

# Определение маршрута для страницы с калькулятором
@app.route('/calculate', methods=['get',"post"])
def calculate():
    res = ""
    # Если метод запроса POST
    if request.method == "POST":
        # Проверяем, является ли number1 числом
        if not(request.form["number1"].isdigit()):
            msg = "Первое значение должно быть числом!"
            # Возвращаем шаблон calculate.html с сообщением об ошибке
            return render_template('calculate.html', msg=msg)
        # Проверяем, является ли number2 числом
        if not(request.form["number2"].isdigit()):
            msg = "Второе значение должно быть числом!"
            # Возвращаем шаблон calculate.html с сообщением об ошибке
            return render_template('calculate.html', msg=msg)
        # Получаем значения number1, number2 и operator из запроса
        a = int(request.form["number1"])
        b = int(request.form["number2"])
        operator = request.form["operator"]
        # Выполняем операцию в зависимости от оператора
        if operator == "+":
            res = a+b
        elif operator == "-":
            res = a-b
        elif operator == "*":
            res = a*b
        elif operator == "/":
            if b==0:
                msg = "Делить на 0 нельзя!"
                # Возвращаем шаблон calculate.html с сообщением об ошибке
                return render_template('calculate.html', msg=msg)
            res = a/b
    # Возвращаем шаблон calculate.html с результатом вычисления
    return render_template('calculate.html', res=res)
    
# Определение маршрута для страницы с проверкой номера телефона
@app.route('/check_phone_number', methods=['get',"post"])
def check_phone_number():
    # Если метод запроса GET
    if request.method == "GET": 
        # Возвращаем шаблон check_phone_number.html без сообщения
        return render_template("check_phone_number.html", msg = "0") 
    else: # Метод запроса POST
        # Получаем номер телефона из формы
        phone_number = request.form["check_number1"]
        # Список допустимых символов, кроме цифр
        acceptable_symbols_except_figures = [" ", "(", ")", ".", "+", "-"]
        # Проверка количества цифр в номере
        counter_of_figures = 0
        for i in phone_number:
            if i.isdigit():
                counter_of_figures += 1
        # Проверка, что количество цифр соответствует стандарту
        if counter_of_figures == 11:
            if not(phone_number[0] == "8" or phone_number[:2] == "+7"):
                return render_template("check_phone_number.html", msg = "1") 
        elif counter_of_figures == 10:
            if (phone_number[0] == "8" or phone_number[:2] == "+7"):
                return render_template("check_phone_number.html", msg = "1")
        else:
            return render_template("check_phone_number.html", msg = "1")
    # Проверка на допустимые символы
    for i in phone_number:
        if not(i in acceptable_symbols_except_figures or i.isdigit()):
            return render_template("check_phone_number.html", msg = "2")
    # Форматирование номера телефона
    formating_phone_nuber = phone_number
    if formating_phone_nuber[0] == '+':
        formating_phone_nuber = formating_phone_nuber.replace('+7', '8', 1)
    if formating_phone_nuber[0] != '8':
        formating_phone_nuber = '8' + formating_phone_nuber
    formating_phone_nuber = formating_phone_nuber.replace('(', '')
    formating_phone_nuber = formating_phone_nuber.replace(')', '')
    formating_phone_nuber = formating_phone_nuber.replace(' ', '')
    formating_phone_nuber = formating_phone_nuber.replace('.', '')
    formating_phone_nuber = formating_phone_nuber.replace('-', '')
    formating_phone_nuber = formating_phone_nuber.replace('+', '')
    formating_phone_nuber = formating_phone_nuber[0] + '-' + formating_phone_nuber[1:4] + '-' + formating_phone_nuber[4:7] + '-' + formating_phone_nuber[7:9] + '-' + formating_phone_nuber[9:]
    # Возвращаем шаблон check_phone_number.html с результатом проверки
    return render_template("check_phone_number.html", msg = "3", phone_number = formating_phone_nuber)

if __name__ == "__main__":
    app.run(debug=True)
