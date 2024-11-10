import os

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost.render.com')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Suraj03saw@')
    MYSQL_DB = os.getenv('MYSQL_DB', 'project')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))  # Default to 3306 if not set
