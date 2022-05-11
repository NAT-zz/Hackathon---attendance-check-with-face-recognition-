import face_recognition
import pickle
import cv2
import os
from playsound import playsound
from gtts import gTTS
#from io import BytesIO
# def speak(text):
#     #mp3_fp = BytesIO()
#     file_name = f"{text}.mp3"
#     text = f"Bạn {text} đã điểm danh!"
#     speaker = gTTS(text=text, lang='vi')
    
#     #speaker.write_to_fp(mp3_fp)
#     speaker.save(file_name)
#     playsound(file_name)
#     os.remove(file_name)

def speak(audio):
    if (audio == 'Unknown'):
        return
    tts = gTTS(text = "Bạn "+audio+"đã điểm danh", lang='vi') #Khởi tạo nội dung và ngôn ngữ 
    filename = 'voice.mp3'  #Tên và địng dạng File
    tts.save(filename)  #Lưu
    playsound(filename)   #Chạy File âm thanh
    os.remove(filename) #Xóa File âm thanh

# def speak(text):
#     text = f"Bạn {text} đã điểm danh!"
#     speaker = gTTS(text=text, lang='vi', slow=False)
#     #speaker.write_to_fp(mp3_fp)
#     speaker.save('file_name.mp3')
#     os.system('start file_name.mp3')
#     os.remove('file_name.mp3')
#find path of xml file containing haarcascade file 
cascPathface = os.path.dirname(
 cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
# load the harcaascade in the cascade classifier
faceCascade = cv2.CascadeClassifier(cascPathface)
# load the known faces and embeddings saved in last file
data = pickle.loads(open('face_enc', "rb").read())
 
# loop over frames from the video file stream
names = set()

def recognition(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,
                                        scaleFactor=1.1,
                                        minNeighbors=5,
                                        minSize=(60, 60),
                                        flags=cv2.CASCADE_SCALE_IMAGE)

    # convert the input frame from BGR to RGB 
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # the facial embeddings for face in input
    encodings = face_recognition.face_encodings(rgb)
    
    # loop over the facial embeddings incase
    # we have multiple embeddings for multiple fcaes
    for encoding in encodings:
    #Compare encodings with encodings in data["encodings"]
    #Matches contain array with boolean values and True for the embeddings it matches closely
    #and False for rest
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        #set name =inknown if no encoding matches
        name = "Unknown"
        # check to see if we have found a match
        if True in matches:
            #Find positions at which we get True and store them
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            # loop over the matched indexes and maintain a count for
            # each recognized face face
            
            for i in matchedIdxs:
                #Check the names at respective indexes we stored in matchedIdxs
                name = data["names"][i]
                #increase count for the name we got
                counts[name] = counts.get(name, 0) + 1
            
            #set name which has highest count
            name = max(counts, key=counts.get)
            

        # update the list of namesq
        if name not in names:
            names.add(name)
            speak(name)
        print(names)
        # loop over the recognized faces
        for ((x, y, w, h), name) in zip(faces, names):
            # rescale the face coordinates
            # draw the predicted face name on the image
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.75, (0, 255, 0), 2)

    return frame,names

if __name__=='__main__':
    recognition()