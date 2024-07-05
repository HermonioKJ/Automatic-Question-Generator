from flask import Flask, render_template, request
import textwrap
import nltk
import cv2
import io
import json
import requests
from app.mcq_generation import MCQGenerator


MCQ_Generator = MCQGenerator(True)

text = "Automobili Lamborghini, the illustrious Italian manufacturer of luxury sports cars and SUVs, is headquartered in the picturesque Sant'Agata Bolognese. This renowned automotive institution boasts a storied legacy, and its contemporary success is firmly underpinned by a fascinating history that has seen it evolve through ownership changes, economic downturns, and groundbreaking innovations.\
Ferruccio Lamborghini, a prominent Italian industrialist with a passion for automobiles, laid the foundation for this iconic marque in 1963. His vision was audacious - to challenge the supremacy of Ferrari, the undisputed titan of Italian sports cars. Under Ferruccio's guidance, Automobili Ferruccio Lamborghini S.p.A. was established, and it immediately began making waves in the automotive world.\
One of the hallmarks of Lamborghini's early years was its distinctive rear mid-engine, rear-wheel-drive layout. This design philosophy became synonymous with Lamborghini's commitment to creating high-performance vehicles. The company's inaugural models, such as the 350 GT, arrived in the mid-1960s and showcased Lamborghini's dedication to precision engineering and uncompromising quality.\
Lamborghini's ascendancy was nothing short of meteoric during its formative decade. It consistently pushed the boundaries of automotive technology and design. However, the heady days of growth were met with a sudden downturn when the world faced the harsh realities of the 1973 global financial crisis and the subsequent oil embargo. Lamborghini, like many other automakers, grappled with plummeting sales and financial instability.\
Ownership of Lamborghini underwent multiple transitions in the wake of these challenges. The company faced bankruptcy in 1978, marking a turbulent chapter in its history. The ownership baton changed hands several times, with different entities attempting to steer the storied brand to calmer waters.\
In 1987, American automaker Chrysler Corporation took the helm at Lamborghini. The Chrysler era saw Lamborghini continue to produce remarkable vehicles like the Diablo while operating under the umbrella of a global conglomerate. However, it was not a permanent arrangement.\
In 1994, Malaysian investment group Mycom Setdco and Indonesian group V'Power Corporation acquired Lamborghini, signaling another phase of transformation for the company. These new custodians brought fresh perspectives and investment to the brand, fueling its resurgence.\
A significant turning point occurred in 1998 when Mycom Setdco and V'Power sold Lamborghini to the Volkswagen Group, which placed the Italian marque under the stewardship of its Audi division. This move brought newfound stability and resources, ensuring Lamborghini's enduring presence in the luxury sports car arena.\
Over the ensuing years, Lamborghini witnessed remarkable expansions in its product portfolio. The V10-powered Huracán captured the hearts of sports car enthusiasts with its exquisite design and formidable performance. Simultaneously, Lamborghini ventured into the SUV market with the Urus, a groundbreaking vehicle powered by a potent twin-turbo V8 engine. This diversification allowed Lamborghini to cater to a broader range of customers without compromising on its commitment to luxury and performance.\
While these successes were noteworthy, Lamborghini was not immune to the challenges posed by global economic fluctuations. In the late 2000s, during the worldwide financial crisis and the subsequent economic downturn, Lamborghini's sales experienced a significant decline, illustrating the brand's vulnerability to external economic factors.\
Despite these challenges, Lamborghini maintained its relentless pursuit of automotive excellence. The company's flagship model, the V12-powered Aventador, reached the pinnacle of automotive engineering and design before concluding its production run in 2022. However, the story does not end here. Lamborghini is set to introduce the Revuelto, a V12/electric hybrid model, in 2024, exemplifying its commitment to embracing cutting-edge technologies and pushing the boundaries of performance.\
In addition to its road car production, Lamborghini has made notable contributions to other industries. The company manufactures potent V12 engines for offshore powerboat racing, further underscoring its prowess in high-performance engineering.\
Interestingly, Lamborghini's legacy extends beyond the realm of automobiles. Ferruccio Lamborghini founded Lamborghini Trattori in 1948, a separate entity from the automobile manufacturer, which continues to produce tractors to this day.\
Lamborghini's rich history is also intertwined with the world of motorsport. In a stark contrast to his rival Enzo Ferrari, Ferruccio Lamborghini decided early on not to engage in factory-supported racing, considering it too expensive and resource-intensive. Nonetheless, Lamborghini's engineers, many of whom were passionate about racing, embarked on ambitious projects, including the development of the iconic Miura sports coupe, which possessed racing potential while being road-friendly. This project marked a pivotal moment in Lamborghini's history, showcasing its ability to create vehicles that could excel on both the track and the road.Despite Ferruccio's reluctance, Lamborghini did make some forays into motorsport. In the mid-1970s, while under the management of Georges-Henri Rossetti, Lamborghini collaborated with BMW to develop and manufacture 400 cars for BMW, a venture intended to meet Group 4 homologation requirements. However, due to financial instability and delays in development, BMW eventually took control of the project, finishing it without Lamborghini's involvement.\
Lamborghini also briefly supplied engines to Formula One teams from 1989 to 1993. Teams like Larrousse, Lotus, Ligier, Minardi, and Modena utilized Lamborghini power units during this period. Lamborghini's best result in Formula One was achieved when Aguri Suzuki finished third at the 1990 Japanese Grand Prix.\
In addition to Formula One, Lamborghini was involved in other racing series. Notably, racing versions of the Diablo were developed for the Diablo Supertrophy, a single-model racing series that ran from 1996 to 1999. The Murciélago R-GT, a production racing car, was created to compete in events like the FIA GT Championship and the American Le Mans Series in 2004, achieving notable results in its racing endeavors.\
Lamborghini's connection with motorsport reflects the brand's commitment to engineering excellence, even though it shied away from factory-backed racing for much of its history.\
Beyond the realms of automotive engineering, Lamborghini has carved a distinct niche in the world of branding. The company licenses its prestigious brand to manufacturers who produce a wide array of Lamborghini-branded consumer goods, including scale models, clothing, accessories, bags, electronics, and even laptop computers. This strategic approach has enabled Lamborghini to extend its brand reach beyond the confines of the automotive industry.\
One fascinating aspect of Lamborghini's identity is its deep connection with the world of bullfighting. In 1962, Ferruccio Lamborghini visited the ranch of Don Eduardo Miura, a renowned breeder of Spanish fighting bulls. Impressed by the majestic Miura animals, Ferruccio decided to adopt a raging bull as the emblem for his burgeoning automaker. This emblem, now iconic, symbolizes Lamborghini's passion for performance, power, and the thrill of the chase.\
Lamborghini's vehicle nomenclature also reflects this bullfighting heritage, with many models bearing the names of famous fighting bulls or bull-related themes. The Miura, named after the Miura bulls, set the precedent, and subsequent models like the Murciélago, Gallardo, and Aventador continued this tradition.\
Furthermore, Lamborghini has enthusiastically embraced emerging automotive technologies, responding to environmental concerns and changing consumer preferences. The Sian, introduced as the company's first hybrid model, showcases Lamborghini's commitment to sustainable performance. With its innovative hybrid powertrain, the Sian combines electric propulsion with a naturally aspirated V12 engine to deliver breathtaking performance while minimizing emissions.\
Looking ahead, Lamborghini has ambitious plans to produce an all-electric vehicle, aligning with the broader industry trend towards electrification. While traditionalists may lament the absence of roaring V12 engines, Lamborghini recognizes the importance of evolving with the times, ensuring that future generations of enthusiasts can experience the thrill of a Lamborghini while contributing to a more sustainable future.\
In summary, Automobili Lamborghini stands as a testament to the enduring allure of Italian craftsmanship and automotive"

