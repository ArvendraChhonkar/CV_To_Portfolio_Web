Contributing to CV to Portfolio Web
Thank you for your interest in contributing to this project. This document outlines the process for proposing changes and improving the accuracy of the resume-to-portfolio pipeline.

How to Contribute
1. Reporting Issues
If you find a bug or have a suggestion for improving the NLP extraction, please open an Issue.

Provide a clear description of the problem.

If the extraction failed, include the file format (.pdf or .docx) and the specific entities (e.g., Name, Projects) that were missed.

2. Improving NLP Accuracy
The current system relies on NLP_1.py located in routes/CV_Process/NLP_Pipeline/. As noted in the project overview, the Spacy-based NER model currently struggles with the high variability of project names and unique naming conventions.

High-priority areas for contribution:

Custom NER Training: Updating the Spacy model with annotated datasets to better recognize project blocks.

LLM Integration: Replacing the local NLP_1.py logic with an API call to Gemini or ChatGPT for more robust contextual understanding.

Regex Fallbacks: Implementing pattern matching to catch common resume headers that the NER model might miss.

3. Adding Templates
If you wish to add new portfolio designs:

Create a new .html file in routes/CV_Process/NLP_Pipeline/HTML_Templates/.

Use standard Jinja2 syntax for variable injection (e.g., {{ name }}, {{ projects }}).

Ensure the CSS remains compatible with the generation logic in the CV_Process route.

Development Workflow
Fork the Repository: Create a personal fork on GitHub.

Create a Branch: Use a descriptive name (e.g., feature/gemini-api-integration or fix/name-extraction).

Local Testing:

Ensure all Node.js and Python dependencies are installed.

Run npm start and verify that the NLP_1.py script executes correctly via the child process.

Submit a Pull Request:

Describe the changes in detail.

Explain how the change improves the accuracy or functionality of the project.

Code of Conduct
Maintain professional communication in all interactions.

Focus on technical accuracy and utility.

Ensure all new code follows the existing directory structure and naming conventions.

Recognition
All contributors who help move this project toward a "real-world working" state will be credited in the main README.