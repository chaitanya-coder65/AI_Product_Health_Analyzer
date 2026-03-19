import re
from rapidfuzz import process


def clean_ocr_text(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z ]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text


def extract_tokens(text):

    tokens = text.split(" ")

    tokens = [t.strip() for t in tokens if len(t.strip()) > 3]

    return tokens


# 🔥 NEW: SPELL CORRECTION FUNCTION
def correct_spelling(tokens, ingredient_list):

    corrected = []

    for token in tokens:

        match, score, _ = process.extractOne(token, ingredient_list)

        # only accept strong matches
        if score >= 85:
            corrected.append(match)
        else:
            corrected.append(token)

    return corrected


# 🔥 NEW: REBUILD CLEAN TEXT
def rebuild_text(tokens):

    return " ".join(tokens)