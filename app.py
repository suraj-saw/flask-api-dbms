import pymysql
from flask import Flask, jsonify, send_file
from flask_cors import CORS
from config import Config
import io

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for the app
CORS(app)

# Manually establish a connection using pymysql
def get_db_connection():
    return pymysql.connect(host=Config.MYSQL_HOST,
                             user=Config.MYSQL_USER,
                             password=Config.MYSQL_PASSWORD,
                             database=Config.MYSQL_DB,
                             port=Config.MYSQL_PORT,
                             ssl_disabled=True)  # Disable SSL explicitly

# API route to fetch the list of PDFs by year
@app.route('/get_pdfs/<year>', methods=['GET'])
def get_pdfs(year):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Write your SQL query
        query = "SELECT filename FROM english_core WHERE year = %s"
        cursor.execute(query, (year,))
        
        # Fetch all results
        pdfs = cursor.fetchall()
        
        # Close the cursor and connection
        cursor.close()
        connection.close()
        
        # Convert results to JSON format for API response
        pdf_list = [{"filename": pdf[0]} for pdf in pdfs]
        
        return jsonify({"pdfs": pdf_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API route to serve a PDF by filename
@app.route('/pdfs/<filename>', methods=['GET'])
def serve_pdf(filename):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        query = "SELECT pdf_data FROM english_core WHERE filename = %s"
        cursor.execute(query, (filename,))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()

        if result:
            pdf_data = result[0]
            pdf_io = io.BytesIO(pdf_data)
            return send_file(pdf_io, mimetype='application/pdf', as_attachment=False, download_name=f"{filename}.pdf")
        else:
            return jsonify({"error": "PDF not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
