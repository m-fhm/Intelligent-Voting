import face_recognition
import cv2
import numpy as np
import pickle
import os
import glob


# Define variables for storing face encodings and names
faces_encodings = []
faces_names = []

# Get current working directory and path to 'faces' folder
cur_direc = os.getcwd()
path = os.path.join(cur_direc, 'faces')

# Get a list of all image files in 'faces' folder
list_of_files = [f for f in glob.glob(os.path.join(path, '*')) if os.path.isfile(f) and f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# Loop over image files and encode faces
for i, file_path in enumerate(list_of_files):
    # Load image file
    image = face_recognition.load_image_file(file_path)
    
    # Encode face in image
    face_encoding = face_recognition.face_encodings(image)[0]
    faces_encodings.append(face_encoding)

    # Extract name from file path and append to list
    file_name = os.path.basename(file_path)
    name = os.path.splitext(file_name)[0]
    faces_names.append(name)

# Save face encodings to file using pickle
with open('dataset_faces.dat', 'wb') as f:
    pickle.dump(faces_encodings, f)

# Save face names to file using pickle
with open('name_faces.dat', 'wb') as f:
    pickle.dump(faces_names, f)
