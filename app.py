from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import datetime

app = Flask(__name__)

# Filename for uploads and forms
dirname = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]

# Function to handle file uploads
def handle_file_upload(files, name):
    for i, file in enumerate(files):
        f = f"uploads/{dirname}/{name}_{i+1}.pdf"
        print(f"Saving file to {f}")
        file.save(f)

# Function to write form data to CSV
def write_to_csv(data):
    csv_file = f"uploads/{dirname}/{data['name']}.csv"
    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data.values())

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    form_data = {}
    for field in request.form:
        form_data[field] = request.form[field]

    if not os.path.exists('uploads/' + dirname):
        os.mkdir('uploads/' + dirname)

    attachments = []
    for field in request.files:
        if request.files.getlist('attachments'):
            attachments = request.files.getlist('attachments')
    
    handle_file_upload(attachments, form_data['name'])
    write_to_csv(form_data)


    return redirect(url_for('success'))

@app.route('/success')
def success():
    return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)
