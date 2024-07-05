from flask import Flask, render_template, request, jsonify
from app.mcq_generation import MCQGenerator  # Import your MCQGenerator
from app.models.question import Question

from typing import List
from nltk.tokenize import sent_tokenize
import cv2
import io
import toolz
import requests
import json
import re

app = Flask(__name__)
MCQ_Generator = MCQGenerator(True)

def generate_questions_from_text(text: str, mcq_count: int, id_count: int):
    ID_questions, MCQ_questions = MCQ_Generator.generate_questions(text, mcq_count, id_count)
    return ID_questions, MCQ_questions

# Function to generate questions from a text file
def generate_questions_from_text_file(file_path: str, mcq_count: int, id_count: int):
    with open(file_path, 'r') as file:
        text = file.read()
        return generate_questions_from_text(text, mcq_count, id_count)

def generate_questions_from_image(image_bytes: bytes, mcq_count: int, id_count: int):
    files = {"image.png": image_bytes}

    url_api = "https://api.ocr.space/parse/image"
    result_ocr = requests.post(url_api,
                               files=files,
                               data={"apikey": "helloworld", "language": "eng"})

    result_ocr = result_ocr.content.decode()
    result_ocr = json.loads(result_ocr)
    text_from_image = ''
    if 'ParsedResults' in result_ocr and len(result_ocr['ParsedResults']) > 0:
        text_from_image = ' '.join([item['ParsedText'] for item in result_ocr['ParsedResults']])
    cleaned_text = re.sub(' +', ' ', text_from_image)
    if len(cleaned_text.split()) <= 10:  # Define a threshold (e.g., 5 words)
        return "No visible text found", "No visible text found"
    print(cleaned_text)
    return generate_questions_from_text(text_from_image, mcq_count, id_count)


# Route to render the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and generate questions
@app.route('/generate', methods=['POST'])
def generate():
    input_type = request.form['inputType']
    mcq_count = int(request.form['mcqCount'])
    id_count = int(request.form['idCount'])

    if input_type == 'text':
        text_input = request.form['textInput']
        text_question = generate_questions_from_text(text_input, mcq_count, id_count)
        id_questions, mcq_questions = text_question
    elif input_type == 'file':
        file = request.files['fileInput']
        file_path = 'path_to_save_uploaded_file'
        file.save(file_path)
        text_file = generate_questions_from_text_file(file_path, mcq_count, id_count)
        id_questions, mcq_questions = text_file
    elif input_type == 'jpg':
        file = request.files['jpgInput']
        image_bytes = file.read()  # Read image file as bytes
        id_questions, mcq_questions = generate_questions_from_image(image_bytes, mcq_count, id_count)


    return render_template('questions.html', id_questions=id_questions, mcq_questions=mcq_questions)
 

if __name__ == '__main__':
    app.run(debug=True)
