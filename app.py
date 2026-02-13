import csv
import json
import os
import random
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from flask import send_file
from flask_sqlalchemy import SQLAlchemy
from openpyxl import load_workbook
from werkzeug.security import check_password_hash, generate_password_hash

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db')
app.config['SQLALCHEMY_BINDS'] = {
    'mood_tracker': os.getenv('SQLALCHEMY_BINDS_MOOD_TRACKER', 'sqlite:///mood_tracker.db'),
    'submit_assessment': os.getenv('SQLALCHEMY_BINDS_SUBMIT_ASSESSMENT', 'sqlite:///submit-assessment.db'),
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'Akingbesote Babajide Created This Site 08134812419'  # Replace with a secure key

# Securely load secret key
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Placeholder for tracking homepage visits
homepage_visits = []

JOURNAL_FILE = "journal_entries.json"

# Upload folder setup
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CSV_FILE = os.path.join(UPLOAD_FOLDER, "responses.csv")
EXCEL_FILE = os.path.join(UPLOAD_FOLDER, "responses.xlsx")

# Admin credentials (hashed password)
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD_HASH = generate_password_hash(os.getenv('ADMIN_PASSWORD'))  # Always store hashed passwords

# API Keys
IPGEO_API_KEY = os.getenv('IPGEO_API_KEY')

# Function to load journal entries
def load_journal_entries():
    if os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save a new journal entry
def save_journal_entry(entry):
    entries = load_journal_entries()
    entries.append(entry)  # Add new entry
    with open(JOURNAL_FILE, "w") as file:
        json.dump(entries, file, indent=4)

class JournalEntry(db.Model):
    __bind_key__ = 'mood_tracker'  # Ensures this table is stored in mood_tracker.db
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(50), nullable=False)
    entry = db.Column(db.Text, nullable=False)
    activity = db.Column(db.String(255))  # Optional field
    note = db.Column(db.Text)  # Optional field
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


### **MODELS**
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    service = db.Column(db.String(100))

    def __repr__(self):
        return f'<Registration {self.name}>'

class SubmitAssessment(db.Model):
    __bind_key__ = 'submit_assessment'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    email = db.Column(db.String(100)) # New
    phone = db.Column(db.String(20))  # New
    age = db.Column(db.Integer)
    sex = db.Column(db.String(20))
    # Create q1 through q20
    q1 = db.Column(db.Integer); q2 = db.Column(db.Integer); q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer); q5 = db.Column(db.Integer); q6 = db.Column(db.Integer)
    q7 = db.Column(db.Integer); q8 = db.Column(db.Integer); q9 = db.Column(db.Integer)
    q10 = db.Column(db.Integer); q11 = db.Column(db.Integer); q12 = db.Column(db.Integer)
    q13 = db.Column(db.Integer); q14 = db.Column(db.Integer); q15 = db.Column(db.Integer)
    q16 = db.Column(db.Integer); q17 = db.Column(db.Integer); q18 = db.Column(db.Integer)
    q19 = db.Column(db.Integer); q20 = db.Column(db.Integer)

class Feedback(db.Model):
    __bind_key__ = 'submit_assessment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()  # Ensure this is called only once

# Random Challenges
challenges = [
    "🌞 Take a 5-minute walk outside!",
    "🎶 Listen to your favorite song and dance!",
    "📖 Read a page from an inspiring book.",
    "🌿 Try deep breathing for 1 minute.",
    "💌 Send a kind message to a friend.",
    "🎨 Draw or doodle something fun!"
]


# Random Affirmations
affirmations = [
    "💖 You are enough just as you are.",
    "🌟 You have the strength to overcome any challenge.",
    "😊 You bring positivity into the world.",
    "💙 You deserve love, happiness, and peace.",
    "🌿 Take a deep breath. You are doing great.",
    "🔥 You are capable of amazing things."
]


class PageVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(255))

with app.app_context():
    db.create_all()


# Set or Update a Cookie
@app.route('/set-cookie', methods=['POST'])
def set_cookie():
    data = request.json
    cookie_name = data.get('name')
    cookie_value = data.get('value')
    days = data.get('days', 30)

    if not cookie_name or not cookie_value:
        return jsonify({"error": "Missing cookie name or value"}), 400

    response = make_response(jsonify({"message": f"Cookie {cookie_name} set"}))
    response.set_cookie(cookie_name, cookie_value, max_age=days * 24 * 60 * 60)
    return response

# Get a Cookie
@app.route('/get-cookie', methods=['GET'])
def get_cookie():
    cookie_name = request.args.get('name')
    if not cookie_name:
        return jsonify({"error": "Cookie name is required"}), 400

    cookie_value = request.cookies.get(cookie_name)
    if cookie_value:
        return jsonify({cookie_name: cookie_value})
    else:
        return jsonify({"error": "Cookie not found"}), 404
        
