import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
import pdfplumber
from docx import Document
import spacy

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)  # Add this line

# Configuration for file uploads
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit to 16MB

def extract_text(file_path):
    """Extract text from PDF or DOCX files."""
    try:
        if file_path.endswith('.pdf'):
            with pdfplumber.open(file_path) as pdf:
                return ' '.join(page.extract_text() or '' for page in pdf.pages)
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            return ' '.join(paragraph.text for paragraph in doc.paragraphs)
    except Exception as e:
        return ""
    return ""

def analyze_resume(text):
    """Analyze the resume text."""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    # Example: Extract basic skills
    skills = ["Python", "JavaScript", "Machine Learning", "SQL", "CSS"]
    found_skills = [skill for skill in skills if skill.lower() in text.lower()]
    return {
        "skills": found_skills,
        "word_count": len(text.split())
    }

@app.route("/analyze", methods=["POST"])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['resume']
    if file and (file.filename.endswith('.pdf') or file.filename.endswith('.docx')):
        # Save the file to the uploads folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        try:
            # Extract and analyze text from the uploaded file
            text = extract_text(file_path)
            if not text.strip():
                return jsonify({"error": "Could not extract text from file"}), 400

            result = analyze_resume(text)
            return jsonify(result)

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

        finally:
            # Clean up by removing the uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)

    return jsonify({"error": "Unsupported file format"}), 400


if __name__ == "__main__":
    app.run(debug=True)
