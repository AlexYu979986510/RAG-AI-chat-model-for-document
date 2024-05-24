"""
Created on Thu Apr 30 16:54:26 2024

@author: AlexYu
"""

#%%  
"""
Converts all PDF files in a folder to txt files
"""
import os
from pdfminer.high_level import extract_text
import re
import logging

# Setting up logging to output the status of file conversion
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def pdf_to_markdown(pdf_path):
    try:
        text = extract_text(pdf_path)
        markdown_text = re.sub(r'\n{2,}', '\n\n', text)  # Ensure proper paragraph spacing
        markdown_text = re.sub(r'\n', ' ', markdown_text)  # Convert single newlines into spaces
        markdown_text = re.sub(r'\s{2,}', ' ', markdown_text)  # Remove extra spaces
        return markdown_text
    except Exception as e:
        logging.error(f"Failed to process {pdf_path}: {e}")
        return None

def convert_folder_to_markdown(pdf_dir):
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)
            txt_path = pdf_path.replace('.pdf', '.txt')

            # Check if the txt file already exists
            if os.path.exists(txt_path):
                logging.info(f"Skipping conversion, text file already exists: {txt_path}")
                continue  # Skip this file as it has already been converted

            markdown_text = pdf_to_markdown(pdf_path)
            if markdown_text is not None:
                try:
                    with open(txt_path, 'w', encoding='utf-8') as md_file:
                        md_file.write(markdown_text)
                    logging.info(f"Converted {pdf_path} to {txt_path}")
                except Exception as e:
                    logging.error(f"Could not write to {txt_path}: {e}")

# Specify the folder containing PDFs
pdf_dir = r"your file location"
convert_folder_to_markdown(pdf_dir)
