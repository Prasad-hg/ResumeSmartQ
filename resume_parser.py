import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
import re

def extract_text_from_image(image_path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()
    return extracted_text

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
    return text.strip()
def extract_section_info(text, section_name):
    """
    Extracts text from a specific section (e.g., "Skills", "Projects") by identifying section headers.
    """
    # Updated pattern to handle variations in section headers
    section_pattern = re.compile(rf'\b(?:{section_name}|technical {section_name}|key {section_name})\b[\s:]*', re.IGNORECASE)
    next_section_pattern = re.compile(r'\b(?:skills|projects|education|experience|summary|interests|languages|certifications|achievements)\b', re.IGNORECASE)

    section_start = section_pattern.search(text)
    if not section_start:
        print(f"No section found for: {section_name}")
        return ""  # Return empty if section header is not found

    start_index = section_start.end()
    subsequent_text = text[start_index:]

    next_section_start = next_section_pattern.search(subsequent_text)
    if next_section_start:
        end_index = next_section_start.start()
        return subsequent_text[:end_index].strip()

    return subsequent_text.strip()

def extract_skills_and_projects(text):
    """
    Extract skills and projects sections dynamically.
    """
    skills_text = extract_section_info(text, "skills")
    projects_text = extract_section_info(text, "projects")

    # Debug: Print the raw extracted sections
    print("\n[DEBUG] Skills Section Text:\n", skills_text)
    print("\n[DEBUG] Projects Section Text:\n", projects_text)

    # Clean and split the skills into a list
    skills = [skill.strip() for skill in re.split(r'[,\n-•]', skills_text) if skill.strip()]

    # Clean and split the projects into a list
    projects = [project.strip() for project in re.split(r'[,\n-•|]', projects_text) if project.strip()]

    # Fallback handling
    if not skills:
        print("\nNo skills found. Please verify the resume formatting.")
    if not projects:
        print("\nNo projects found. Please verify the resume formatting.")

    return skills, projects

def process_resume(image_path=None, pdf_path=None):
    extracted_text = ""
    if image_path:
        extracted_text = extract_text_from_image(image_path)
    elif pdf_path:
        extracted_text = extract_text_from_pdf(pdf_path)
    else:
        print("No valid file path provided!")
        return

    if not extracted_text.strip():
        print("No text extracted from the file. Please check the input file.")
        return

    # Debug: Print raw extracted text
    print("\n[DEBUG] Raw Extracted Text:\n", extracted_text)

    cleaned_text = clean_text(extracted_text)
    skills, projects = extract_skills_and_projects(cleaned_text)

    print("\nExtracted Skills:")
    for skill in skills:
        print(f"- {skill}")

    print("\nExtracted Projects:")
    for project in projects:
        print(f"- {project}")

# Example usage
image_path = r"E:\nlp_project\resume.png"
pdf_path = r"C:\Users\DELL\OneDrive\Desktop\interview related docs\prasadhgresume2024.pdf"
process_resume(pdf_path=pdf_path)
