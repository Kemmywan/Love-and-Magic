import fitz  # PyMuPDF
import sys

def extract_annotations(pdf_path):
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc[page_num]
        annots = page.annots()
        if annots is None:
            continue
        for annot in annots:
            print(f"Page {page_num + 1}:")
            print(f"Type: {annot.type[1]}")
            print(f"Content: {annot.info.get('content', '')}")
            print('-' * 40)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <filename.pdf>")
        sys.exit(1)
    extract_annotations(sys.argv[1])