import joblib

# Load trained URL model
model = joblib.load("ml/phishguard_url_model.pkl")

# Function to predict a URL
def check_url(url):

    prediction = model.predict([url])[0]

    probabilities = model.predict_proba([url])[0]

    # Get phishing probability
    phishing_probability = probabilities[
        list(model.classes_).index(0)
    ]

    print("\nURL:", url)

    if prediction == 0:
        print("Result: PHISHING URL")
    else:
        print("Result: LEGITIMATE URL")

    print(
        "Phishing probability:",
        round(phishing_probability * 100, 2),
        "%"
    )


# Test URLs
check_url("https://www.google.com")

check_url("http://paypal-login-security-example.com")

check_url("https://www.wikipedia.org")