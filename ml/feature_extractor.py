import re
import ipaddress
import tldextract
from urllib.parse import urlparse


def extract_features(url):

    # Add HTTPS if the user does not provide a scheme
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed_url = urlparse(url)

    # Extract domain information
    extracted = tldextract.extract(url)

    domain = extracted.domain
    suffix = extracted.suffix

    hostname = parsed_url.hostname or ""

    # Count letters, digits and special characters
    letters = sum(char.isalpha() for char in url)
    digits = sum(char.isdigit() for char in url)

    special_chars = sum(
        not char.isalnum() for char in url
    )

    # Check whether domain is an IP address
    try:
        ipaddress.ip_address(hostname)
        is_ip = 1
    except ValueError:
        is_ip = 0

    # Count subdomains
    subdomains = extracted.subdomain.split(".")
    subdomain_count = (
        len([s for s in subdomains if s]) if extracted.subdomain else 0
    )

    # Detect possible URL obfuscation
    obfuscated_chars = len(re.findall(r"%[0-9a-fA-F]{2}", url))

    features = {
        "URLLength": len(url),
        "DomainLength": len(hostname),
        "IsDomainIP": is_ip,
        "TLDLength": len(suffix),
        "NoOfSubDomain": subdomain_count,
        "HasObfuscation": int(obfuscated_chars > 0),
        "NoOfObfuscatedChar": obfuscated_chars,
        "ObfuscationRatio": obfuscated_chars / max(len(url), 1),
        "NoOfLettersInURL": letters,
        "LetterRatioInURL": letters / max(len(url), 1),
        "NoOfDegitsInURL": digits,
        "DegitRatioInURL": digits / max(len(url), 1),
        "NoOfEqualsInURL": url.count("="),
        "NoOfQMarkInURL": url.count("?"),
        "NoOfAmpersandInURL": url.count("&"),
        "NoOfOtherSpecialCharsInURL": special_chars,
        "SpacialCharRatioInURL": special_chars / max(len(url), 1),
        "IsHTTPS": int(parsed_url.scheme == "https")
    }

    return features