import re
from pdfminer.high_level import extract_text
import requests

# Predefined skills
predefined_skills = [
    "Python", "JavaScript", "Java", "C#", "C++", "HTML", "CSS", "React.js",
    "Node.js", "Angular", "SQL", "Docker", "Kubernetes", "Git", "AWS",
    "Azure", "Machine Learning", "TensorFlow", "Scikit-learn", "PyTorch",
    "Data Science", "Terraform", "Ansible", "Linux", "Prometheus", "Grafana",
    "CloudFormation", "Nagios", "Jenkins", "Shell Script", "Bash", "AgroCD"
]

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

# Function to clean and normalize text
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Normalize multiple spaces
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
    text = re.sub(r'\s*-\s*', ' ', text)  # Fix broken terms like "Shell Script - Bash"
    text = re.sub(r'\bJava\s*Script\b', 'JavaScript', text)  # Fix "Java Script"
    text = re.sub(r'\bTensor\s*Flow\b', 'TensorFlow', text)  # Fix "Tensor Flow"
    return text.strip()

# Function to extract skills
def extract_matching_skills(text):
    matched_skills = []
    text = re.sub(r'\s*[-,;|]\s*', ' ', text)  # Normalize delimiters
    for skill in predefined_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            matched_skills.append(skill)
    return matched_skills

# Function to send skills to the Gemini API
def generate_questions(skills, difficulty="Medium"):
    """
    Send extracted skills to the Gemini API and retrieve generated questions.
    Adjust the questions based on the selected difficulty level.

    Parameters:
    - skills (list): A list of extracted skills.
    - difficulty (str): Difficulty level for the questions (Easy, Medium, Hard).
    """
    api_key = "AIzaSyC1SdomX-1zbJkRMKPI7nf-x3cA0Bl7Bwo"  # Replace with your real API key
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    # Construct the difficulty-based prompt
    prompt = f"Generate {5 if difficulty == 'Hard' else 3} technical interview questions for a {difficulty} role based on the following skills: {', '.join(skills)}"
    if difficulty == "Easy":
        prompt += " The questions should be simple and focused on understanding the basics of each technology."
    elif difficulty == "Medium":
        prompt += " The questions should involve practical scenarios, combining multiple technologies."
    elif difficulty == "Hard":
        prompt += " The questions should involve complex scenarios and require deep technical knowledge and problem-solving."

    # Prepare the payload for the API
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    # Headers for the API request
    headers = {
        "Content-Type": "application/json"
    }

    # Send the API request
    response = requests.post(api_url, json=payload, headers=headers)

    # Print the full response for debugging
    print(f"\n[DEBUG] Full API Response: {response.text}")

    if response.status_code == 200:
        result = response.json()

        # Extract the questions from the API response
        questions = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()

        if questions:
            # Split the questions by newlines and return them as a list
            questions_list = questions.split("\n\n")  # Split questions if they are separated by double newlines
            return questions_list
        else:
            print("No questions found in the response.")
            return []

    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []


# Function to process a resume and generate questions
def process_resume(pdf_path):
    # Step 1: Extract text
    extracted_text = extract_text_from_pdf(pdf_path)
    if not extracted_text:
        print("No text extracted from the resume.")
        return

    # Step 2: Clean text
    cleaned_text = clean_text(extracted_text)
    print("\n[DEBUG] Cleaned Extracted Text:\n", cleaned_text)

    # Step 3: Extract skills
    matched_skills = extract_matching_skills(cleaned_text)
    if matched_skills:
        print("\nExtracted Skills:")
        for skill in matched_skills:
            print(f"- {skill}")
    else:
        print("No skills found in the resume.")
        return

    # Step 4: Generate questions using Gemini API
    print("\nGenerating Questions...")
    questions = generate_questions(matched_skills)
    if questions:
        print("\nGenerated Questions:")
        for question in questions:
            print(f"- {question}")
    else:
        print("No questions generated.")

# Example usage
pdf_path = r"C:\Users\DELL\OneDrive\Desktop\interview related docs\X-c 1.pdf" # Replace with your resume file path
process_resume(pdf_path)
