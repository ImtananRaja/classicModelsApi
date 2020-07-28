from flask import Flask, jsonify
from config.connection import db, res

app = Flask(__name__)

"""
Painful learning
"""


@app.route('/')
def home():
    return jsonify("welcome to here")


@app.route('/api/employees')
def employees():
    "This will be the simple documentation for the api"
    sql = "SELECT * FROM employees"
    db.execute(sql)
    res = db.fetchall()
    newRes = []
    for item in res:
        newRes.append(item)
    return jsonify(newRes)


"""
Get Employee details

@params:
1) Employee Number - should be unique

@returns:
1) Dictionary with employee details
"""


@app.route('/api/employee/<int:emp_num>')
def get_employee_det(emp_num):
    sql = "SELECT * FROM employees WHERE employeeNumber = %s"
    db.execute(sql, emp_num)
    result = db.fetchone()
    description = db.description
    header_data = []
    for item in description:
        header_data.append(item[0])
    final_data = dict(zip(tuple(header_data), result))
    print(final_data)
    return jsonify(final_data)


"""
Get all Customers for an Employee

@param:
1) Employee Number - should be unique

@returns:
1) List of Customers details for the employee
"""
@app.route('/api/employee/<int:emp_num>/customers')
def get_employee_customers(emp_num):
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

    return jsonify(res)
    #final_data = dict(zip(tuple(header_data), result))
    #print(final_data)
    #return "heleo"


# get all employees
# get all offices
# get all orders
# get all orderdetails
# get all payments
# get all products
# get all productlines
# get all customers


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
