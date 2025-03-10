import cv2
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import filedialog

# Load pre-trained model (MobileNetV2 for simplicity)
model = tf.keras.applications.MobileNetV2(weights="imagenet")

def preprocess_image(image_path):
    """Preprocess the image to fit the model's input format."""
    # Load the image
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Resize the image to fit the model input size (224x224 for MobileNetV2)
    img_resized = cv2.resize(img_rgb, (224, 224))
    
    # Preprocess the image for MobileNetV2
    img_preprocessed = tf.keras.applications.mobilenet_v2.preprocess_input(np.expand_dims(img_resized, axis=0))
    
    return img, img_resized, img_preprocessed

def detect_damage(image_path):
    """Detect damage in the car image and mark the damaged areas."""
    img, img_resized, img_preprocessed = preprocess_image(image_path)
    
    # Make a prediction
    predictions = model.predict(img_preprocessed)
    
    # Decode the predictions
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
    
    print(f"Top predictions: {decoded_predictions}")
    
    # Simple damage detection logic (in reality, this should be based on a custom model)
    damage_detected = False
    for _, label, _ in decoded_predictions:
        if 'car' in label.lower():  # Check if any prediction involves a car
            damage_detected = True

    # If damage is detected, mark the area (this is a simplified version)
    if damage_detected:
        print("Damage detected! Marking the damage areas...")

        # Simulated damage marking (adjust the coordinates dynamically)
        # These regions are just placeholders and should ideally be generated by a real damage detection model
        damage_areas = [
            (50, 50, 200, 200),  # Example: top-left to bottom-right rectangle
            (150, 150, 300, 300),  # Another area
            (250, 50, 400, 200),  # Another possible damaged area
        ]
        
        # Draw rectangles around the detected damage areas
        for (x1, y1, x2, y2) in damage_areas:
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 3)  # Blue rectangle for damage

    else:
        print("No damage detected.")

    # Show the output with marked areas
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    plt.imshow(img_bgr)
    plt.axis('off')
    plt.show()

def select_image_file():
    """Open a file dialog for the user to select an image."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select a Car Image",
        filetypes=(("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*"))
    )
    return file_path

# Main execution
if __name__ == "__main__":
    image_path = select_image_file()  # Open file dialog to select an image
    if image_path:  # Check if a file was selected
        detect_damage(image_path)
    else:
        print("No image file selected.")
