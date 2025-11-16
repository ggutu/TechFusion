from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import redis
from dotenv import load_dotenv
import os

load_dotenv()

# Read database and Redis config from environment
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')

# load config.py into environment variables
# import config

# # os.environ['MYSQL_HOST'] = config.MYSQL_HOST
# # os.environ['MYSQL_USER'] = config.MYSQL_USER
# # os.environ['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
# # os.environ['MYSQL_DB'] = config.MYSQL_DB
# # os.environ['REDIS_HOST'] = config.REDIS_HOST
# # os.environ['REDIS_PORT'] = str(config.REDIS_PORT)
# # os.environ['SECRET_KEY'] = config.SECRET_KEY

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# MySQL connection setup
mysql_db = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DB')
)
mysql_cursor = mysql_db.cursor()

def run_db_script():
    try:
        # Open and read the SQL file
        with open('database/schema.sql', 'r') as f:
            sql_script = f.read()
        
        # Split the SQL script into individual queries
        sql_statements = sql_script.split(';')  # Split by semicolon to get individual statements
        
        # Execute each statement
        for statement in sql_statements:
            statement = statement.strip()
            if statement:  # Skip empty statements
                mysql_cursor.execute(statement)
        
        # Commit the changes to the database
        mysql_db.commit()
        print("Database schema executed successfully.")
    
    except mysql.connector.Error as err:
        print("Error executing script:", err)


run_db_script()
# Redis connection setup
redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=0, decode_responses=True)

@app.route('/')
def index():
    # Check if the user is cached in Redis
    if 'user_data' in session:
        user_data = session['user_data']
        return render_template('index.html', user=user_data)
    else:
        return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        # Try to fetch user data from Redis
        user_data = redis_client.get(username)
        if user_data:
            # If data exists in Redis, use it
            user_data = user_data.split(',')
            return render_template('index.html', user={'username': user_data[0], 'email': user_data[1]})
        else:
            # If data is not cached, query MySQL
            mysql_cursor.execute("SELECT * FROM users WHERE username = %s AND email = %s", (username, email))
            user = mysql_cursor.fetchone()
            if user:
                # Cache user data in Redis
                redis_client.set(username, f"{user[1]},{user[2]}", ex=3600)  # 1-hour expiration
                session['user_data'] = {'username': user[1], 'email': user[2]}
                return redirect(url_for('index'))
            else:
                return "Invalid username or email", 400
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_data', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=9999, host='0.0.0.0')
