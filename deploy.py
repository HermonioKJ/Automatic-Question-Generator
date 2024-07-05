from flask import Flask, render_template, request
import textwrap
import cv2
import io
import json
import requests
from app.mcq_generation import MCQGenerator

app = Flask(__name__)

# Your other functions and code go here...

if __name__ == '__main__':
    app.run(debug=True)
