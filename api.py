from flask import Flask, jsonify
from config.connection import db, hello_string
import datetime
import decimal
app = Flask(__name__)

"""
Painful learning:

TODO: factor out logic for dealing with dates and decimals and any other thing that may arise

"""



@app.route('/')
def home():
    return jsonify("welcome to here")


# get all offices
# get all orders
# get all orderdetails
# get all payments
# get all productlines
# get all customers

@app.route('/api/employees')
def employees() -> list:
    """Getting all the employees details
    :return: json object of employees
    """
    sql = "SELECT * FROM employees"
    db.execute(sql)
    employees_tuple: tuple = db.fetchall()

    header_data = []
    for header in db.description:
        print(header[0])
        header_data.append(header[0])

    new_data = []
    for employee in employees_tuple:
        new_data.append(dict(zip(header_data, employee)))

    return jsonify(new_data)


@app.route('/api/offices')
def offices() -> list:
    sql = "SELECT * FROM offices"
    db.execute(sql)
    offices_tuple: tuple = db.fetchall()

    header_data = []
    for header in db.description:
        header_data.append(header[0])

    new_data = []
    for office in offices_tuple:
        new_data.append(dict(zip(header_data, office)))

    return jsonify(new_data)


@app.route('/api/products')
def products() -> list:
    sql = "SELECT * FROM products"
    db.execute(sql)
    products_tuple: tuple = db.fetchall()

    header_data = []
    for header in db.description:
        header_data.append(header[0])

    new_data = []
    for product in products_tuple:
        new_data.append(dict(zip(header_data, product)))

    return jsonify(new_data)


@app.route('/api/customers')
def customers() -> list:
    sql = "SELECT * FROM customers"
    db.execute(sql)
    customers_tuple: tuple = db.fetchall()

    header_data = []
    for header in db.description:
        header_data.append(header[0])

    new_data = []
    for customer in customers_tuple:
        new_data.append(dict(zip(header_data, customer)))

    return jsonify(new_data)


@app.route('/api/orders')
def orders() -> list:
    sql = "SELECT * FROM orders"
    db.execute(sql)
    orders_tuple: tuple = db.fetchall()

    header_data = []
    for header in db.description:
        header_data.append(header[0])

    new_data = []
    for order in orders_tuple:
        new_data.append(dict(zip(header_data, order)))

    return jsonify(new_data)


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

    order_details = []
    for order in orders_det:
        order_details.append(dict(zip(header_data, order)))

    return jsonify(order_details)


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


# for a customer get all orders
# for a given order get its details
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
