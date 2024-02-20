# Importing necessary modules
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re

# Download NLTK resources
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Load the training dataset
train_df = pd.read_csv('G:/Pratik Profile PC/Desktop/PRODIGY INFOTECH INTERNSHIP TASKS/TASK_04/twitter_training.csv')
validation_df = pd.read_csv('G:/Pratik Profile PC/Desktop/PRODIGY INFOTECH INTERNSHIP TASKS/TASK_04/twitter_validation.csv')

train_df.columns=['id','information','type','text']
train_df.head()

validation_df.columns=['id','information','type','text']
validation_df.head()

train_df.shape

validation_df.shape

# Check for missing values in the training dataset
print("Missing values in Training Dataset:")
print(train_df.isnull().sum())

# Check for missing values in the validation dataset
print("Missing values in Validation Dataset:")
print(validation_df.isnull().sum())

train_df = train_df.dropna(subset=['text'])

# Check for missing values in the training dataset
print("Missing values in Training Dataset:")
print(train_df.isnull().sum())

train_df.shape

train_df.info()

# Check the distribution of Emotion
train_df['type'].value_counts()

import matplotlib.pyplot as plt

# Check the distribution of the 'type' column
type_counts = train_df['type'].value_counts()

# Define colors for each emotion type
colors = ['skyblue', 'lightcoral', 'lightgreen', 'orange']

# Plotting a pie chart
plt.figure(figsize=(8, 8))
plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
plt.title('Distribution of Emotion Types')
plt.show()

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# Download NLTK resources if not already downloaded
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Function for text preprocessing
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and links
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenization and removing stopwords
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)

# Apply the preprocess_text function to the 'text' column
train_df['preprocessed_text'] = train_df['text'].apply(preprocess_text)
train_df

# Apply the preprocess_text function to the 'text' column
validation_df['preprocessed_text'] = validation_df['text'].apply(preprocess_text)
validation_df

from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize the TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=5000)  # You can adjust the 'max_features' parameter based on your dataset

# Fit and transform the training data
tfidf_train_features = tfidf_vectorizer.fit_transform(train_df['preprocessed_text'])

# Transform the validation data using the same vectorizer
tfidf_validation_features = tfidf_vectorizer.transform(validation_df['preprocessed_text'])

# Display the shape of the TF-IDF features
print(f"TF-IDF Training Features Shape: {tfidf_train_features.shape}")
print(f"TF-IDF Validation Features Shape: {tfidf_validation_features.shape}")

from sklearn.preprocessing import LabelEncoder

# Initialize the LabelEncoder
label_encoder = LabelEncoder()

# Encode the class labels in both training and validation datasets
train_labels_encoded = label_encoder.fit_transform(train_df['type'])
validation_labels_encoded = label_encoder.transform(validation_df['type'])

####
import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Initialize the XGBoost classifier
xgb_classifier = xgb.XGBClassifier()

# Train the classifier on the TF-IDF training features and encoded labels
xgb_classifier.fit(tfidf_train_features, train_labels_encoded)

# Predict the encoded labels for the TF-IDF validation features
validation_predictions_xgb_encoded = xgb_classifier.predict(tfidf_validation_features)

# Decode the predicted labels back to the original class labels
validation_predictions_xgb = label_encoder.inverse_transform(validation_predictions_xgb_encoded)

# Evaluate the performance of the XGBoost classifier
accuracy_xgb = accuracy_score(validation_df['type'], validation_predictions_xgb)
print(f"XGBoost Accuracy: {accuracy_xgb:.2f}")

####
# Display additional classification metrics for XGBoost
print("XGBoost Classification Report:")
print(classification_report(validation_df['type'], validation_predictions_xgb))

# Display the confusion matrix for XGBoost
print("XGBoost Confusion Matrix:")
print(confusion_matrix(validation_df['type'], validation_predictions_xgb))

####
# Assuming you have defined the preprocess_text function

# Example user input
user_input = "Platinum is the best loot @Borderlands"

# Preprocess the user input
user_input_processed = preprocess_text(user_input)

# Vectorize the user input using TF-IDF
user_input_tfidf = tfidf_vectorizer.transform([user_input_processed])

# Predict the sentiment type using the trained XGBoost model
prediction_encoded = xgb_classifier.predict(user_input_tfidf)[0]

# Decode the predicted label back to the original class label
predicted_type = label_encoder.inverse_transform([prediction_encoded])[0]

print(f"The predicted type for the input text is: {predicted_type}")

####
# Example user input
user_input = "This is shitty. I get that profit-wise it was less business expected prior to a huge problem."

# Preprocess the user input
user_input_processed = preprocess_text(user_input)

# Vectorize the user input using TF-IDF
user_input_tfidf = tfidf_vectorizer.transform([user_input_processed])

# Predict the sentiment type using the trained XGBoost model
prediction_encoded = xgb_classifier.predict(user_input_tfidf)[0]

# Decode the predicted label back to the original class label
predicted_type = label_encoder.inverse_transform([prediction_encoded])[0]

print(f"The predicted type for the input text is: {predicted_type}")