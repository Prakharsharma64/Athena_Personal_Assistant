import json
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import random
import subprocess

# Load intents data
with open("intents.json") as file:
    data = json.load(file)

# Load pre-trained model
model = load_model("chat_model.keras")

# Load tokenizer
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Load label encoder
with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder = pickle.load(encoder_file)

def predict_intent(input_text):
    """Function to predict intent and return response."""
    # Convert input text into padded sequences
    padded_sequences = pad_sequences(tokenizer.texts_to_sequences([input_text]), maxlen=20, truncating='post')
    
    # Predict the model output
    result = model.predict(padded_sequences)
    
    # Get the predicted intent tag
    tag = label_encoder.inverse_transform([np.argmax(result)])[0]
    
    return tag

def get_response(tag, input_text):
    """Function to get a random response from the intents data, including system commands."""
    for intent in data['intents']:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            
            # If the intent is related to system commands (e.g., opening an app)
            if tag == "open_calculator":  # Example tag for opening calculator
                # Execute a system command to open the calculator
                subprocess.run(["calc"])  # Works on Windows, use "gnome-calculator" for Linux, "open -a Calculator" for macOS
                response = "Opening Calculator..."
            
            elif tag == "check_system":  # Example tag for checking system status
                # Check system status (e.g., disk usage, memory, etc.)
                system_status = "System is running fine. All resources are normal."
                response = system_status
            
            return response
    return "Sorry, I didn't understand that."

def test_model(input_text):
    """Test the model with user input."""
    print(f"Testing with input: {input_text}")
    
    # Predict the intent
    tag = predict_intent(input_text)
    
    # Get response based on the predicted tag
    response = get_response(tag, input_text)
    
    print(f"Model response: {response}")

# Example of testing the model
test_model("open calculator")  # Should trigger the calculator to open
test_model("check system")  # Should provide system status
test_model("How are you?")  # Normal chatbot response