@app.route('/mood_tracker')
def mood_tracker():
    return render_template('mood_tracker.html')

# API: Get a Random Affirmation (one per day based on date)
@app.route('/api/affirmation', methods=['GET'])
def get_affirmation():
    """
    Returns the same affirmation for the entire day.
    Uses current date as seed to ensure consistency.
    """
    # Get today's date as string
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Use date as seed for random selection
    random.seed(today + "affirmation")  # Add suffix to make it unique from challenge
    daily_affirmation = random.choice(affirmations)
    
    # Reset random seed to not affect other operations
    random.seed()
    
    return jsonify({"affirmation": daily_affirmation})

# API: Get a Random Challenge (one per day based on date)
@app.route('/api/challenge', methods=['GET'])
def get_challenge():
    """
    Returns the same challenge for the entire day.
    Uses current date as seed to ensure consistency.
    """
    # Get today's date as string
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Use date as seed for random selection
    random.seed(today + "challenge")  # Add suffix to make it unique from affirmation
    daily_challenge = random.choice(challenges)
    
    # Reset random seed to not affect other operations
    random.seed()
    
    return jsonify({"challenge": daily_challenge})



# API: Get All Journal Entries
@app.route('/api/journal', methods=['GET'])
def get_journals():
    journals = JournalEntry.query.all()
    journal_list = [{"id": j.id, "mood": j.mood, "entry": j.entry} for j in journals]
    return jsonify(journal_list)

# API to save journal entries
@app.route('/save_journal_entry', methods=['POST'])
def save_journal_entry_route():
    data = request.get_json()

    if not data or 'mood' not in data or 'entry' not in data:
        return jsonify({'error': 'Mood and entry are required'}), 400

    new_entry = JournalEntry(
        mood=data['mood'],
        entry=data['entry'],
        activity=data.get('activity', None),
        note=data.get('note', None),
        timestamp=data.get('timestamp', datetime.utcnow())
    )

    db.session.add(new_entry)
    db.session.commit()

    return jsonify({'message': 'Journal entry saved successfully'}), 201


@app.route('/api/get_journal')
def get_journal():
    """Retrieve all past journal entries."""
    entries = load_journal_entries()
    return jsonify(entries)


@app.route('/')
def index():
    ip_address = request.remote_addr
    location = get_location(ip_address)

    # Get visit count from cookies
    visit_count = request.cookies.get("visit_count", 0)
    visit_count = int(visit_count) + 1

    # Add visit to homepage visits log
    homepage_visits.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "location": location
    })

    # Store visit in database if it's the first time
    existing_visit = PageVisit.query.filter_by(ip_address=ip_address).first()
    if not existing_visit:
        visit = PageVisit(ip_address=ip_address, location=location)
        db.session.add(visit)
        db.session.commit()

    # Create response with updated visit count cookie
    resp = make_response(render_template("index.html", location=location, visit_count=visit_count))
    resp.set_cookie("visit_count", str(visit_count), max_age=365 * 24 * 60 * 60, httponly=True, samesite="Lax")

    return resp


