import tensorflow as tf
from tensorflow.keras import layers, models
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report

# Set dataset directories
dataset_dir = "/home/crj/venv/dataset"
image_size = (224, 224)  # Resize all images to this size

# Image Preprocessing: Load and preprocess the images
def load_images_from_directory(directory):
    images = []
    labels = []
    for label, class_name in enumerate(['real', 'fake']):
        class_folder = os.path.join(directory, class_name)
        if not os.path.exists(class_folder):
            print(f"Warning: Folder '{class_name}' does not exist.")
            continue
        for img_name in os.listdir(class_folder):
            if img_name.endswith((".jpg", ".png", ".jpeg")):
                img_path = os.path.join(class_folder, img_name)
                image = cv2.imread(img_path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
                image = cv2.resize(image, image_size)  # Resize image
                images.append(image)
                labels.append(label)
    return np.array(images), np.array(labels)

# Load data
real_fake_images, real_fake_labels = load_images_from_directory(dataset_dir)

# Check dataset
if real_fake_images.size == 0:
    raise ValueError("No images found in the dataset directory.")
print(f"Loaded {len(real_fake_labels)} samples: {np.bincount(real_fake_labels)}")

# Normalize image data
real_fake_images = real_fake_images / 255.0  # Normalize to [0, 1]

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(real_fake_images, real_fake_labels, test_size=0.2, random_state=42)

# Data augmentation for better generalization
datagen = ImageDataGenerator(
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest"
)

# Build the CNN model
model = models.Sequential([
    layers.InputLayer(shape=(224, 224, 3)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')  # Binary classification (Real vs Fake)
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
history = model.fit(
    datagen.flow(X_train, y_train, batch_size=32),
    epochs=20,
    validation_data=(X_test, y_test),
    callbacks=[early_stopping]
)

# Evaluate and save metrics
y_pred = (model.predict(X_test) > 0.5).astype("int32")
print(classification_report(y_test, y_pred, target_names=['Fake', 'Real']))

# Save the model
model_path = "/home/crj/venv/dataset/yolov8conn-tensormodel.keras"
model.save(model_path)
print(f"Model saved to {model_path}")
