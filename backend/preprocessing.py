import re


def preprocess_text(text: str) -> str:
    """
    Clean and normalize submission text
    before plagiarism analysis.
    """

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation and special characters
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()