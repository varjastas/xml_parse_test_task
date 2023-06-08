from flask import Flask, request, jsonify, render_template, send_file, after_this_request, Response, make_response
import random
import string
import os
from time import time
# import your script functions and classes
from main import parse_file
import shutil
import tempfile


app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))

resources_dir = os.path.join(base_dir, 'resources')

#Create files containing parsing results if they`re not present
def create_result_files():
    if not os.path.exists("items_count.txt"):
        parse_file("resources/export_full.xml", 1, True)
    if not os.path.exists("items.txt"):
        parse_file("resources/export_full.xml", 2, True)
    if not os.path.exists("parts.txt"):
        parse_file("resources/export_full.xml", 3, True)

#Running function on start of server
with app.app_context():
    create_result_files()

@app.route('/')
def index():
    create_result_files()
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse():
    create_result_files()
    data = request.json
    scenario = int(data.get('scenario'))

    if scenario == 1:
        file_name = "resources/items_count.txt"
    elif scenario == 2:
        file_name = "resources/items.txt"
    elif scenario == 3:
        file_name = "resources/parts.txt"
    
    file_path = os.path.join(base_dir, file_name)

    #Reading result file content 
    with open(file_path, 'rb') as file:
        file_content = file.read()

    response = make_response(file_content)
    response.headers.set('Content-Type', 'application/octet-stream')
    response.headers.set('Content-Disposition', 'attachment', filename='result.txt')

    return response

if __name__ == '__main__':
    app.run(debug=True)