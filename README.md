# SQL Injection Scanner
> Python Flask-based web app to scan websites for SQL Injection vulnerabilities.

## Description
This tool scans web forms and URLs for SQL Injection vulnerabilities using a curated set of payloads.
The backend is powered by Flask and Python, while the interactive, modern frontend is built with HTML, CSS, and JavaScript.
Results are presented in-browser for rapid analysis and actionable security advice.
- Flexible input: scan any site/form
- Wide variety of real attack payloads (see payloads.txt)
- Live result visualization

## Features
- Test websites and forms for SQL Injection vulnerabilities
- Uses a diverse set of payloads from payloads.txt
- Displays results with security recommendations
- Easy-to-use drag-and-drop interface
- Modern UI with custom favicon

## Technologies Used
- Python 3.x (Flask)
- BeautifulSoup, requests, flask-cors
- HTML, CSS, JavaScript

## Project Structure
```
sql-injection-scanner/
├── app.py # Flask backend
├── payloads.txt # SQL injection payloads
├── frontend/
│   ├── index.html # Main UI
│   ├── style.css # Styles
│   └── script.js # Frontend JS logic
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```
## Installation & Usage
1. **Clone this repository:**
```
git clone https://github.com/mahesh-kakde/sql-injection-scanner.git
cd sql-injection-scanner
```
2. **Backend setup:**
```
cd sql-injection-scanner
pip install -r requirements.txt
python app.py
```
(Default Flask server runs at http://127.0.0.1:5000)

3. **Frontend usage:**
- Open frontend/index.html in your browser.
- Enter the website URL to scan and view results.

## License
This project is licensed under the MIT License. See `LICENSE` for details.

## Author
Mahesh Kakde  
[LinkedIn](https://linkedin.com/in/mahesh-kakde)  
[GitHub](https://github.com/mahesh-kakde)