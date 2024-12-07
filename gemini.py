import re
from pdfminer.high_level import extract_text

# Predefined skills to match
predefined_skills = [
    "Python", "JavaScript", "Java", "C#", "C++", "HTML", "CSS", "React.js",
    "Node.js", "Angular", "SQL", "Docker", "Kubernetes", "Git", "AWS",
    "Azure", "Machine Learning", "TensorFlow", "Scikit-learn", "PyTorch",
    "Data Science", "Terraform", "Ansible", "Linux", "Prometheus", "Grafana",
    "CloudFormation", "Nagios", "Jenkins", "Shell Script", "Bash", "AgroCD"
]

def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF using PDFMiner.
    """
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def clean_text(text):
    """
    Normalize text by fixing spaces, punctuation, and formatting issues.
    """
    text = re.sub(r'\s+', ' ', text)  # Normalize multiple spaces
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
    text = re.sub(r'\s*-\s*', ' ', text)  # Fix broken terms like "Shell Script- Bash"
    text = re.sub(r'\bJava\s*Script\b', 'JavaScript', text)  # Fix "Java Script"
    text = re.sub(r'\bTensor\s*Flow\b', 'TensorFlow', text)  # Fix "Tensor Flow"
    return text.strip()

def extract_matching_skills(text):
    """
    Match predefined skills in the text.
    """
    matched_skills = []
    text = re.sub(r'\s*[-,;|]\s*', ' ', text)  # Normalize delimiters
    for skill in predefined_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            matched_skills.append(skill)
    return matched_skills

def process_resume(pdf_path):
    """
    Process the resume to extract skills.
    """
    # Extract text
    extracted_text = extract_text_from_pdf(pdf_path)
    if not extracted_text:
        print("No text extracted from the resume.")
        return

    # Clean text
    cleaned_text = clean_text(extracted_text)
    print("\n[DEBUG] Cleaned Extracted Text:\n", cleaned_text)

    # Match skills across the entire resume
    matched_skills = extract_matching_skills(cleaned_text)
    if matched_skills:
        print("\nExtracted Skills:")
        for skill in matched_skills:
            print(f"- {skill}")
    else:
        print("No skills found in the resume.")

# Example usage
pdf_path = r"C:\Users\DELL\OneDrive\Desktop\interview related docs\X-c 1.pdf"  # Adjust path to match the uploaded resume
process_resume(pdf_path)