@app.route('/submit-assessment', methods=['POST'])
def submit_assessment():
    total_score = 0
    unanswered_questions = 0
    
    # 1. Capture Personal Info
    email = request.form.get("email")
    phone = request.form.get("phone")
    age = request.form.get("age")
    sex = request.form.get("sex")

    # 2. Scoring Map (Ensure exactly 20 items)
    # 1-5 represents the value of the option selected
    score_mappings = [
        {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}, {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}, # q1, q2
        {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, # q3, q4
        {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, # q5, q6
        {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, # q7, q8
        {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}, # q9, q10
        {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, # q11, q12
        {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, # q13, q14
        {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, # q15, q16
        {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, # q17, q18
        {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}  # q19, q20
    ]

    # 3. Loop through q1 to q20
    answers_dict = {}
    for i in range(1, 21):
        val = request.form.get(f'q{i}')
        if val:
            try:
                ans_int = int(val)
                total_score += score_mappings[i-1][ans_int]
                answers_dict[f'q{i}'] = ans_int
            except (ValueError, KeyError):
                unanswered_questions += 1
        else:
            unanswered_questions += 1

    # 4. Error Check
    if unanswered_questions > 0:
        return render_template('error.html', message=f"Please answer all questions. You missed {unanswered_questions}.")

    # 5. Save to Database
    try:
        new_assessment = SubmitAssessment(
            email=email,
            phone=phone,
            age=age,
            sex=sex,
            **answers_dict # This automatically maps q1=val, q2=val...
        )
        db.session.add(new_assessment)
        db.session.commit()
    except Exception as e:
        print(f"Database Error: {e}")
        # Even if DB fails, we want the user to see their result
        pass

    return redirect(url_for('assessment_results', score=total_score))

@app.route('/assessment_results')
def assessment_results():
    score = request.args.get('score', 0, type=int)
    return render_template('assessment_results.html', score=score)


@app.route('/admin/clear_excel', methods=['POST'])
def clear_excel():
    # Ensure only admin can perform this action
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    if os.path.exists(EXCEL_FILE):
        wb = load_workbook(EXCEL_FILE)
        ws = wb.active
        # Delete all rows after the header row (assuming header is in row 1)
        if ws.max_row > 1:
            ws.delete_rows(2, ws.max_row - 1)
        wb.save(EXCEL_FILE)
        message = "Excel sheet entries have been cleared."
    else:
        message = "Excel file does not exist."

    # You can choose to render a template with the message or simply return it.
    return render_template('admin_panel.html')

@app.route('/visit')
def visit():
    visit_count = request.cookies.get('visit_count', 0)
    location = request.cookies.get('location', "Unknown")

    return render_template('visit.html', visit_count=visit_count, homepage_visits=homepage_visits)


def calculate_age(dob):
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    except ValueError:
        return None  # Invalid date format

@app.route('/submit', methods=['POST'])
def submit():
    required_fields = ['name', 'age', 'email', 'phone', 'service']
    for field in required_fields:
        if field not in request.form:
            return f"Missing field: {field}", 400

    # Capture specific form fields
    name = request.form['name']
    age = calculate_age(request.form['age'])
    email = request.form['email']
    phone = request.form['phone']
    service = request.form['service']

    if not age:
        return "Invalid date format for age", 400

    # Save to database
    new_registration = Registration(name=name, age=age, email=email, phone=phone, service=service)
    db.session.add(new_registration)
    db.session.commit()

    data = {key: [value] for key, value in request.form.items()}
    df = pd.DataFrame(data)

    # Append to Excel file
    if os.path.exists(EXCEL_FILE):
        with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            wb = load_workbook(EXCEL_FILE)
            sheet = wb.active
            start_row = sheet.max_row + 1
            df.to_excel(writer, index=False, header=False, startrow=start_row)
    else:
        df.to_excel(EXCEL_FILE, index=False)

    return redirect(url_for('confirmation'))



@app.route('/confirmation')
def confirmation():
    latest_submission = Registration.query.order_by(Registration.id.desc()).first()

    if latest_submission:
        return render_template(
            'confirmation.html',
            name=latest_submission.name,
            age=latest_submission.age,
            email=latest_submission.email,
            phone=latest_submission.phone,
            service=latest_submission.service,
        )
    return "No submission found."


@app.route('/admin/registrations')
def admin_registrations():
    registrations = Registration.query.all()
    latest_data = {
        "name": session.get('name'),
        "age": session.get('age'),
        "email": session.get('email'),
        "phone": session.get('phone'),
        "service": session.get('service'),
    }

    return render_template(
        'admin_registrations.html',
        registrations=registrations,
        latest=latest_data,
        datetime=datetime  # Pass datetime to the template
    )


@app.route('/admin/delete_submission/<int:id>', methods=['POST'])
def delete_submission(id):
    try:
        submission = Registration.query.get(id)
        if submission:
            db.session.delete(submission)
            db.session.commit()
            return jsonify({"success": True, "message": "Submission deleted successfully."})
        return jsonify({"success": False, "message": "Submission not found."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)})


@app.route('/register', endpoint='register')
def register():
    return render_template('register.html')

@app.route('/mental')
def mental():
    return render_template('mental.html')

@app.route('/Resources')
def Resources():
    return render_template('Resources.html')

@app.route('/sel_activities')
def sel_activities():
    return render_template('sel-activities.html')

def get_location(ip):
    try:
        # Handle local/private IPs
        if ip in ["127.0.0.1", "::1"] or ip.startswith(("192.168.", "10.", "172.")):
            return "Local Network (Unknown Location)"

        # API Request
        url = f"https://api.ipgeolocation.io/ipgeo?apiKey={IPGEO_API_KEY}&ip={ip}"
        response = requests.get(url, timeout=5)  # 5-second timeout

        if response.status_code == 200:
            data = response.json()
            city = data.get("city", "Unknown")
            country = data.get("country_name", "Unknown")
            return f"{city}, {country}"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching location: {e}")

    return "Location unavailable"

# Download Responses (CSV)
@app.route('/admin/download_responses')
def download_responses():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    if not os.path.exists(EXCEL_FILE):
        return "No responses available to download.", 404

    return send_file(EXCEL_FILE, as_attachment=True, download_name="responses.csv")




@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error_message = None
    if request.method == 'POST':
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session["is_admin"] = True
            return redirect(url_for("admin_panel"))
        else:
            error_message = "Invalid username or password!"
    return render_template("admin_login.html", error=error_message)

@app.route('/admin/panel')
def admin_panel():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    # Get file list from the static/uploads/ folder
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("admin_panel.html", files=files)


@app.route('/admin/logout')
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin_login"))


### **RUN FLASK APP**
if __name__ == "__main__":
    app.run(debug=True)