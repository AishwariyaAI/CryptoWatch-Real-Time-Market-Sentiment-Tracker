from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis"
)

def analyze_sentiment(text):

    result = classifier(text[:512])

    return result[0]['label']