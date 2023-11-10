import os
import pickle
import face_recognition

save_encoding = "encodings/encodings.pkl"

folder_path = 'data'  
def get_all_file_paths(root_folder):
    all_paths = []
    for root, dir, files in os.walk(root_folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            all_paths.append(file_path)
    return all_paths

all_paths = get_all_file_paths(folder_path)

def encode_known_faces(model = "cnn", encodings_location = save_encoding,all_paths=all_paths):
    names = []
    encodings = []
    pr = 0 
    for file_path in all_paths:
        pr += 100 / len(all_paths)
        if file_path == all_paths[-1]:
          print('completed: 100%')
        else:
          print('Processing:',int(pr),'%')
        name = file_path.split('/')[1]
        image = face_recognition.load_image_file(file_path)
        # bouding box
        face_locations = face_recognition.face_locations(image, model=model)
        # encoding bouding box
        face_encodings = face_recognition.face_encodings(image, face_locations)
        for encoding in face_encodings:
            # label, p
            names.append(name)
            encodings.append(encoding)
    name_encodings = {"names": names, "encodings": encodings}
    # save names and encodings
    with open(encodings_location,mode="wb") as f:
        pickle.dump(name_encodings, f)
encode_known_faces()