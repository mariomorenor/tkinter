from tkinter import *
from tkinter.ttk import Combobox, LabelFrame
import cv2
from PIL import Image
from PIL import ImageTk


class MainWindow():

    clientes = [
        {
            "display_name": "Scanner Express",
            "id": 13,
            "camaras": [
                {
                    "ip": "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
                }
            ],
            "autorizadores": [
                {
                    "id": 1,
                    "display_name": "Mario Moreno"
                },
                {
                    "id": 2,
                    "display_name": "Ceider Zambrano"
                },
            ]
        },
        {
            "display_name": "Proají",
            "id": 13,
            "camaras": [
                {
                    "ip": "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
                }
            ],
            "autorizadores": [
                {
                    "id": 3,
                    "display_name": "Stalin Pinos"
                },
                {
                    "id": 4,
                    "display_name": "Hernán Naranjo Avilés"
                },
            ]
        }
    ]
    streaming = False

    def __init__(self, window):
        self.window = window
        self.window.title("Bitácora")

        # Frame Container
        frame = LabelFrame(self.window, text="Datos del Registro")
        frame.grid(row=0, column=1, sticky=N, pady=20)

        # Frame Video Container
        frameVideo = LabelFrame(self.window, text="VideoPortero")
        frameVideo.grid(row=0, column=0, padx=30, pady=20)

        # Imagen container
        self.canvas = Canvas(frameVideo, width=400, height=200)
        self.canvas.grid(row=0, column=0)

        # Intervalo de Actualización
        self.interval = 30  # Milisegundos

        # VideoPortero CONTROL
        Label(frame, text="Videoportero:").grid(
            row=0, column=0, pady=10, padx=10)
        self.cmbClientes = Combobox(
            frame, state="readonly", values=self.get_clientes())
        self.cmbClientes.grid(row=0, column=1, padx=10)
        self.cmbClientes.bind("<<ComboboxSelected>>",
                              func=self.cliente_selected)

        # Autorizador Control
        Label(frame, text="Autorizador:").grid(row=1, column=0)
        self.cmbAutorizadores = Combobox(
            frame, state="readonly", values=[])
        self.cmbAutorizadores.grid(row=1, column=1)

        # Boton Iniciar Stream Control
        self.btnStream = Button(
            frame, text="Iniciar Video", command=self.init_stream).grid(row=2, column=0)
        self.btnStopStream = Button(
            frame, text="Detener Video", command=self.stop_stream).grid(row=2, column=1)

    # Se ejecuta cada que se selecciona un videoportero
    def cliente_selected(self, event):
        for c in self.clientes:
            if c["display_name"] == self.cmbClientes.get():
                self.cmbAutorizadores["values"] = list(
                    map(lambda autorizador: autorizador["display_name"], c["autorizadores"]))
                self.cmbAutorizadores.current(0)

    # Funcion para obtener los clientes
    def get_clientes(self):
        clientes = map(lambda cliente: cliente["display_name"], self.clientes)
        return list(clientes)

    # Actualiza la imagen dado un intervalo
    def update_image(self):
        # Get the latest frame and convert image format
        try:
            self.OGimage = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB)  # to RGB
            self.OGimage = Image.fromarray(self.OGimage)  # to PIL format
            self.image = self.OGimage.resize((400, 200), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(self.image)  # to ImageTk format
            # Update image
            self.canvas.create_image(0, 0, anchor=NW, image=self.image)
            # Repeat every 'interval' ms
            self.window.after(self.interval, self.update_image)

        except Exception as e:
            print(e)

    # Inicia la transmisión de video

    def init_stream(self):
        print(self.cmbClientes.get())
        if not self.streaming:
            self.streaming = True
            for c in self.clientes:
                if c['display_name'] == self.cmbClientes.get():
                    self.cap = cv2.VideoCapture(c["camaras"][0]["ip"])
                    self.update_image()
            if self.cmbClientes.get() == "":
                self.streaming = False
                    

    def stop_stream(self):
        if self.streaming:
            self.cap.release()
            self.streaming = False


if __name__ == "__main__":
    window = Tk()
    application = MainWindow(window)
    window.geometry("900x600")
    window.mainloop()

# import cv2
# from PIL import Image
# from PIL import ImageTk


# class MainWindow():
#     def __init__(self, window, cap):
#         self.window = window
#         self.cap = cap
#         self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
#         self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
#         self.interval = 60 # Interval in ms to get the latest frame
#         # Create canvas for image
#         self.canvas = tk.Canvas(self.window, width=600, height=400)
#         self.canvas.grid(row=0, column=0)
#         # Update image on canvas
#         root.after(self.interval, self.update_image)


#     def update_image(self):
#         # Get the latest frame and convert image format
#         self.OGimage = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) # to RGB
#         self.OGimage = Image.fromarray(self.OGimage) # to PIL format
#         self.image = self.OGimage.resize((600, 400), Image.ANTIALIAS)
#         self.image = ImageTk.PhotoImage(self.image) # to ImageTk format
#         # Update image
#         self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
#         # Repeat every 'interval' ms
#         self.window.after(self.interval, self.update_image)


# if __name__ == "__main__":

#     root = tk.Tk()
#     MainWindow(root, cv2.VideoCapture("rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4"))
#     root.mainloop()
