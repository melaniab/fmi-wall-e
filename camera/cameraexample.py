import picamera
import time

def capture():
    camera = picamera.PiCamera()
    camera.capture("test.jpeg") # camere capture
    

def record():
    camera = picamera.PiCamera()
    camera.start_recording("examplevid.h264")
    time.sleep(10)
    camera.stop_recording()
    
def preview():
    camera = picamera.PiCamera()
    camera.start_preview()
    time.sleep(15)
    camera.stop_preview()
   


def stream():
    with picamera.PiCamera() as camera:
        with picamera.PiCameraCircularIO(camera,seconds = 10, splitter_port=2) as stream:
            camera.start_recording(stream, format='h264', splitter_port=2)
            camera.wait_recording(10, splitter_port=2)
            camera.stop_recording(splitter_port=2)
        
if __name__ == "__main__":
    capture()
    