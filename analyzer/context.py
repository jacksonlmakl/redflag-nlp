import re
import json
from rapidfuzz import process, fuzz

# Load topic weights from JSON
with open("context_config.json") as f:
    TOPIC_WEIGHTS = json.load(f)

def calculate_context_multiplier(text, threshold=80, adjust_factor=4.0):
    """
    Determines a context multiplier (0-1) based on topic severity.
    Uses fuzzy matching, exponential scaling, and severity boosts to ensure
    highly conspiratorial texts get a proper multiplier.
    """
    text = text.lower()  # Normalize text
    scores = []
    matches = []

    for phrase, weight in TOPIC_WEIGHTS.items():
        match, score, _ = process.extractOne(phrase, [text], scorer=fuzz.partial_ratio)
        if score >= threshold:
            scores.append(weight)
            matches.append(phrase)

    if not matches:
        return 0.1  # Baseline neutral multiplier

    total_score = sum(scores)  # Sum of detected topic weights

    # Set max_possible_score dynamically to allow higher severity
    max_possible_score = max(scores) * 1.5  # Reduce suppression effect

    # Apply exponential scaling (boosts texts with few strong matches)
    context_multiplier = min(1, (total_score / max_possible_score) ** adjust_factor)

    # Apply severity boost if any topic is extremely high-risk (≥ 0.9 weight)
    if any(weight >= 0.9 for weight in scores):
        context_multiplier = max(context_multiplier, 0.75)  # Ensure minimum severity impact

    return round(context_multiplier, 4)  # Keep concise precision
