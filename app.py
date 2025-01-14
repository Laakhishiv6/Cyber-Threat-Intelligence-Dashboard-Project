from flask import Flask, jsonify, render_template, request, redirect, url_for, session 
import random
import csv
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

# Function to generate random IP addresses
def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

# Simulate a larger set of CVE data (100 entries)
def get_cve_data():
    cve_data = []
    vulnerability_types = [
        "Buffer Overflow", "SQL Injection", "Cross-Site Scripting", 
        "Privilege Escalation", "Command Injection", "Directory Traversal", 
        "Denial of Service", "Cross-Site Request Forgery", "Information Disclosure"
    ]
    impacts = [
        "Remote Code Execution", "Denial of Service", 
        "Information Disclosure", "Privilege Escalation", 
        "Data Manipulation", "Unauthorized Access"
    ]
    for i in range(1, 101):  # Generating 100 entries
        cve_data.append({
            "id": f"CVE-2025-{1000+i}",
            "description": f"Vulnerability {i} identified in the software running on IP {generate_random_ip()} with a {random.choice(vulnerability_types)} vulnerability, which could allow an attacker to exploit the system.",
            "severity": random.choice(["High", "Medium", "Low"]),
            "date": time.strftime("%Y-%m-%d", time.gmtime(random.randint(1515122400, 1609459200))),
            "category": random.choice(vulnerability_types),
            "impact": random.choice(impacts),
            "solution": "Upgrade to the latest version of the software to patch the vulnerability."
        })
    return cve_data

# User database (temporary, for demo purposes)
users = {"admin": {"password": "password123", "feedbacks": []}}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]["password"] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Invalid credentials, try again!"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/api/threats')
def get_threats():
    return jsonify(get_cve_data())

@app.route('/api/predict-threats')
def predict_threats():
    prediction = random.choice(['High', 'Medium', 'Low'])
    return jsonify({"prediction": prediction})

@app.route('/api/user-feedback', methods=['POST'])
def user_feedback():
    if 'username' not in session:
        return redirect(url_for('login'))
    feedback = request.form.get('feedback')
    rating = request.form.get('rating')
    username = session['username']
    users[username]["feedbacks"].append({"feedback": feedback, "rating": rating})
    return jsonify({"message": f"Thank you for your feedback: {feedback} (Rating: {rating})"})

@app.route('/api/download-data')
def download_data():
    data = get_cve_data()
    with open("cve_data.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "description", "severity", "date", "category", "impact", "solution"])
        writer.writeheader()
        writer.writerows(data)
    return jsonify({"message": "Data downloaded as cve_data.csv"})

@app.route('/threat/<cve_id>')
def threat_details(cve_id):
    data = get_cve_data()
    threat = next((item for item in data if item['id'] == cve_id), None)
    if threat:
        return render_template('threat_details.html', threat=threat)
    return "Threat not found", 404

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    data = get_cve_data()
    filtered_data = [item for item in data if query.lower() in item['id'].lower() or query.lower() in item['description'].lower()]
    return jsonify(filtered_data)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')


