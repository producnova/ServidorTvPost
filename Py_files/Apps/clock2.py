# importing whole module 
from tkinter import font
import tkinter as tk
from tkinter.ttk import *
import sys
import os
import subprocess
from time import strftime 

class RelojDigital:
    def __init__(self, ventana):
        self.color_fondo = 'white'
        self.color_letras = 'black'
        if len(sys.argv) == 2:
            self.color_fondo = sys.argv[1]
        if len(sys.argv) == 3:
            self.color_fondo = sys.argv[1]
            self.color_letras = sys.argv[2]
        self.ventana = ventana
        self.ventana.title("Reloj")
        self.ventana.configure(bg=self.color_fondo)
        self.ventana.bind('<Configure>', self.resize)
        self.label_font = font.Font(self.ventana, family='Arial', size=12, weight='bold')
        self.label = Label(self.ventana,
                           background = self.color_fondo,
                           foreground = self.color_letras)
        self.label.pack(fill = "both", expand = "yes", anchor = "center")
        self.time()
        #Ancho del 20% de la pantalla
        self.ancho, self.alto, self.x, self.y = self.ventanasize()
        self.ventana.geometry("{}x{}+{}+{}".format(self.ancho, self.alto, self.x, self.y))

        
    # display time on the label 
    def time(self): 
        string = strftime('%H:%M:%S') 
        self.label.config(text = string, font = self.label_font) 
        self.label.after(1000, self.time) 
        
    def resize(self, event):
        height = self.label.winfo_height()
        width = self.label.winfo_width()
        self.label.configure(anchor="center")
        height = (height // 2)
#         if height < 10 or width < 200:
#             height = height
#         elif width < 400 and height > 20:
#             height = 70
#         elif width < 600 and height > 30:
#             height = 100
#         else:
#             height = 60
        self.label_font['size'] = height
        #frameless
        #self.ventana.overrideredirect(True)
        
    def ventanasize(self):
        ruta_datos = "/home/pi/TvPost/Resolutions/new_resolutions.txt"
        ancho = ""
        alto = ""
        x=""
        y=""
        #Se calculan los tamños y proporciones
        if os.path.exists(ruta_datos):
            with open(ruta_datos) as f:
                for line in f:
                    (key, val) = line.strip().split(":")
                    if key == "Screen 1":
                        y =  val[str(val).find("x")+1:]
                    if key == "Screen 3":
                        ancho = val[:str(val).find("x")]
                        ancho = int(int(ancho)*0.2)
                        alto = val[str(val).find("x")+1:]
                        x = int(val[:str(val).find("x")]) - ancho
            if ancho == "" or alto == "":
                return "200", "70", 0, 0
            else:
                return str(ancho), alto, x, y
                    
        else:
            return "200", "70", 0, 0
                
        
root = tk.Tk()
#Sin marco
#root.attributes('-type', 'dock')
reloj_digital_interfaz = RelojDigital(root)
root.mainloop()