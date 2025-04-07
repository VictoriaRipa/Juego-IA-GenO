from threading import Thread
import cv2
import platform

class Webcam:
    def __init__(self, camera_index=0):  # Permite elegir la cámara
        self.stopped = False
        self.stream = None
        self.lastFrame = None
        self.os_name = platform.system()
        self.camera_index = camera_index  # Guarda el índice de la cámara

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        if self.stream is None:
            if self.os_name == "Windows":
                self.stream = cv2.VideoCapture(self.camera_index, cv2.CAP_MSMF)
                if not self.stream.isOpened():
                    self.stream = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
                if not self.stream.isOpened():
                    self.stream = cv2.VideoCapture(self.camera_index)
            elif self.os_name == "Darwin":
                self.stream = cv2.VideoCapture(self.camera_index, cv2.CAP_AVFOUNDATION)
            else:
                self.stream = cv2.VideoCapture(self.camera_index, cv2.CAP_V4L)

        while True:
            if self.stopped:
                return
            (result, image) = self.stream.read()
            if not result:
                self.stop()
                return
            self.lastFrame = image
                
    def read(self):
        return self.lastFrame

    def stop(self):
        self.stopped = True
        if self.stream is not None:
            self.stream.release()

    def width(self):
        if self.stream is not None:
            return self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        return 0

    def height(self):
        if self.stream is not None:
            return self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return 0
    
    def ready(self):
        return self.lastFrame is not None



def detectar_camaras():
    print("Buscando cámaras disponibles...")
    for i in range(5):  # Prueba hasta 5 índices de cámara
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Cámara detectada en índice {i}")
            cap.release()


if __name__ == "__main__":
    detectar_camaras()  # Muestra qué cámaras están disponibles

    cam_index = int(input("Ingresa el índice de la cámara a usar (0 = interna, 1 = externa, etc.): "))

    cam = Webcam(camera_index=cam_index)
    cam.start()

    while True:
        frame = cam.read()
        if frame is not None:
            cv2.imshow("Cámara", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break

    cam.stop()
    cv2.destroyAllWindows()
