import markdown, os
from flask import jsonify
from app import app
from controllers.CityController import *


@app.route('/', methods=['GET']) 
def documentation():
  with open(os.path.dirname(app.root_path) + '/backend-onto/README.md', 'r') as markdown_file:
    content = markdown_file.read()
    return markdown.markdown(content), 200

@app.route('/cities', methods=['GET']) 
def city_index(): return CityController.index()