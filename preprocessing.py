"""Preprocessing logic used into Kialo data.
"""
import re
import nltk
import string
from collections import Counter

try:
    nltk.data.find('corpus/stopwords')
except LookupError:
    nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = Counter(stopwords.words('english')) # reduces complexity of stopword removal to ~O(1) with Counter


def clean_text(text, lower=True, markdown=True, punctuation=True, stopwords=True) -> str:
    """Removes Markdown links and NLP-standard formattings from `text`.
    """
    clean_text = text.replace('\\', '')

    if lower:
        clean_text = clean_text.lower()
    if markdown:
        clean_text = re.sub(r'\[(.*)\]\(http[s]{0,}:.*\)', r'\1', clean_text)
    if punctuation:
        clean_text = clean_text.translate(str.maketrans('', '', string.punctuation))
    if stopwords:
        clean_text = ' '.join([word for word in clean_text.split() if word not in stop_words])
    
    return clean_text.strip()