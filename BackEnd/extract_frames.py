# Importing all necessary libraries 
import cv2 
import os 
  
def extract_frames(path):
    cam = cv2.VideoCapture(path) 
    fps = cam.get(cv2.CAP_PROP_FPS)
    fps = round(fps)*10
    try: 
        if not os.path.exists('extracted_frames/'): 
            os.makedirs('extracted_frames') 
    
    except OSError: 
        print ('Error: Creating directory of data') 
    
    currentframe = 0
    
    while(True): 
        ret,frame = cam.read() 
        if ret: 
            if currentframe%fps == 0:   
                name = './extracted_frames/frame' + str(currentframe) + '.jpg'
                print ('Creating...' + name) 

                cv2.imwrite(name, frame) 
            currentframe += 1
        else: 
            break
        
    cam.release() 
    cv2.destroyAllWindows()

if __name__ == '__main__':
    #extract_frames('C:/Users/Melin/Desktop/sweettooth.mp4')
    for file in os.listdir("C:/Users/Melin/Desktop/bitirme-2/deneme"):
        if file.endswith(".m4v"):
            path=os.path.join("C:/Users/Melin/Desktop/bitirme-2/deneme", file)
            extract_frames(path)
            