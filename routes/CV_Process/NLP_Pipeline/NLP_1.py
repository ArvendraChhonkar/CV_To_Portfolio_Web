import os
import re
import sys
import json
import logging
import warnings
import spacy
import pdfplumber
import fitz  # PyMuPDF
from docx import Document
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Suppress warnings to keep stdout clean for the Express child process
warnings.filterwarnings("ignore")

# --- Path Configuration ---
# NLP_1.py location: CV_TO_PORTFOLIO_WEB/routes/CV_Process/NLP_Pipeline/NLP_1.py
SCRIPT_PATH = Path(__file__).resolve()
ROOT_DIR = SCRIPT_PATH.parents[3] 

MODEL_PATH = ROOT_DIR / "portfolio_ner_model"
TEMPLATES_DIR = SCRIPT_PATH.parent / "HTML_Templates"
OUTPUT_DIR = ROOT_DIR / "public" / "portfolios"

# Configure logging to hide info messages from Express
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')

def clean_text(text: str) -> str:
    """Normalize extracted resume text for NLP processing."""
    if not text: return ""
    # Normalize quotes, dashes, and bullets
    text = text.replace("\u2013", "-").replace("\u2014", "-").replace("\u2022", "-").replace("\xa0", " ")
    # Remove control characters and multiple spaces
    text = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", text)
    text = re.sub(r"[ ]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def extract_text(file_path: str) -> str:
    """Detects file type and extracts raw text with layout awareness."""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    raw_text = ""

    try:
        if ext == ".pdf":
            try:
                with pdfplumber.open(file_path) as pdf:
                    raw_text = "\n".join([p.extract_text(x_tolerance=2) or "" for p in pdf.pages])
            except Exception:
                with fitz.open(file_path) as doc:
                    raw_text = "\n".join([page.get_text("text", sort=True) for page in doc])
        elif ext == ".docx":
            doc = Document(file_path)
            raw_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
    except Exception as e:
        logging.error(f"Extraction error: {e}")
    
    return clean_text(raw_text)

def refine_entities(text, user_data):
    """
    Refines extraction by prioritizing the top-of-page name 
    and aggressive project sectioning.
    """
    # 1. NAME FIX: Take the first two words of the first non-empty line
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if lines:
        first_line = lines[0]
        words = first_line.split()
        if len(words) >= 2:
            # Join the first two words (e.g., "Aman Yadav")
            user_data["NAME"] = f"{words[0]} {words[1]}"
        elif len(words) == 1:
            user_data["NAME"] = words[0]
    
    # 2. PROJECT EXTRACTION: Fuzzy search for section start/end
    # Matches lines containing 'Projects' regardless of leading numbers or icons
    start_pattern = r'(?im)^.*(projects?|key achievements|selected works|technical projects)\b.*$'
    # Boundaries to stop extraction
    end_pattern = r'(?im)^.*(experience|work experience|employment|education|skills|certifications|links|hobbies)\b.*$'
    
    start_match = re.search(start_pattern, text, re.MULTILINE)
    if start_match:
        start_idx = start_match.end()
        remaining = text[start_idx:]
        end_match = re.search(end_pattern, remaining, re.MULTILINE)
        if end_match:
            user_data["PROJECTS"] = remaining[:end_match.start()].strip()
        else:
            user_data["PROJECTS"] = remaining.strip()
    else:
        user_data["PROJECTS"] = "Project details available upon request."
        
    return user_data

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No file path provided"}))
        sys.exit(1)

    input_file = sys.argv[1]
    # template_idx passed from Express (0-3)
    try:
        template_idx = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    except (ValueError, IndexError):
        template_idx = 0

    try:
        # 1. Extraction & NLP Processing
        extracted_text = extract_text(input_file)
        nlp = spacy.load(MODEL_PATH)
        doc = nlp(extracted_text)

        # Initialize data structure
        user_data = {
            "NAME": "", "EMAIL": "", "PHONE": "", "GITHUB": "", "LINKEDIN": "",
            "SKILLS": [], "JOB_TITLE": [], "COMPANY": [], "EDUCATION": [], "UNIVERSITY": []
        }

        # Populate entities from model
        for ent in doc.ents:
            label = ent.label_
            if label in ["SKILLS", "JOB_TITLE", "COMPANY", "EDUCATION", "UNIVERSITY"]:
                if ent.text not in user_data[label]:
                    user_data[label].append(ent.text)
            elif label in user_data:
                user_data[label] = ent.text

        # 2. Apply Refinements (Name Fallback & Project Section)
        user_data = refine_entities(extracted_text, user_data)

        # 3. HTML Generation Setup
        template_map = ["modern.html", "minimal.html", "creative.html", "dark.html"]
        selected_template = template_map[template_idx % len(template_map)]

        env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=select_autoescape(['html'])
        )
        
        template = env.get_template(selected_template)
        # Pass both 'user' and 'data' for template variable compatibility
        html_content = template.render(user=user_data, data=user_data)

        # 4. Save and Output Path for Express
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        # Generate safe filename from name
        safe_name = re.sub(r'\W+', '', user_data["NAME"].lower())
        output_filename = f"{safe_name}_{template_idx}.html"
        final_path = OUTPUT_DIR / output_filename

        with open(final_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Success: Output ONLY the path for Node.js child_process to capture
        print(str(final_path))

    except Exception as e:
        # Error: Output JSON for Node.js to handle
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()