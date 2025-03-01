from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def generate_questions(job_description):
    questions = [
        f"What experience do you have in {job_description}?",
        f"How have you applied {job_description} in your past work?",
        f"What challenges have you faced while working with {job_description}?"
    ]
    return questions

if __name__ == "__main__":
    job_desc = "Machine Learning Engineer with Python & NLP experience"
    print(generate_questions(job_desc))
