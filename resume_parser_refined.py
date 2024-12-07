import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


# Function to extract text from an image using Tesseract OCR
def extract_text_from_image(image_path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    image = Image.open(image_path)
    return pytesseract.image_to_string(image, config="--psm 6")


# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()
    return extracted_text


# Function to clean the extracted text
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
    return text.strip()


# Function to fix common OCR errors like word splits
def fix_ocr_errors(text):
    # Correct common OCR issues like split words (e.g., 'P R A S A D' -> 'PRASAD')
    text = re.sub(r'\b([A-Za-z])\s+([A-Za-z])\b', r'\1\2', text)  # Merge split words
    text = re.sub(r'\b([A-Za-z])\s+\b([A-Za-z])\b', r'\1\2', text)  # Handle extra spaces between words
    text = re.sub(r'\s(\d+)\s', r'\1', text)  # Fix digits separated by spaces
    return text


# Function to extract only the Skills section
def extract_skills_section(text):
    """
    Extracts the Skills section using variations like 'Technical Skills', 'Core Skills', etc.
    """
    skills_headers = [
        "skills", "technical skills", "technologies", "soft skills", "core skills", "key skills"
    ]

    skills_pattern = re.compile(
        rf'\b(?:{"|".join(skills_headers)})\b[\s:]*', re.IGNORECASE
    )

    next_section_pattern = re.compile(
        r'\b(?:projects|education|experience|summary|interests|languages|certifications|achievements)\b',
        re.IGNORECASE
    )

    section_start = skills_pattern.search(text)
    if not section_start:
        return ""

    start_index = section_start.end()
    subsequent_text = text[start_index:]

    next_section_start = next_section_pattern.search(subsequent_text)
    if next_section_start:
        end_index = next_section_start.start()
        return subsequent_text[:end_index].strip()

    return subsequent_text.strip()


# Function to process the resume and extract the Skills section
def process_resume(image_path=None, pdf_path=None):
    extracted_text = ""
    if image_path:
        extracted_text = extract_text_from_image(image_path)
    elif pdf_path:
        extracted_text = extract_text_from_pdf(pdf_path)
    else:
        print("No valid file path provided!")
        return

    if not extracted_text:
        print("No text extracted from the file. Please check the input file.")
        return

    # Fix common OCR errors and clean the text
    fixed_text = fix_ocr_errors(extracted_text)
    cleaned_text = clean_text(fixed_text)
    print("[DEBUG] Cleaned Text:\n", cleaned_text[:500])  # Optional: Preview first 500 characters

    # Extract the skills section
    skills_section = extract_skills_section(cleaned_text)
    if skills_section:
        print("\n--- Extracted Skills Section ---")
        print(skills_section)
    else:
        print("\nNo Skills Section Found.")


# Example usage


# Example usage
pdf_path =  r"E:\nlp_project\X-c 1.pdf" # Replace with your uploaded file path
process_resume(pdf_path=pdf_path)
