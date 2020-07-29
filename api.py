from flask import Flask, jsonify
from config.connection import db, hello_string

app = Flask(__name__)

"""
Painful learning
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
def order_det(order_num) -> list:
    sql = """
    SELECT orderdetails.* 
    FROM orderdetails
    LEFT JOIN orders ON orders.orderNumber = orderdetails.orderNumber
    LEFT JOIN 
    WHERE orderdetails.orderNumber = %s
    """
    db.execute(sql, order_num)
    order_details_tuple: tuple = db.fetchall()
    print(order_details_tuple)

    return jsonify("Someting")


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
    result = db.fetchall()
    description = db.description
    header_data = []
    for item in description:
        header_data.append(item[0])
    new_data = []
    for resp in result:
        deref_decimal: str = str(resp[-1])
        resp: list = list(resp[:-1])
        resp.append(deref_decimal)
        new_data.append(dict(zip(header_data, resp)))

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
