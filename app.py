import os
import json
import subprocess
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {
    "en": "English",
    "vi": "Vietnamese",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    # Add more languages as needed...
}

is_crawling = False  # Track crawl status


def start_crawl(keyword, location_code):
    global is_crawling
    is_crawling = True  # Set crawling status to true

    # Run main.py as a subprocess, passing in translated keyword and location as arguments
    process = subprocess.Popen(
        ['python', 'main.py', '--keyword', keyword, '--location', location_code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = process.communicate()
    if process.returncode != 0:
        is_crawling = False  # Reset crawling status if there's an error
        error_message = stderr.decode()
        logger.error(f"Error in crawling: {error_message}")
        return jsonify({"status": "error", "message": f"Error in crawling: {error_message}"}), 500

    is_crawling = False  # Reset crawling status after successful run
    logger.info("Crawl started successfully.")
    return jsonify({"status": "success", "message": "Crawl started successfully."}), 202


@app.route('/')
def home():
    return render_template("home.html", languages=SUPPORTED_LANGUAGES)


@app.route('/crawl', methods=['POST'])
def crawl():
    global is_crawling
    if is_crawling:
        return jsonify({"status": "error", "message": "Crawl in progress"}), 202
    
    keyword = request.form.get("keyword")
    location_code = request.form.get("location")

    if not keyword or not location_code:
        return jsonify({"status": "error", "message": "Keyword and location are required"}), 400

    # Clear the file before each new crawl
    with open("output.json", "w") as f:
        f.write("[]")

    is_crawling = True
    success = start_crawl(keyword, location_code)
    is_crawling = False

    if not success:
        return jsonify({"status": "error", "message": "Error in starting crawl"}), 500

    # Redirect to results if successful
    return redirect(url_for('get_results'))




@app.route('/status', methods=['GET'])
def crawl_status():
    global is_crawling
    return jsonify({"status": "in progress" if is_crawling else "completed"})

@app.route('/results', methods=['GET'])
def get_results():
    try:
        # Always read the output.json file fresh
        if os.path.exists("output.json"):
            with open("output.json", "r", encoding="utf-8") as f:
                results = json.load(f)
        else:
            results = []

        return render_template("results.html", results=results)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return render_template("results.html", results=[], error="Error loading results. Please ensure the JSON format is correct.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        return render_template("results.html", results=[], error="An unexpected error occurred.")




if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="0.0.0.0", debug=True)
