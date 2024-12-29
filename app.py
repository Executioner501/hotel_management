from flask import Flask, request, jsonify, send_from_directory
import psycopg2
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="hotel_management",  # Replace with your DB name
    user="postgres",              # Replace with your PostgreSQL username
    password="171523"             # Replace with your PostgreSQL password
)

# Define the path to the HTML files
html_folder = os.path.join(os.getcwd())  # Current working directory

@app.route('/')
def index():
    return send_from_directory(html_folder, 'index.html')  # Serving main page (home)

@app.route('/chef')
def branch_page():
    return send_from_directory(html_folder, 'chef.html')  # Serving chef page
@app.route('/branch')
def chef_page():
    return send_from_directory(html_folder, 'branch.html')  # Serving branch page

# Route to retrieve chef data based on branch_id
@app.route('/get-chefs', methods=['GET'])
def get_chefs():
    try:
        branch_id = request.args.get('branch_id')
        query = "SELECT * FROM CHEF"
        cursor = conn.cursor()

        if branch_id:
            query += " WHERE ssn IN (SELECT chef_ssn FROM CHEF_ASSIGNMENT WHERE branch_id = %s)"
            cursor.execute(query, (branch_id,))
        else:
            cursor.execute(query)
        
        rows = cursor.fetchall()
        chefs = [{"ssn": row[0], "name": row[1], "join_date": row[2], "specialty_cuisine": row[3]} for row in rows]
        return jsonify(chefs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        
            cursor.close()  # Ensure cursor is closed properly

@app.route('/get-all-chefs', methods=['GET'])
def get_all_chefs():
    try:
        query = "SELECT * FROM CHEF"  # Fetch all chefs
        cursor = conn.cursor()
        cursor.execute(query)
        
        rows = cursor.fetchall()
        chefs = [
            {"ssn": row[0], "name": row[1], "join_date": row[2], "specialty_cuisine": row[3]}
            for row in rows
        ]
        return jsonify(chefs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        
            cursor.close()

@app.route('/add-chef', methods=['POST'])
def add_chef():
    try:
        data = request.json  # Expecting JSON input
        cursor = conn.cursor()
        sql_query = """
            INSERT INTO CHEF (ssn, name, join_date, specialty_cuisine)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_query, (data['ssn'], data['name'], data['join_date'], data['specialty_cuisine']))
        conn.commit()
        return jsonify({"message": "Chef added successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
       
            cursor.close()

@app.route('/get-unassigned-chefs', methods=['GET'])
def get_unassigned_chefs():
    try:
        query = """
            SELECT ssn, name FROM CHEF
            WHERE ssn NOT IN (SELECT chef_ssn FROM CHEF_ASSIGNMENT)
        """
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        chefs = [{"ssn": row[0], "name": row[1]} for row in rows]
        return jsonify(chefs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        
            cursor.close()

@app.route('/assign-chef', methods=['POST'])
def assign_chef():
    try:
        data = request.json
        ssn = data['ssn']
        branch_id = data['branch_id']
        
        if not ssn or not branch_id:
            return jsonify({"error": "SSN and Branch ID are required"}), 400
        
        cursor = conn.cursor()
        sql_query = """
            INSERT INTO CHEF_ASSIGNMENT (chef_ssn, branch_id)
            VALUES (%s, %s)
        """
        cursor.execute(sql_query, (ssn, branch_id))
        conn.commit()
        
        return jsonify({"message": "Chef assigned successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        
            cursor.close()

if __name__ == '__main__':
    app.run(debug=True)
