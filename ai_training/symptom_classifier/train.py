import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# --- CONFIGURATION ---
DATASET_PATH = 'dataset.csv'
CLASSIFIER_OUTPUT_PATH = '../../backend/triage_service/symptom_classifier_model.pkl'
VECTORIZER_OUTPUT_PATH = '../../backend/triage_service/tfidf_vectorizer.pkl'

# 1. Load Data
print("Loading dataset...")
try:
    df = pd.read_csv(DATASET_PATH)
except FileNotFoundError:
    print(f"Error: Dataset not found at {DATASET_PATH}. Please create it.")
    exit()

# Assuming columns are named 'symptoms' and 'triage_level'
X = df['symptoms']
y = df['triage_level']

# 2. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Create and fit the TF-IDF Vectorizer
print("Fitting vectorizer...")
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 4. Train the Classifier
print("Training Naive Bayes classifier...")
classifier = MultinomialNB()
classifier.fit(X_train_tfidf, y_train)

# 5. Evaluate the model (optional but good practice)
y_pred = classifier.predict(X_test_tfidf)
print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# 6. Save the trained model and vectorizer
print(f"Saving model to {CLASSIFIER_OUTPUT_PATH}")
with open(CLASSIFIER_OUTPUT_PATH, 'wb') as f:
    pickle.dump(classifier, f)

print(f"Saving vectorizer to {VECTORIZER_OUTPUT_PATH}")
with open(VECTORIZER_OUTPUT_PATH, 'wb') as f:
    pickle.dump(vectorizer, f)

print("\nTraining complete. Model and vectorizer are saved and ready.")