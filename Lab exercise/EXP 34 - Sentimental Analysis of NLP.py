
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Sample dataset
texts = [
    "I love this product",
    "This is amazing",
    "The experience is wonderful",
    "I am very happy",
    "Excellent service",
    "I hate this product",
    "This is terrible",
    "Very bad experience",
    "I am disappointed",
    "Worst service ever",
    "The product is okay",
    "It is an average experience",
    "Nothing special",
    "The service is normal",
    "It is neither good nor bad"
]

labels = [
    "Positive", "Positive", "Positive", "Positive",
    "Positive", "Negative", "Negative", "Negative",
    "Negative", "Negative", "Neutral", "Neutral",
    "Neutral", "Neutral", "Neutral"
]

# Convert text into numerical features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.2, random_state=42,
    stratify=labels
)

# Create and train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict test data
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Actual Sentiments:", list(y_test))
print("Predicted Sentiments:", list(y_pred))
print("Accuracy:", accuracy * 100, "%")

# Test a new sentence
new_text = ["This product is very excellent"]

new_features = vectorizer.transform(new_text)

prediction = model.predict(new_features)

print("Input Text:", new_text[0])
print("Predicted Sentiment:", prediction[0])
