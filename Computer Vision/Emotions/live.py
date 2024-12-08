import cv2
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import numpy as np
import time

def load_image_from_frame(frame):
    img = cv2.resize(frame, (224, 224))
    img = img_to_array(img)
    img = img.reshape(1, 224, 224, 3)
    img = img.astype('float32')
    img = img - [123.68, 116.779, 103.939]
    return img

def run_live_example():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    model = load_model('C:/Users/Adrian Danao/Codes/Python/Computer Vision/Emotions/final_model_emotions.keras')
    categories = ["Angry", "Happy", "Neutral", "Sad", "Surprised"]

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        img = load_image_from_frame(frame)
        result = model.predict(img)
        
        predicted_class = np.argmax(result[0])
        predicted_label = categories[predicted_class]
        predicted_percentage = result[0][predicted_class] * 100
        
        for i, category in enumerate(categories):
            print(f"{category}: {result[0][i] * 100:.2f}%")
        
        cv2.putText(frame, f"Predicted: {predicted_label} ({predicted_percentage:.2f}%)", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        cv2.imshow('Emotion Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        time.sleep(1)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_live_example()