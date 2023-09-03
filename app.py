import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request

app = Flask(__name__)

# Use your own scope and credentials file
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

client = gspread.authorize(credentials)

spreadsheet = client.open('AyushRupicard')  # Use your own spreadsheet name
worksheet = spreadsheet.get_worksheet(0)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        # Validate name and mobile number
        if not name or len(name.replace(" ","")) < 4 or not all(c.isalpha() or c.isspace() for c in name):
            return "Name must contain only alphabets and spaces and be at least 4 characters long", 400
        if not mobile.isdigit() or len(mobile) != 10:
            return "Mobile number must be a valid 10-digit number", 400
        # check if it's the first row, then add header and data
        if worksheet.row_count == 1:
            worksheet.append_row(['Username', 'Mob_No'])
        worksheet.append_row([name, mobile])
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
