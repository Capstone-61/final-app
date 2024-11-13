import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("Melvinjj/bert_results")

# Define event labels for decoding
event_labels = {
    0: 'free kick',
    1: 'foul',
    2: 'goal',
    3: 'corner',
    4: 'substitution',
    5: 'offside',
    6: 'yellow card',
    7: 'handball',
    8: 'penalty',
    9: 'red card'
}

csv_path = 'Port_vs_Spain2_audio.csv'

# Load the CSV file
df = pd.read_csv(csv_path)  # Update with the correct file path if needed

# Function to classify context text
def classify_event(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    return event_labels.get(predicted_class, "Unknown")

# Apply the function to each row in the 'Context' column
df['Predicted Event'] = df['Context'].apply(classify_event)

event_category_map = {
    'goal': 'Goals and Scoring Opportunities',
    'penalty': 'Goals and Scoring Opportunities',
    'foul': 'Fouls and Infractions',
    'yellow card': 'Fouls and Infractions',
    'red card': 'Fouls and Infractions',
    'handball': 'Fouls and Infractions',
    'free kick': 'Set Pieces',
    'corner': 'Set Pieces',
    'substitution': 'Game Management',
    'offside': 'Game Management'
}

# Map the Predicted Event to a broader category
df['Event Category'] = df['Predicted Event'].map(event_category_map)

# Save the results to a new CSV file
df.to_csv(csv_path, index=False)

print("Classification complete. Output saved ")
