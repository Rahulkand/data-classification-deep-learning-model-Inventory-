from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing import image

class ImageClassifier():
            
    def image_classifier_model(self,dir_path, image_file):
        model = load_model("D:\start up project\Inventory\classification model-vgg16\modelV1_vgg_16.h5")
        img_paths = image_file
        for img_path in img_paths:
            img = image.load_img(path=dir_path+'//'+img_path,target_size=(224,224))
            X = image.img_to_array(img)
            X = np.expand_dims(X,axis=0)
            images = np.vstack([X])
            val = model.predict(images)
            a=np.argmax(val, axis=1)
            a = a.flatten()
            if(a[0]==0):
                return ("Fogg Absolute")
            elif(a[0]==1):
                return ("Fogg Dynamic")
            elif(a[0]==2):
                return ("Fogg Nepolean")
            elif(a[0]==3):
                return ("Fogg Royal")
            elif(a[0]==4):
                return ("Mama earth Sunscreen")
            elif(a[0]==5):
                return ("Nivea Milk BL")
            elif(a[0]==6):
                return ("Nivea Aloe BL")
            elif(a[0]==7):
                return ("Nivea Face Cream")
            else:
                return ("Unable to identify")