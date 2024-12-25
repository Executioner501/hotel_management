from flask import Flask, request, jsonify, send_from_directory
import psycopg2
import os

app = Flask(__name__)

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
def chef_page():
    return send_from_directory(html_folder, 'chef.html')  # Serving chef page

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
        cursor.close()

if __name__ == '__main__':
    app.run(debug=True)
