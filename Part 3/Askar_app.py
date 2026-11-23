##### FINAL - Part 3 #####
##### CSEC-380/480 - <Farris Askar> ####

'''
3) 12 points Part 3: Podman/Ansible (Flask app with Postgres).
'''

from flask import Flask, render_template, request, redirect, url_for
import re
import logging
import psycopg2


# Instantiate Flask app and setup logging
app = Flask(__name__)
logging.basicConfig(
    filename='web_log.log',
    level = logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

# Add Flask route that targets the root directory
@app.route('/')
def index():
    fields = {
        'first_name': {
            'name': 'firstname',
            'description': 'First Name:',
            'placeholder': 'Enter your first name'
        },
        'last_name': {
            'name': 'lastname',
            'description': 'Last Name:',
            'placeholder': 'Enter your last name'
        },
        'phone': {
            'name': 'phone',
            'description': 'Phone Number:',
            'placeholder': 'Enter your phone number'
        },
        'email': {
            'name': 'email',
            'description': 'Email Address:',
            'placeholder': 'Enter your email address'
        },
    }

    departments = [
        {'id': 'HR', 'name': 'Human Resources'},
        {'id': 'IT', 'name': 'Information Technology'},
        {'id': 'Finance', 'name': 'Finance'},
        {'id': 'Marketing', 'name': 'Marketing'},
        {'id': 'Sales', 'name': 'Sales'}
    ]

    # Logging debug message that states the template is being rendered
    logging.debug('Rendering register.j2 template')
    # Render Jinja template
    return render_template('register.j2', fields=fields, departments=departments)

# Part 3 section!
def save_user(firstname, lastname, phone, email, department):
    conn = psycopg2.connect(
        host = '127.0.0.1',
        port = 5432,
        dbname = 'flask_db',
        user = 'faskar',
        password = 'csec380480'
    )
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (first_name, last_name, phone_number, email_address, department) Values (%s, %s, %s, %s, %s)",
        (firstname, lastname, phone, email, department)
    )
    conn.commit()
    cur.close()
    conn.close()

# Add Flask route that lets user post form data
@app.route('/register', methods=['POST'])
def register():
    # Get form data
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    phone = request.form.get('phone')
    email = request.form.get('email')
    department = request.form.get('department')

    # Logging debug message that displays the collected form data
    logging.debug(f'Form data: {firstname} | {lastname} | {phone} | {email} | {department}')
    # Define email regex
    email_regex = r'^[\w.+-]+@[\w-]+\.[\w.-]+$'

    # Validate Email. If validation fails, call the error function and include an error message.
    # Logging error message that states the incorrect email.
    if not re.match(email_regex, email):
        logging.error(f'Invalid email: {email}')
        return redirect(url_for('error', message='Invalid email format please enter a valid email'))

    # Define phone regex
    phone_regex = r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'

    # Validate Phone. If validation fails, call the error function and include an error message. 
    # Logging error message that states the incorrect phone number.
    if not re.match(phone_regex, phone):
        logging.error(f'Invalid phone number: {phone}')
        return redirect(url_for('error', message='Invalid phone number please enter a valid phone number.'))

    # Part 3:
    save_user(firstname, lastname, phone, email, department)
    # If all inputs are valid, redirect to root/index
    # Logging info message that states the user is registered successfully. (This is instead of performing a registration action)
    logging.info(f'User registered successfully: {firstname} {lastname}')
    return redirect(url_for('index'))

# Add a Flask route that displays an error if incorrect format is submitted
@app.route('/error')
def error():
    message = request.args.get('message')
    logging.info('Error template rendered')
    return render_template('error.j2', message=message)

if __name__ == '__main__':
    # Run webserver
    # Logging info message that states the webserver is running
    logging.info('Webserver is running')
    app.run()