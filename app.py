from flask import Flask, jsonify, send_file, make_response
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import Config
import io

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for the app
CORS(app)

# Initialize MySQL
mysql = MySQL(app)

# Define a route for the root URL (index route)
@app.route('/')
def index():
    return jsonify({"message": "Flask API is running"})

# Define an API route to fetch the list of PDFs by year
@app.route('/get_pdfs/<year>', methods=['GET'])
def get_pdfs(year):
    try:
        # Create a database cursor to execute queries
        cur = mysql.connection.cursor()
        
        # Write your SQL query
        query = "SELECT filename FROM english_core WHERE year = %s"
        
        # Execute the query with the specified year as a parameter
        cur.execute(query, (year,))
        
        # Fetch all results
        pdfs = cur.fetchall()
        
        # Close the cursor
        cur.close()
        
        # Convert results to JSON format for API response
        pdf_list = [{"filename": pdf[0]} for pdf in pdfs]
        
        # Return the list of PDFs as a JSON response
        return jsonify({"pdfs": pdf_list})

    except Exception as e:
        # Handle errors by returning a JSON error message
        return jsonify({"error": str(e)}), 500

# Define an API route to serve a PDF by filename
@app.route('/pdfs/<filename>', methods=['GET'])
def serve_pdf(filename):
    try:
        # Create a database cursor to execute queries
        cur = mysql.connection.cursor()
        
        # SQL query to fetch the PDF BLOB based on filename
        query = "SELECT pdf_data FROM english_core WHERE filename = %s"
        
        # Execute the query
        cur.execute(query, (filename,))
        result = cur.fetchone()
        
        # Close the cursor
        cur.close()

        if result:
            # Extract PDF data from the result
            pdf_data = result[0]
            
            # Convert BLOB data to a BytesIO stream for sending as a file response
            pdf_io = io.BytesIO(pdf_data)
            
            # Send the PDF file as a response
            return send_file(pdf_io, mimetype='application/pdf', as_attachment=False, download_name=f"{filename}.pdf")
        else:
            return jsonify({"error": "PDF not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the app on all network interfaces (0.0.0.0) and specify a port
    app.run(host='0.0.0.0', port=5000, debug=True)
