import spacy
import PyPDF2

nlp = spacy.load("en_core_web_sm")

def extract_resume_text(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = " ".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
    return text

def extract_entities(text):
    doc = nlp(text)
    entities = {ent.label_: ent.text for ent in doc.ents}
    return entities

if __name__ == "__main__":
    resume_text = extract_resume_text("../data/sample_resume.pdf")
    print(extract_entities(resume_text))
