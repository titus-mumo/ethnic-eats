# import tensorflow as tf
# from tensorflow.python.keras import layers, models
# import albumentations as A
# from albumentations.pytorch import ToTensorV2
# from tensorflow.python.keras.utils import Sequence
# import os
# import numpy as np
# from PIL import Image

# # Define directories for training and validation data
# train_dir = 'path_to_train_data'
# validation_dir = 'path_to_validation_data'

# # Define the augmentation pipeline
# transform = A.Compose([
#     A.Resize(150, 150),
#     A.Rotate(limit=40),
#     A.ShiftScaleRotate(shift_limit=0.2, scale_limit=0.2, rotate_limit=0.2),
#     A.RandomBrightnessContrast(),
#     A.HorizontalFlip(),
#     A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
#     ToTensorV2()
# ])

# # Custom data generator
# class CustomDataGenerator(Sequence):
#     def __init__(self, image_paths, labels, batch_size, transform):
#         self.image_paths = image_paths
#         self.labels = labels
#         self.batch_size = batch_size
#         self.transform = transform

#     def __len__(self):
#         return len(self.image_paths) // self.batch_size

#     def __getitem__(self, idx):
#         batch_x = self.image_paths[idx * self.batch_size:(idx + 1) * self.batch_size]
#         batch_y = self.labels[idx * self.batch_size:(idx + 1) * self.batch_size]

#         images = [self.load_image(img_path) for img_path in batch_x]
#         images = np.stack(images, axis=0)

#         return images, np.array(batch_y)

#     def load_image(self, image_path):
#         image = Image.open(image_path).convert('RGB')
#         image = np.array(image)
#         augmented = self.transform(image=image)
#         return augmented['image']

# def load_data(directory):
#     categories = ['cat', 'dog']  # assuming binary classification
#     image_paths = []
#     labels = []

#     for category in categories:
#         class_num = categories.index(category)
#         path = os.path.join(directory, category)
#         for img in os.listdir(path):
#             image_paths.append(os.path.join(path, img))
#             labels.append(class_num)

#     return image_paths, labels

# # Load data
# train_image_paths, train_labels = load_data(train_dir)
# validation_image_paths, validation_labels = load_data(validation_dir)

# # Create data generators
# batch_size = 20
# train_generator = CustomDataGenerator(train_image_paths, train_labels, batch_size, transform)
# validation_generator = CustomDataGenerator(validation_image_paths, validation_labels, batch_size, transform)

# # Define the CNN model
# model = models.Sequential([
#     layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
#     layers.MaxPooling2D((2, 2)),
#     layers.Conv2D(64, (3, 3), activation='relu'),
#     layers.MaxPooling2D((2, 2)),
#     layers.Conv2D(128, (3, 3), activation='relu'),
#     layers.MaxPooling2D((2, 2)),
#     layers.Conv2D(128, (3, 3), activation='relu'),
#     layers.MaxPooling2D((2, 2)),
#     layers.Flatten(),
#     layers.Dense(512, activation='relu'),
#     layers.Dense(1, activation='sigmoid')
# ])

# model.compile(
#     loss='binary_crossentropy',
#     optimizer='adam',
#     metrics=['accuracy']
# )

# # Train the model
# history = model.fit(
#     train_generator,
#     steps_per_epoch=len(train_generator),
#     epochs=30,
#     validation_data=validation_generator,
#     validation_steps=len(validation_generator)
# )

# # Evaluate the model
# loss, accuracy = model.evaluate(validation_generator)
# print(f"Validation accuracy: {accuracy:.2f}")
