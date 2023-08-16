import face_recognition as fr
import os
import pickle

Encodings=[]
Names=[]

#Learning
image_dir='/home/es017590/Desktop/pyPro/faceRecognizer/demoImages/known'
for root, dirs, imgs in os.walk(image_dir):
    for img in imgs:
        path=os.path.join(root,img)
        name=os.path.splitext(img)[0]
        face=fr.load_image_file(path)
        Encodings.append(fr.face_encodings((face))[0])
        Names.append(name)
        print("Learned what " + name + " looks like!")
print('Training DONE!')

with open('trainingData.pkl', 'wb') as f:
    pickle.dump(Names, f)
    pickle.dump(Encodings, f)
print('Data saved!')
