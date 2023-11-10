import pickle
import face_recognition
import cv2
from collections import Counter
import csv
import os 
from datetime import datetime



save_encoding = r"encodings/encodings.pkl"
# so sánh encoding với rate = .5
def recognize_face(unknown_encoding, loaded_encodings):
    boolean_matches = face_recognition.api.compare_faces(loaded_encodings["encodings"], unknown_encoding,tolerance=0.5)
    votes = Counter(name for match, name in zip(boolean_matches, loaded_encodings["names"]) if match)
    if votes :
        return votes.most_common(1)[0][0]
    else:
        return 'Unknown'

check_csv = False
def display_face(img, List_Bounding, List_Name):
    global check_csv
    if List_Name == None:
        check_csv = False
        return img
    else:
        for bounding_box , name in zip(List_Bounding,List_Name):
            top, right, bottom, left = bounding_box
            imgID  = cv2.rectangle(img,(left,top),(right,bottom),(0,255,0))
            imgID = cv2.putText(imgID, text=name,org=(left,top+20),color=(0,255,0),fontFace=1,fontScale=1,thickness=1)
        check_csv = True
        return imgID
    
def recognize_faces(image_location, model = "hog", encodings_location = save_encoding) :
    global List_Name
    with open(encodings_location,mode="rb") as f:
        loaded_encodings = pickle.load(f)
    input_face_locations = face_recognition.face_locations(image_location, model = model)
    if input_face_locations == []:
        undetected = display_face(image_location,None,None)
        return False,undetected
    input_face_encodings = face_recognition.face_encodings(image_location, input_face_locations)
    List_Name = []
    List_Bounding = []
    for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings): 
        name = recognize_face(unknown_encoding, loaded_encodings)
        List_Name.append(name)
        List_Bounding.append(bounding_box)
    detected = display_face(image_location, List_Bounding, List_Name) 
    write_csv()
    return True,detected

def write_csv():
    global List_Name,status
    data = []
    cur_date = datetime.now().date()
    cur_time = datetime.now().strftime("%H:%M:%S")
    for i in List_Name:
        data.append([i,status,cur_date,cur_time])
    file_path = r'csv/attention.csv'
    file_exists = os.path.exists(file_path)
    with open(file_path, mode='a', newline='') as f:
        writer = csv.writer(f)
        if file_exists == False:
            writer.writerow(['Full Name','Status','Date','Time'])
        writer.writerows(data)
        f.close()

def read_csv():
    file_path = r'csv/attention.csv'
    with open(file_path, mode='r', newline='') as f:
        read = csv.reader(f)
        data = [data for data in read]
        return data[-1]
status = None
def status_in():
    global status
    status = 'Check In'   
def status_out():
    global status
    status = 'Check Out'