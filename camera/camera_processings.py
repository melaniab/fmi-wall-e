import time
import datetime
import picamera


class ImageSaver():
    
    def __init__(self):
        self.queue = []
        self.camera = picamera.PiCamera()
        self.rate = 30
        self.fdir = "./images/{}"
        self.fname = "./images/{}.jpeg"
    
    def c(self):
        pass
    
    def start(self):
        for i in range(self.rate):
            t = int(time.time())
            fname = self.fname.format(t)
            self.capture(fname)
   
    def capture(self,image_name):
        self.camera.capture(image_name):
            
        pass
    
    def _create_file(self,t):
       return self.fdir.format()
        
        
        
if __name__ == "__main__":
    image = ImageSaver()
#    image.start()
    #capture()
   