def generate_questions_from_text_file(file_path: str, question_type: tuple):
    mcq_count, id_count = question_type
    with open(file_path, 'r') as file:
        text = file.read()
        generate_questions_from_text(text, question_type)

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

def choose_input_type():
    print("Choose an input type:")
    print("1. Text input")
    print("2. Text file input")
    print("3. Image input")
    choice = input("Enter your choice (1/2/3): ")

    question_quan = choose_question_type()
    
    if choice == "1":
        text_input = input("Enter your text: ")
        generate_questions_from_text(text_input, question_quan)
    elif choice == "2":
        file_input = input("Enter path to your text file: ")
        generate_questions_from_text_file(file_input, question_quan)
    elif choice == "3":
        image_input = input("Enter path to your image file: ")
        generate_questions_from_image(image_input, question_quan)
    return question_quan

def choose_question_type():
    print("How many questions for each type:")
    print("Multiple Choice Questions")
    MCQcount = input("Enter your choice: ")
    print("Identification Questions:")
    countID = input("Enter your choice: ")
    return int(MCQcount), int(countID)

def generate_questions_from_text(text: str, question_type: tuple):
    mcq_count, id_count = question_type
    MCQ_Generator = MCQGenerator(True)
    questions = MCQ_Generator.generate_questions(text, mcq_count, id_count)
    id_questions, mcq_questions = questions
    return id_questions, mcq_questions



questions = choose_input_type()

