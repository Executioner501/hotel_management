from flask import Flask, request, jsonify, send_from_directory
import psycopg2
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="HotelManagement",  # Replace with your DB name
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
    cursor = None  # Initialize cursor to None
    try:
        data = request.json
        assignment_id = data.get('assignment_id')  # Assignment ID
        branch_id = data.get('branch_id')          # Branch ID
        chef_ssn = data.get('chef_ssn')            # Chef SSN
        start_date = data.get('start_date')        # Start Date
        end_date = None  # Handle end_date as None

        # Validate required inputs
        if not assignment_id or not branch_id or not chef_ssn or not start_date:
            return jsonify({"error": "assignment_id, branch_id, chef_ssn, and start_date are required"}), 400

        cursor = conn.cursor()
        
        # Insert into CHEF_ASSIGNMENT
        sql_query = """
            INSERT INTO CHEF_ASSIGNMENT (assignment_id, branch_id, chef_ssn, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql_query, (assignment_id, branch_id, chef_ssn, start_date, end_date))
        conn.commit()

        return jsonify({"message": "Chef assigned successfully!"})
    except Exception as e:
        print(f"Error in assign_chef: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:  # Ensure cursor exists before closing
            cursor.close()


@app.route('/branch-menu', methods=['GET'])
def branch_menu():
    branch_id = request.args.get('branch_id')  # Correct parameter name here
    if not branch_id:
        return jsonify({"error": "Branch ID is required"}), 400
    
    query = """
        SELECT m.menu_name, d.name, d.price
        FROM MENU_CARD m
        JOIN DISH d ON m.menu_id = d.menu_id
        WHERE m.branch_id = %s
    """
    cursor = conn.cursor()
    try:
        cursor.execute(query, (branch_id,))
        rows = cursor.fetchall()

        menus = {}
        for menu_name, dish_name, price in rows:
            if menu_name not in menus:
                menus[menu_name] = []
            menus[menu_name].append({"name": dish_name, "price": price})  # Keep price as numeric
        return jsonify(menus)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@app.route('/get-branch-financials', methods=['GET'])
def get_branch_financials():
    try:
        b_fi = request.args.get('b_fin')  # 'b_fin' for branch financials

        if not b_fi:
            return jsonify({"error": "Branch ID is required"}), 400

        query = """
            SELECT record_date, actual_revenue, actual_expenditure, performance_notes
            FROM FINANCIAL_RECORD
            WHERE branch_id = %s
        """
        cursor = conn.cursor()
        cursor.execute(query, (b_fi,))
        rows = cursor.fetchall()

        if not rows:
            return jsonify({"error": "No financial records found for this branch"}), 404    

        financials = [
            {"record_date": row[0], "actual_revenue": row[1], "actual_expenditure": row[2], "performance_notes": row[3]}
            for row in rows
        ]
        return jsonify(financials)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()





if __name__ == '__main__':
    app.run(debug=True)
