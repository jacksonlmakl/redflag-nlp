import re
from urllib.parse import urlparse
import pandas as pd 

def fraud_analysis(text):
    """
    Extracts phone numbers, emails, and external URLs from a given text.
    The function also detects obfuscated URLs (e.g., spaces in 'h t t p s ://example.com').

    Returns a dictionary containing lists of detected phone numbers, emails, and URLs.
    """

    # Improved regex for phone numbers (supports US + international formats + plain 10-digit numbers)
    phone_pattern = re.compile(
        r"(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}|\b\d{10}\b"
    )

    # Regular expression for email addresses
    email_pattern = re.compile(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    )

    # Regular expression for URLs (detects standard and obfuscated ones)
    url_pattern = re.compile(
        r"(?:https?://|www\.)[^\s]+|(?:h[\s]*t[\s]*t[\s]*p[\s]*s?[\s]*:[\s]*/[\s]*/[\s]*[a-zA-Z0-9.-]+)"
    )

    # Find all matches in text
    phone_numbers = phone_pattern.findall(text)
    emails = email_pattern.findall(text)
    urls = url_pattern.findall(text)

    # Clean up URLs (remove spaces and normalize formatting)
    cleaned_urls = []
    for url in urls:
        url = re.sub(r"\s+", "", url)  # Remove spaces within URL
        parsed_url = urlparse(url)
        if parsed_url.scheme == "":  # If no scheme, assume it's HTTP
            url = "http://" + url
        cleaned_urls.append(url)

    df= pd.DataFrame([{
        "phone_numbers": list(set(phone_numbers)) if len(phone_numbers) > 0 else float('nan'),  # Remove duplicates
        "emails": list(set(emails)) if len(emails) > 0 else float('nan'),  # Remove duplicates
        "urls": list(set(cleaned_urls)) if len(cleaned_urls) > 0 else float('nan'),  # Remove duplicates
    }])
    df=df.dropna()
    return df 
