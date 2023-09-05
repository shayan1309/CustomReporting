# app/routes.py

from flask import Flask, render_template, request, jsonify
import os
from functions.api import handler as api_handler
from functions.process import handler as process_handler
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        api_key = request.form["api_key"]
        project_name = request.form["project_name"]
        saved_report_name = request.form["saved_report_name"]
        word_file = request.files["word_file"]

        # Save the uploaded file
        file_path = "C:\\Python\\uploads"
        word_file.save(os.path.join(file_path, word_file.filename))

        # Call the API handler function
        api_response = api_handler(api_key, project_name, saved_report_name, file_path)

        # Call the data processing handler function
        processed_data = process_handler(api_response)

        return jsonify({"data": processed_data})

    return render_template("index.html")

if __name__ == "__main__":
    app.run()


