from flask import Flask, jsonify, request, abort, redirect, url_for
from config.connection import db
import datetime
import decimal
from functools import wraps

app = Flask(__name__)

"""
Painful learning:

TODO: factor out logic for dealing with dates and decimals and any other thing that may arise

"""


# The actual decorator function
def require_app_api_key(view_function):
    """
    Decorator function to authenticate the api request with valid key
    :param view_function:
    :return:
    """

    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        print(request.headers)
        # get the key from the database if exists ( using the value passed from the headers 'x-api-key' )
        # check if the key is also valid and not suspended
        # if suspended then abort on the request
        # if not valid then reroute to get new key
        # NOTE: everytime this is called update the api key table to set the keys to invalid which pass the expiry_date
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == 'GETKEYFROMDB':
            return view_function(*args, **kwargs)
        else:
            #return redirect('/api/api_key') or
            return redirect(url_for('api_key'))
            #abort(401)

    return decorated_function


@app.route('/')
@require_app_api_key
def home():
    return jsonify("welcome to the classic models api")


@app.route('/api/api_key')
def api_key():
    return "Randomly generated API_KEY"



@app.route('/api/payments')
def payments() -> list:
    """Getting all the payments details
    :return: json object of payments
    """
    sql = "SELECT * FROM payments"
    db.execute(sql)
    payments_list: list = list(db.fetchall())

    header_data = []
    for header in db.description:
        header_data.append(header[0])

    all_payments_data = []
    for payment in payments_list:
        payment_list: list = list(payment)

        for index, item in enumerate(payment_list):
            if isinstance(item, decimal.Decimal):
                payment_list[index]: str = str(item)
            if isinstance(item, datetime.date):
                payment_list[index]: str = item.strftime("%d/%m/%Y")
        all_payments_data.append(dict(zip(header_data, payment_list)))

    return jsonify(all_payments_data)


@app.route('/api/productlines')
def product_lines() -> list:
    """Getting all the product lines details
    :return: json object of product lines
    """
    sql = "SELECT * FROM productlines"
    db.execute(sql)
    product_lines_list: list = list(db.fetchall())

    header_data = []
    for header in db.description:
        header_data.append(header[0])

    all_product_line_data = []
    for product_line in product_lines_list:
        all_product_line_data.append(dict(zip(header_data, product_line)))

    return jsonify(all_product_line_data)


@app.route('/api/employees')
def employees() -> list:
    """Getting all the employees details
    :return: json object of employees
    """
    sql = "SELECT * FROM employees"
    db.execute(sql)
    employees_list: list = list(db.fetchall())

    header_data = []
    for header in db.description:
        header_data.append(header[0])

    all_employees_data = []
    for employee in employees_list:
        all_employees_data.append(dict(zip(header_data, employee)))

    return jsonify(all_employees_data)


@app.route('/api/offices')
def offices() -> list:
    sql = "SELECT * FROM offices"
    db.execute(sql)
    offices_list: list = list(db.fetchall())

    header_data = []
    for header in db.description:
        header_data.append(header[0])

    all_offices_data = []
    for office in offices_list:
        all_offices_data.append(dict(zip(header_data, office)))

    return jsonify(all_offices_data)


@app.route('/api/products')
def products() -> list:
    sql = "SELECT * FROM products"
    db.execute(sql)
    products_list: list = list(db.fetchall())

    header_data = []
    for header in db.description:
        header_data.append(header[0])

    all_products_data = []
    for product in products_list:
        all_products_data.append(dict(zip(header_data, product)))

    return jsonify(all_products_data)


@app.route('/api/orderdetails')
def order_details() -> list:
    sql = "SELECT * FROM orderdetails"
    db.execute(sql)
    orders_list: list = list(db.fetchall())

    header_data = []
    for header in db.description:
        header_data.append(header[0])

    all_orders_data = []
    for order_detail in orders_list:
        all_orders_data.append(dict(zip(header_data, order_detail)))

    return jsonify(all_orders_data)


@app.route('/api/customers')
def customers() -> list:
    sql = "SELECT * FROM customers"
    db.execute(sql)
    customers_list: list = list(db.fetchall())

    header_data = []
    for header in db.description:
        header_data.append(header[0])

    all_customers_data = []
    for customer in customers_list:
        all_customers_data.append(dict(zip(header_data, customer)))

    return jsonify(all_customers_data)


