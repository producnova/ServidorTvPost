# importing whole module
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QSizeGrip, QVBoxLayout, QLabel
import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, QTime, Qt, QPoint

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Reloj"
        #Ancho del 20% de la pantalla
        self.ancho, self.alto, self.posicionx, self.posiciony = self.ventanasize()
        self.setWindowTitle(self.title)
        
        self.color_fondo = 'white'
        self.color_letras = 'black'
        if len(sys.argv) == 2 and sys.argv[1] != "":
            self.color_fondo = sys.argv[1]
        if len(sys.argv) == 3 and sys.argv[1] != "" and sys.argv[2] != "":
            self.color_fondo = sys.argv[1]
            self.color_letras = sys.argv[2]
        
        #print("Color del fondo en py: {}".format(self.color_fondo))
        
        #Cambia color del fondo
        self.setStyleSheet("background-color: {}".format(self.color_fondo))
        self.setGeometry(int(self.posicionx), int(self.posiciony), int(self.ancho), int(self.alto))
        #Tamaño de las letras = 44% del alto del reloj
        font_size = int(self.alto) * .44
        #font_size = 12
        
        #Contenedor que poseerá el label 
        layout = QVBoxLayout()
        font = QFont('Arial', font_size, QFont.Bold)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(font)
        self.label.setStyleSheet("color: {}".format(self.color_letras))
        layout.addWidget(self.label)
        self.setLayout(layout)
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        #Para ventana sin bordes
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        #Efecto drag
        self.oldPos = self.pos()
        self.show()

        #os.system('xdotool getactivewindow windowmove 830 691')
        
    
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
        
    def showTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.label.setText(label_time)
        
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
                        x =  val[:str(val).find("x")]
                    if key == "Screen 2":
                        ancho = int(val[:str(val).find("x")])
                        #y =  val[str(val).find("x")+1:]
                        #ancho = int(ancho)
                    if key == "Screen 3":
                        #ancho = val[:str(val).find("x")]
                        #ancho = int(int(ancho)*0.2)
                        alto = val[str(val).find("x")+1:]
                        #x = int(val[:str(val).find("x")]) - ancho
            if ancho == "" or alto == "":
                return "200", "70", 1200, 0
            else:
                return str(ancho), alto, x, y
                    
        else:
            return "200", "70", 0, 0

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())