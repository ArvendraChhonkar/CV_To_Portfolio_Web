# CV to Portfolio Web

A Node.js and Express-based web application that automates the conversion of resumes into structured web portfolios. The system utilizes Python-based Natural Language Processing (NLP) to extract entities from uploaded documents and maps them to HTML templates.

---

## Core Features

* **Document Upload**: Supports PDF and DOCX resume formats.
* **Automated Extraction**: Uses Spacy-based Named Entity Recognition (NER) to identify key resume sections.
* **Template Engine**: Employs Jinja2 and HTML tag-based updates to populate portfolio layouts.
* **Asynchronous Processing**: Uses Node.js child processes to execute Python scripts for data extraction.
* **Multiple Themes**: Includes several HTML templates (Creative, Dark, Minimal, Modern) for the generated output.

---

## Requirements and Tech Stack

### Backend
* **Node.js & Express**: Primary web server and routing.
* **Pug (Jade)**: View engine for the web interface.

### Data Processing
* **Python 3.x**: Core processing language.
* **Spacy**: NLP library used for Named Entity Recognition.
* **Jinja2**: Templating engine for generating HTML files.
* **Child Process**: Node.js module used to bridge the JavaScript and Python environments.

---

## Installation Instructions

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd CV_TO_PORTFOLIO_WEB
    ```

2.  **Install Node.js Dependencies**
    ```bash
    npm install
    ```

3.  **Setup Python Environment**
    Ensure you have Python 3 installed. Install the necessary NLP and templating libraries:
    ```bash
    pip install spacy jinja2
    python -m spacy download en_core_web_sm
    ```

4.  **Run the Application**
    ```bash
    npm start
    ```
    The server typically runs on `http://localhost:3000`.

---

## Basic Usage

1.  **Upload**: Navigate to the upload route and select a `.pdf` or `.docx` file.
2.  **Processing**: The application saves the file to the `/uploaded` directory. `app.js` triggers `routes/CV_Process/NLP_Pipeline/NLP_1.py` via a child process.
3.  **NER Extraction**: `NLP_1.py` parses the text and identifies entities.
4.  **Generation**: The system merges the extracted data into a selected template from `routes/CV_Process/NLP_Pipeline/HTML_Templates`.
5.  **View**: The final portfolio is saved to `public/portfolios/` and can be accessed via the browser.

### Project Structure Overview
The core logic for NLP extraction is located in: 
`routes/CV_Process/NLP_Pipeline/NLP_1.py`

---

## License and Contribution

### Current Limitations
The current Spacy NER model may have difficulty consistently identifying specific project titles or unique names due to the high variability in resume formatting.

### Future Roadmap
* Migration from local NER models to LLM APIs (GPT or Gemini) for higher extraction accuracy.
* Improved CSS styling for generated portfolios.

### Contributing
Contributions are welcome to improve the extraction accuracy or add new templates. Please fork the repository and submit a pull request with a detailed description of your changes.

This project is licensed under the **MIT License**.



# NOTE - the css and the html-templates are AI generated and some of the python script is refined using AI .