@app.route('/api/orders')
def orders() -> list:
    sql = "SELECT * FROM orders"
    db.execute(sql)
    orders_list: list = list(db.fetchall())

    header_data = []
    for header in db.description:
        header_data.append(header[0])

    all_orders_data = []
    for order_item in orders_list:
        all_orders_data.append(dict(zip(header_data, order_item)))

    return jsonify(all_orders_data)


@app.route('/api/order/<int:order_num>')
def order(order_num) -> dict:
    sql = "SELECT * FROM orders WHERE orderNumber = %s"
    db.execute(sql, order_num)
    order_data: list = list(db.fetchone())

    # basically convert datetime.date to human readable form
    for index, item in enumerate(order_data):
        if isinstance(item, datetime.date):
            order_data[index]: str = item.strftime("%d/%m/%Y")

    header_data = []
    for header in db.description:
        header_data.append(header[0])

    final_data = dict(zip(header_data, order_data))
    return jsonify(final_data)


@app.route('/api/order/<int:order_num>/details')
def order_det(order_num) -> dict:
    sql = """
    SELECT * FROM orderdetails WHERE orderNumber = %s
    """
    db.execute(sql, order_num)
    orders_det: list = list(db.fetchall())

    header_data = []
    for header in db.description:
        header_data.append(header[0])

    order_details_list = []
    for order_item in orders_det:
        order_details_list.append(dict(zip(header_data, order_item)))

    return jsonify(order_details_list)


"""
Get Employee details

@params:
1) Employee Number - should be unique

@returns:
1) Dictionary with employee details
"""


@app.route('/api/employee/<int:emp_num>')
def get_employee_det(emp_num) -> dict:
    """
    returns json object of employee details
    :param emp_num: int
    :return: json object of employee details
    """
    sql = "SELECT * FROM employees WHERE employeeNumber = %s"
    db.execute(sql, emp_num)
    employee_details: tuple = db.fetchone()
    header_data = []
    for header in db.description:
        header_data.append(header[0])
    final_data = dict(zip(tuple(header_data), employee_details))
    return jsonify(final_data)


"""
Get all Customers for an Employee

@param:
1) Employee Number - should be unique

@returns:
1) List of Customers details for the employee
"""


@app.route('/api/employee/<int:emp_num>/customers')
def get_employee_customers(emp_num) -> list:
    sql = """
    SELECT customers.* 
    FROM customers 
    LEFT JOIN employees ON salesRepEmployeeNumber = employees.employeeNumber
    WHERE employeeNumber = %s"""
    db.execute(sql, emp_num)
    customers_data = list(db.fetchall())
    description = db.description

    header_data = []
    for item in description:
        header_data.append(item[0])

    new_data = []
    for customer_list in customers_data:
        customer_list = list(customer_list)
        for index, item in enumerate(customer_list):
            if isinstance(item, decimal.Decimal):
                customer_list[index] = str(item)
        new_data.append(dict(zip(header_data, customer_list)))

    return jsonify(new_data)


@app.route('/api/customer/<int:customer_num>/orders')
def get_customer_orders(customer_num) -> list:
    """
    Get all orders for an customer given a customer number
    :params customer_num: int
    :returns json list of dicts
    """
    sql = """
    SELECT orders.* 
    FROM orders 
    LEFT JOIN customers ON customers.customerNumber = orders.customerNumber
    WHERE customers.customerNumber = %s"""
    db.execute(sql, customer_num)
    customers_orders = list(db.fetchall())
    description = db.description

    header_data = []
    for item in description:
        header_data.append(item[0])

    new_data = []
    for order_list in customers_orders:
        order_list: list = list(order_list)

        for index, item in enumerate(order_list):
            if isinstance(item, decimal.Decimal):
                order_list[index]: str = str(item)
            if isinstance(item, datetime.date):
                order_list[index]: str = item.strftime("%d/%m/%Y")

        new_data.append(dict(zip(header_data, order_list)))

    return jsonify(new_data)

# for an office get all employees
# for an employee get all the sales they've made
# for a given employee get all its superiors and subordinates

#


# @app.route('/api/cards/')
# def api_card_list():
#     return jsonify(db)
#
#
# @app.route('/api/card/<int:index>')
# def api_card_detail(index):
#     try:
#         return db[index]
#     except IndexError:
#         abort(404)


# def row2dict(row):
#     d = {}
#     for column in row.__table__.columns:
#         print(row)
#         print(column)
#         d[row.employeeNumber] = row.firstName
#         d[row.employeeNumber] = row.lastName
#
#     return d
