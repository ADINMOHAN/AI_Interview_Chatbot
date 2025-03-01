from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased")

def analyze_sentiment(answer):
    result = sentiment_analyzer(answer)
    return result[0]

if __name__ == "__main__":
    response = "I am highly skilled in Python and Machine Learning."
    print(analyze_sentiment(response))
