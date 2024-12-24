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

# Cursor for executing queries
cursor = conn.cursor()

# Define the path to your HTML files
html_folder = os.path.join(os.getcwd())  # Current working directory

@app.route('/')
def serve_html():
    return send_from_directory(html_folder, 'index.html')  # Replace 'index.html' with your HTML file name

@app.route('/get-chefs', methods=['GET'])
def get_chefs():
    try:
        # Execute a query to fetch all chefs
        cursor.execute("SELECT * FROM chef;")
        rows = cursor.fetchall()
        # Convert the result to a list of dictionaries
        chefs = [{"ssn": row[0], "name": row[1], "join_date": row[2], "specialty_cuisine": row[3]} for row in rows]
        return jsonify(chefs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/get-branches', methods=['GET'])
def get_branches():
    try:
        # Execute a query to fetch all branches
        cursor.execute("SELECT branch_id, name, city, state, start_date, planned_revenue, planned_expenditure FROM HOTEL_BRANCH;")
        rows = cursor.fetchall()
        # Convert the result to a list of dictionaries
        branches = [
            {
                "branch_id": row[0],
                "name": row[1],
                "city": row[2],
                "state": row[3],
                "start_date": row[4],
                "planned_revenue": float(row[5]) if row[5] else None,
                "planned_expenditure": float(row[6]) if row[6] else None
            }
            for row in rows
        ]
        return jsonify(branches)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)
