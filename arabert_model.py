from transformers import pipeline

sentiment = pipeline("sentiment-analysis",
                     model="aubmindlab/bert-base-arabertv02")

def analyze_sentiment(text):
    result = sentiment(text)
    return result