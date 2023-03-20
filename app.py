from flask import Flask, request, make_response
import mysql.connector

app = Flask(__name__)

@app.route('/customers', methods=['GET'])
def get_customers():
    try:
        conn = mysql.connector.connect(user='lab3user', password='lab3password',
                                        host='127.0.0.1',
                                        database='lab3cust')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customer')
        customer_list = []
        for CustomerID, Gender, Age, AnnualIncome, SpendingScore, Profession, WorkExperience, FamilySize in cursor:
            customer = {}
            customer['CustomerID'] = CustomerID
            customer['Gender'] = Gender
            customer['Age'] = Age
            customer['AnnualIncome'] = AnnualIncome
            customer['SpendingScore'] = SpendingScore
            customer['Profession'] = Profession
            customer['WorkExperience'] = WorkExperience
            customer['FamilySize'] = FamilySize
            customer_list.append(customer)
        cursor.close()
        conn.close()
        return make_response(customer_list, 200)
    except:
        return make_response({'error': "An errored occurred while getting customers"}, 400)


@app.route('/customer/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    try:
        conn = mysql.connector.connect(user='lab3user', password='lab3password',
                                        host='127.0.0.1',
                                        database='lab3cust')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM customer WHERE CustomerID={customer_id}')
        row = cursor.fetchone()
        customer = {}
        if row is not None:
            CustomerID, Gender, Age, AnnualIncome, SpendingScore, Profession, WorkExperience, FamilySize = row
            customer = {}
            customer['CustomerID'] = CustomerID
            customer['Gender'] = Gender
            customer['Age'] = Age
            customer['AnnualIncome'] = AnnualIncome
            customer['SpendingScore'] = SpendingScore
            customer['Profession'] = Profession
            customer['WorkExperience'] = WorkExperience
            customer['FamilySize'] = FamilySize
            cursor.close()
            conn.close()
        return make_response(customer, 200)
    except:
        return make_response({'error': "An errored occurred while getting customer"}, 400)


@app.route('/add_customer', methods=['POST'])
def add_customer():
    try:
        conn = mysql.connector.connect(user='lab3user', password='lab3password',
                                        host='127.0.0.1',
                                        database='lab3cust')
        cursor = conn.cursor()
        content = request.json
        
        CustomerID = content['CustomerID']
        Gender = content['Gender']
        Age = content['Age']
        AnnualIncome = content['AnnualIncome']
        SpendingScore = content['SpendingScore']
        Profession = content['Profession']
        WorkExperience = content['WorkExperience']
        FamilySize = content['FamilySize']
        cursor.execute(f"INSERT INTO customer VALUES ('{CustomerID}', '{Gender}', '{Age}', '{AnnualIncome}', '{SpendingScore}', '{Profession}', '{WorkExperience}', '{FamilySize}')")
        conn.commit()
        cursor.close()
        conn.close()
        return make_response({'success': "Customer successfully added!"}, 200)
    except:
        return make_response({'error': "An errored occurred while adding customer"}, 400)


@app.route('/update_profession/<customer_id>', methods=['PUT'])
def update_profession(customer_id):
    try:
        conn = mysql.connector.connect(user='lab3user', password='lab3password',
                                        host='127.0.0.1',
                                        database='lab3cust')
        cursor = conn.cursor()
        content = request.json
        Profession = content['Profession']
        cursor.execute(f"UPDATE customer SET Profession = '{Profession}' WHERE CustomerID={customer_id}")
        conn.commit()
        cursor.close()
        conn.close()
        return make_response({'success': "Customer Profession successfully updated!"}, 202)
    except:
        return make_response({'error': "An errored occurred while updating customer profession"}, 400)


@app.route('/highest_income_report', methods=['GET'])
def get_highest_income():
    try:
        conn = mysql.connector.connect(user='lab3user', password='lab3password',
                                        host='127.0.0.1',
                                        database='lab3cust')
        cursor = conn.cursor()
        cursor.execute(f"SELECT CustomerID, max(AnnualIncome) AS AnnualIncome, Profession FROM lab3cust.customer GROUP BY Profession;")
        customer_list = []
        for CustomerID, AnnualIncome, Profession in cursor:
            customer = {}
            customer['CustomerID'] = CustomerID
            customer['AnnualIncome'] = AnnualIncome
            customer['Profession'] = Profession
            customer_list.append(customer)
        cursor.close()
        conn.close()
        return make_response(customer_list, 200)
    except:
        return make_response({'error': "An errored occurred while getting highest income by profession"}, 400)


@app.route('/total_income_report', methods=['GET'])
def get_total_income():
    try:
        conn = mysql.connector.connect(user='lab3user', password='lab3password',
                                        host='127.0.0.1',
                                        database='lab3cust')
        cursor = conn.cursor()
        cursor.execute(f"SELECT sum(AnnualIncome) AS TotalIncome, Profession FROM lab3cust.customer GROUP BY Profession;")
        customer_list = []
        for TotalIncome, Profession in cursor:
            customer = {}
            customer['TotalIncome'] = TotalIncome
            customer['Profession'] = Profession
            customer_list.append(customer)
        cursor.close()
        conn.close()
        return make_response(customer_list, 200)
    except:
        return make_response({'error': "An errored occurred while getting total income by profession"}, 400)


@app.route('/average_work_experience', methods=['GET'])
def get_average_experience():
    try:
        conn = mysql.connector.connect(user='lab3user', password='lab3password',
                                        host='127.0.0.1',
                                        database='lab3cust')
        cursor = conn.cursor()
        cursor.execute(f"SELECT Round(avg(WorkExperience),0) AS AverageExperience, Profession FROM lab3cust.customer WHERE AnnualIncome > 50000 AND Age < 35 GROUP BY Profession;")
        customer_list = []
        for AverageExperience, Profession in cursor:
            customer = {}
            customer['AverageExperience'] = AverageExperience
            customer['Profession'] = Profession
            customer_list.append(customer)
        cursor.close()
        conn.close()
        return make_response(customer_list, 200)
    except:
        return make_response({'error': "An errored occurred while getting average experience by profession"}, 400)


@app.route('/average_spending_score/<profession>', methods=['GET'])
def get_average_spending_score(profession):
    try:
        conn = mysql.connector.connect(user='lab3user', password='lab3password',
                                        host='127.0.0.1',
                                        database='lab3cust')
        cursor = conn.cursor()
        cursor.execute(f"SELECT Round(avg(SpendingScore),0) AS AverageSpendingScore, Gender FROM lab3cust.customer WHERE Profession = '{profession}' GROUP BY Gender;")
        customer_list = []
        for AverageSpendingScore, Gender in cursor:
            customer = {}
            customer['AverageSpendingScore'] = AverageSpendingScore
            customer['Gender'] = Gender
            customer_list.append(customer)
        cursor.close()
        conn.close()
        return make_response(customer_list, 200)
    except:
        return make_response({'error': "An errored occurred while getting average spending score for profession"}, 400)


if __name__ == '__main__':
    app.run()

