import MySQLdb
from config import Config

try:
    # Attempt to connect to the database
    connection = MySQLdb.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        passwd=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB,
        port=Config.MYSQL_PORT
    )
    print("Connection successful!")
    connection.close()
except MySQLdb.Error as e:
    print(f"Error connecting to MySQL: {e}")
