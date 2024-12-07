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


def extract_skills_section(text):
    """
    Extract the skills section based on capitalized headers like 'SKILLS' or 'TECHNICAL SKILLS'.
    """
    # Look for capitalized headers (e.g., 'SKILLS', 'TECHNICAL SKILLS', etc.)
    skill_headers = r"\b(?:SKILLS|TECHNICAL SKILLS|CORE SKILLS|SOFT SKILLS)\b"
    next_section_headers = r"(experience|projects|education|summary|languages|certifications)"

    # Search for the start of the skills section
    section_pattern = re.compile(skill_headers, re.IGNORECASE)
    section_start = section_pattern.search(text)

    if not section_start:
        print("Skills section not found.")
        return ""

    # Extract content from the start of the skills section until the next section header
    start_index = section_start.end()
    subsequent_text = text[start_index:]

    # Debug: Print the text immediately after the skills header to inspect content
    print("\n[DEBUG] Text After Skills Header:\n", subsequent_text)

    # Stop capturing when another section starts
    next_section_start = re.search(next_section_headers, subsequent_text, re.IGNORECASE)
    if next_section_start:
        end_index = next_section_start.start()
        skills_section = subsequent_text[:end_index].strip()
    else:
        skills_section = subsequent_text.strip()

    return skills_section


def clean_skills_text(skills_text):
    """Clean and split the extracted skills text into a list."""
    # Split skills by commas, newlines, or bullet points and remove extra spaces
    skills = re.split(r'[,\n-•|]', skills_text)
    skills = [skill.strip() for skill in skills if skill.strip()]  # Clean and remove empty skills
    return skills


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

    # Clean the extracted text
    cleaned_text = clean_text(extracted_text)

    # Extract the skills section
    skills_section = extract_skills_section(cleaned_text)

    if not skills_section:
        print("No skills section found.")
        return

    # Clean the skills section text and split into individual skills
    skills = clean_skills_text(skills_section)

    print("\nExtracted Skills:")
    for skill in skills:
        print(f"- {skill}")


# Example usage
image_path = r"E:\nlp_project\resume.png"
pdf_path = r"C:\Users\DELL\OneDrive\Desktop\interview related docs\prasadhgresume2024.pdf"
process_resume(pdf_path=pdf_path)
