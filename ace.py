import textwrap
import nltk
import cv2
import io
import json
import requests
from app.mcq_generation import MCQGenerator

nltk.download('punkt')

def show_result(generated: str, answer: str, context: str, original_question: str = ''):
    print('Question:')
    print(generated)

    print('Answer:')
    print(answer)
    print('-----------------------------')

def generate_questions_from_text(text: str, question_type: tuple):
    mcq_count, id_count = question_type
    MCQ_Generator = MCQGenerator(True)
    questions = MCQ_Generator.generate_questions(text, mcq_count, id_count)

def generate_questions_from_text_file(file_path: str, question_type: tuple):
    mcq_count, id_count = question_type
    with open(file_path, 'r') as file:
        text = file.read()
        generate_questions_from_text(text, mcq_count, id_count)

def generate_questions_from_image(image_path: str,question_type: tuple):
    mcq_count, id_count = question_type
    img = cv2.imread(image_path)
    height, width, _ = img.shape

    roi = img

    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".png", roi, [1, 90])
    file_bytes = io.BytesIO(compressedimage)

    result_ocr = requests.post(url_api,
                                files={"image.png": file_bytes},
                                data={"apikey": "helloworld",
                                    "language": "eng"})
    result_ocr = result_ocr.content.decode()
    result_ocr = json.loads(result_ocr)

    text_from_image = ' '.join([item['ParsedText'] for item in result_ocr['ParsedResults']])
    generate_questions_from_text(text_from_image, question_type)

def choose_question_type():
    print("How many questions for each type:")
    print("Multiple Choice Questions")
    MCQcount = input("Enter your choice: ")
    print("Identification Questions:")
    countID = input("Enter your choice: ")
    return int(MCQcount), int(countID)

def choose_input_type():
    print("Choose an input type:")
    print("1. Text input")
    print("2. Text file input")
    print("3. Image input")
    choice = input("Enter your choice (1/2/3): ")

    question_type = choose_question_type()

    if choice == "1":
        text_input = input("Enter your text: ")
        generate_questions_from_text(text_input, question_type)
    elif choice == "2":
        file_input = input("Enter path to your text file: ")
        generate_questions_from_text_file(file_input, question_type)
    elif choice == "3":
        image_input = input("Enter path to your image file: ")
        generate_questions_from_image(image_input, question_type)
    else:
        print("Invalid choice. Please choose a valid option.")

# Example usage
choose_input_type()
