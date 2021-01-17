import socket
import os
import io
import time
import threading
import math
from PIL import Image

class ClientThread(threading.Thread):
    clientAddress = '';
    conn = '';
    def __init__(self, address, clientSocket):
        try:
            threading.Thread.__init__(self, name="hiloNuevo", target=ClientThread.run)
            self.conn = clientSocket
            self.clientAddress = address
            print ("Nueva conexión con: ", self.clientAddress)
        except e as msg:
            print("Error al crear clase hilo: "+str(msg))
    
    #Funciones que reciben y envían datos
    def ResponderPing(self):
        return "Conectado"
    
    def CambiarResolucion(self, Ancho, Alto):
        os.system('python3 ~/TvPost/Py_files/Resolution/CambiarResolucion.py {} {}'.format(Ancho,Alto))
        return ('Resolución cambiada a: ' + Ancho + 'x' + Alto)

    def ModificarLayout(self,ArregloDatos):
        
        #Leer el archivo de información si existe y obtener el layout.
        #Si al compararlo con el layout que viene desde el móvil son distinos, se cambia
        #la resolucion, sino, se mantiene
        #Acá tengo que ver si el reloj que viene es igual al que está
        archivoDatosReprroduccion = "/home/pi/TvPost/Resolutions/datos_reproduccion.txt"
        relojEnArchivo = ""
        archivo10 = ""
        if (os.path.exists(archivoDatosReprroduccion)):
            with open(archivoDatosReprroduccion) as f:
                for line in f:
                    if "relojEnPantalla," in line:
                        relojEnArchivo = line[line.find('#')-2:line.find('#')]
                    if "archivo3," in line:
                        archivo10 = line[line.find(',')+1:].strip()
                        if archivo10 == "0":
                            archivo10 = ""

        #Datos que se escriben en el archivo para obtenerlos en el equipo móvil
        porcionACambiar = ArregloDatos[2]
        tipoArchivo1 = ArregloDatos[3]
        tipoArchivo2 = ArregloDatos[4]
        tipoArchivo3 = ArregloDatos[5]
        archivo1 = ArregloDatos[6]
        archivo2 = ArregloDatos[7]
        archivo3 = ArregloDatos[8]
        relojEnPantalla = ArregloDatos[9]
        relojQueViene = relojEnPantalla[relojEnPantalla.find('#')-2:relojEnPantalla.find('#')]
        layout = ""
        if (ArregloDatos[1] == '100'):
            layout = "1"
        if (ArregloDatos[1] == '5050'):
            layout = "2"
        if (ArregloDatos[1] == '802010'):
            layout = "3"
                
            
        #if (ArregloDatos[1] == '802010' and relojEnPantalla[:relojEnPantalla.index('#')] == 'off' ):
        #    layout = "3"
        #if (ArregloDatos[1] == '802010' and relojEnPantalla[:relojEnPantalla.index('#')] == 'on' ):
        #    layout = "3reloj"
        
        
        if (porcionACambiar == "null"):
            #Preguntar que layout viene para mantener cierta porcion
            #layout 100 mantiene archivo izquierda
            #layout 2 mantiene izquierda y derecha
            #layout 3 mantiene todo
            if layout == "1":
                porcionACambiar = "mantener1"
            if layout == "2":
                porcionACambiar = "mantener2"
            if layout == "3":
                #si no son iguales, cambiar la imagen por la porción 3 correspondiente
                # y ya no sería mantener 3, sería porción a cambiar 3-3
                #y el archivo 3 tiene qeu ser el correspondiente a la imagen
                #pero de la carpeta correspondiente
                
                #Si son iguales, se mantiene
                if relojEnArchivo == relojQueViene:
                    porcionACambiar = "mantener3"
                else:
                #Si el reloj está on, se va abuscar la imagen a la carpeta 10
                    #Si no hay archivo en el 10, se mantiene todo
                    if archivo10 == "":
                        porcionACambiar = "mantener3"
                    else:
                        if relojQueViene == "on":
                            porcionACambiar = "3-3"
                            archivo10 = archivo10[archivo10.rfind("/") + 1:]
                            archivo10 = archivo10.replace(' ', '<!-!>')
                            archivo3 = "/var/www/html/ImagenesPostTv10/{}".format(archivo10)

                        else:
                            porcionACambiar = "3-3"
                            archivo10 = archivo10[archivo10.rfind("/") + 1:]
                            archivo10 = archivo10.replace(' ', '<!-!>')
                            archivo3 = "/var/www/html/ImagenesPostTv/{}".format(archivo10)
                        self.CambioLayout(layout, relojQueViene, relojEnArchivo, relojEnPantalla)
                        
        else:
            #Verifico si se necesita cambiar layout o no
            #solo cambia layout si no se desea mantener algo
            #si se desea mantener, se cambio luego de manipular
            #las apps en el bash opening_apps
            #Si es porción 3 también hago una apertura previa del archivo anterior existente
            self.CambioLayout(layout, relojQueViene, relojEnArchivo, relojEnPantalla)

        try:

            listadoArchivosUtilizar = []

            if (porcionACambiar == "1-1"):
                listadoArchivosUtilizar.clear()
                listadoArchivosUtilizar.append(archivo1)
                
            if (porcionACambiar == "2-1"):
                listadoArchivosUtilizar.clear()
                listadoArchivosUtilizar.append(archivo1)
                
            if (porcionACambiar == "2-2"):
                listadoArchivosUtilizar.clear()
                listadoArchivosUtilizar.append(archivo2)
                
            if (porcionACambiar == "2-3"):
                listadoArchivosUtilizar.clear()
                listadoArchivosUtilizar.append(archivo1)
                listadoArchivosUtilizar.append(archivo2)
                
            if (porcionACambiar == "3-1"):
                listadoArchivosUtilizar.clear()
                listadoArchivosUtilizar.append(archivo1)
            
            if (porcionACambiar == "3-2"):
                listadoArchivosUtilizar.clear()
                listadoArchivosUtilizar.append(archivo2)
                
            if (porcionACambiar == "3-3"):
                #Cambia archivo específico para reloj
                #cuando viene vacío
                listadoArchivosUtilizar.clear()
                if relojQueViene == "on":
                    if 'ImagenesPostTv10' not in archivo3:
                        archivo3 = archivo3.replace('ImagenesPostTv', 'ImagenesPostTv10')
                else:
                    archivo3 = archivo3.replace('ImagenesPostTv10', 'ImagenesPostTv')
                listadoArchivosUtilizar.append(archivo3)
            
            if (porcionACambiar == "3-4"):
                listadoArchivosUtilizar.clear()
                listadoArchivosUtilizar.append(archivo1)
                listadoArchivosUtilizar.append(archivo2)
                if relojQueViene == "on":
                    if 'ImagenesPostTv10' not in archivo3:
                        archivo3 = archivo3.replace('ImagenesPostTv', 'ImagenesPostTv10')
                else:
                    archivo3 = archivo3.replace('ImagenesPostTv10', 'ImagenesPostTv')
                listadoArchivosUtilizar.append(archivo3)
                
            if (porcionACambiar == "3-5"):
                listadoArchivosUtilizar.clear()
                listadoArchivosUtilizar.append(archivo1)
                listadoArchivosUtilizar.append(archivo2)
                
            if (porcionACambiar == "3-6"):
                listadoArchivosUtilizar.clear()
                listadoArchivosUtilizar.append(archivo2)
                if relojQueViene == "on":
                    if 'ImagenesPostTv10' not in archivo3:
                        archivo3 = archivo3.replace('ImagenesPostTv', 'ImagenesPostTv10')
                else:
                    archivo3 = archivo3.replace('ImagenesPostTv10', 'ImagenesPostTv')
                listadoArchivosUtilizar.append(archivo3)
                
            if (porcionACambiar == "3-7"):
                listadoArchivosUtilizar.clear()
                listadoArchivosUtilizar.append(archivo1)
                if relojQueViene == "on":
                    if 'ImagenesPostTv10' not in archivo3:
                        archivo3 = archivo3.replace('ImagenesPostTv', 'ImagenesPostTv10')
                else:
                    archivo3 = archivo3.replace('ImagenesPostTv10', 'ImagenesPostTv')
                listadoArchivosUtilizar.append(archivo3)
                

            archivoBash = 'bash ~/TvPost/Bash_files/Apps_interaction/app_opening_functions.sh'
            archivoBash += ' ' + porcionACambiar
            for archivo in listadoArchivosUtilizar:
                print("Archivo: " + archivo)
                archivoBash += " '" + archivo + "'"
            archivoBash += ' ' + relojEnPantalla
            print("Instruccion al cambiar: " + archivoBash)
            os.system(archivoBash)
            print('OK!')
        except:
            return 'Error al crear archivo bash'
        
         #Se escriben los datos del archivo de repŕoduccion atual
        self.CrearArchivoDatosReproduccion(ArregloDatos)
        
        return 'Ok, vea sus pantallas'
    
    def CrearArchivoDatosReproduccion(self,ArregloDatos):
    
        #Datos que se escriben en el archivo para obtenerlos en el equipo móvil
        layout = ""
        if (ArregloDatos[1] == '100'):
            layout = "1"
        if (ArregloDatos[1] == '5050'):
            layout = "2"
        if (ArregloDatos[1] == '802010'):
            layout = "3"
        tipoArchivo1 = ArregloDatos[3]
        tipoArchivo2 = ArregloDatos[4]
        tipoArchivo3 = ArregloDatos[5]
        archivo1 = ArregloDatos[6]
        archivo2 = ArregloDatos[7]
        archivo3 = ArregloDatos[8]
        relojEnPantalla = ArregloDatos[9]
        
        archivo1 = archivo1.replace('<!-!>', ' ')
        archivo2 = archivo2.replace('<!-!>', ' ')
        archivo3 = archivo3.replace('ImagenesPostTv10', 'ImagenesPostTv')
        archivo3 = archivo3.replace('<!-!>', ' ')
        
        #Crea archivo de datos de reproduccion actual
        try:
            #Verifrica contenido de archivo actual
            archivoDatosReprroduccion = "/home/pi/TvPost/Resolutions/datos_reproduccion.txt"
            d = {}
            if (os.path.exists(archivoDatosReprroduccion)):
                with open(archivoDatosReprroduccion) as f:
                    for line in f:
                        (key, val) = line.strip().split(",")
                        d[key] = val
            
            if archivo1 != '0' and '/var/www/html' in archivo1:
                archivo1 = archivo1[13:]
            if archivo2 != '0' and '/var/www/html' in archivo2:
                archivo2 = archivo2[13:]
            if archivo3 != '0' and '/var/www/html' in archivo3:
                archivo3 = archivo3[13:]
                
            archivoDatos = "/home/pi/TvPost/Resolutions/datos_reproduccion.txt"
            #Escribe los datos
            with open(archivoDatos, "w") as f:
                f.write("layout," + layout + "\n")
                f.write("tipoArchivo1," + tipoArchivo1 + "\n")
                f.write("tipoArchivo2," + tipoArchivo2 + "\n")
                f.write("tipoArchivo3," + tipoArchivo3 + "\n")
                f.write("archivo1," + archivo1 + "\n")
                f.write("archivo2," + archivo2 + "\n")
                f.write("archivo3," + archivo3 + "\n")
                f.write("relojEnPantalla," + relojEnPantalla)
                
        except:
            print('Error al crear archivo datos reproducción')
        
    def CambioLayout(self,layout ,relojQueViene, relojEnArchivo, relojCompleto):
    #Cambio de porción solo si es distinto
        direccion_archivo_datos = "/home/pi/TvPost/Resolutions/datos_reproduccion.txt"
        layoutActualEnArchivo = ""
        archivo3Existente = ""
        if os.path.exists(direccion_archivo_datos):
            with open(direccion_archivo_datos, "rt") as f:
                for line in f:
                    if "layout," in line:
                        #Asigna valor
                        layoutActualEnArchivo = str(line[line.index(',') + 1:]).strip()
                    if "archivo3," in line:
                        #Asigna valor al archivo
                        archivo3Existente = "/var/www/html" + str(line[line.index(',') + 1:]).strip()

            try:
                if layout != layoutActualEnArchivo:
                    print("Llegaron distintos")
                    #print("layout" + layout)
                    #print("layout en archivo" + layoutActualEnArchivo)
                    if layout == "1":
                        if os.system('python3 ~/TvPost/Py_files/Screen_format/Formato_100.py'):
                            os.wait()
                    if layout == "2":
                        if os.system('python3 ~/TvPost/Py_files/Screen_format/Formato_50_50.py'):
                            os.wait()
                    if layout == "3":
                        if relojQueViene == "on":
                            if os.system('python3 ~/TvPost/Py_files/Screen_format/Formato_80_20_10_reloj.py'):
                                os.wait()
                        else:
                            if os.system('python3 ~/TvPost/Py_files/Screen_format/Formato_80_20_10.py'):
                                os.wait()
                else:
                    print("Llegaron iguales")
                    if layout == "3":
                        if relojQueViene != relojEnArchivo:
                            print("Relojes distintos")
                            #Si son distintos, tengo que:
                            #1.- Obtener el nombre del archivo 3 y su id para xrander y minimizarlo
                            #2.- Cerrar el archivo 3
                            #3.- Cambiar layout
                            #4.- Abrir archivo 3 en la porción inferior
                            #Obtengo ID
                            id3EnArchivo = ""
                            archivoId = "/home/pi/TvPost/Resolutions/window_id.txt"
                            if os.path.exists(archivoId):
                                with open(archivoId, "rt") as f:
                                    for line in f:
                                        if "3:" in line:
                                            #Asigna valor
                                            id3EnArchivo = str(line[line.index(':') + 1:line.index('-')]).strip()
                            
                            #Minimizo archivo 3 por id
                            os.system('xdotool windowminimize {}'.format(id3EnArchivo))
                            
                            if relojQueViene == "on":
                                print("reloj encendido")
                                #Se modifica la ruta del archivo para tomar imagen de carpeta 10
                                archivo3Existente = archivo3Existente.replace('ImagenesPostTv', 'ImagenesPostTv10')
                                if os.system('python3 ~/TvPost/Py_files/Screen_format/Formato_80_20_10_reloj.py'):
                                    os.wait()
                                #os.system("bash ~/TvPost/Bash_files/Apps_interaction/app_opening_functions.sh '{}' '{}' '{}'".format("3-3", archivo3Existente, relojCompleto))
                            else:
                                print("reloj apagado")
                                if os.system('python3 ~/TvPost/Py_files/Screen_format/Formato_80_20_10.py'):
                                    os.wait()
                                    
                            os.system("bash ~/TvPost/Bash_files/Apps_interaction/app_opening_functions.sh '{}' '{}' '{}'".format("3-3", archivo3Existente, relojCompleto))

            except:
                return 'Error al cambiar layout'
                        
                
        else:
            #Si no existe el archivo, se genera una nueva partición de pantalla utilizando
            #el valor que viene desde l dispositvo
            try:
                if layout == "1":
                    if os.system('python3 ~/TvPost/Py_files/Screen_format/Formato_100.py'):
                        os.wait()
                if layout == "2":
                    if os.system('python3 ~/TvPost/Py_files/Screen_format/Formato_50_50.py'):
                        os.wait()
                if layout == "3":
                    if relojQueViene == "on":
                        if os.system('python3 ~/TvPost/Py_files/Screen_format/Formato_80_20_10_reloj.py'):
                            os.wait()
                    else:
                        if os.system('python3 ~/TvPost/Py_files/Screen_format/Formato_80_20_10.py'):
                            os.wait()
            except:
                return 'Error al cambiar layout'

    def CapturarPantalla(self,conn):
        #Tomo captura
        os.system('bash ~/TvPost/Bash_files/Apps_interaction/screenshot.sh')
        
        archivo="/home/pi/TvPost/Screenshots/pantalla.png"
        
        with open(archivo, "rb") as f:
            content = f.read()
            
        size = len(content)
        print("File bytes: ", size)

        conn.sendall(content)
                 
        print("Enviando...")
        
        return "Datos enviados"   
    
    def NombresImagenes(self, conn):
        directorio = '/var/www/html/ImagenesPostTv'
        #directorio = '/home/pi/TvPost/ImagenesPostTv/'
        dirs = os.listdir(directorio)
        listadoItemsEnDirectorio = os.listdir(directorio)
        listadoItemsEnDirectorio.sort()
        listunido = ','.join(map(str, listadoItemsEnDirectorio))
        #Envío nombre de archivo
        conn.sendall(listunido.encode())
        
        print("Enviando Nombres")
        
        return "ENviado nombres"
    
    def VerificarNombreImagen(self, conn, nombreImagen):
        #Obtiene el listado de archivos
        directorio = '/var/www/html/ImagenesPostTv'
        dirs = os.listdir(directorio)
        resultado = '';
        if nombreImagen in dirs:
            resultado = 'Existe'
        else:
            resultado = 'No existe'
            
        print(resultado)
        conn.sendall(resultado.encode())
        return "Resultado Enviado"
    
    def NombresVideos(self, conn):
        #directorio = '/var/www/html/VideosPostTv'
        #Obtiene el listado de archivos
        directorioVideos = '/var/www/html/VideosPostTv'

        #Se crea el listado que guarda los nombres de videos
        dirsVideos = []
        for archivo in os.scandir(directorioVideos):
            if archivo.is_file():
                dirsVideos.append(archivo.name)

        dirsVideos.sort()
        listunido = ','.join(map(str, dirsVideos))

        #Envío nombre de archivo
        conn.sendall(listunido.encode())
        
        print("Enviando Nombres")
        
        return "Eviado nombres"
    
    def VerificarNombreVideo(self, conn, nombreVideo):
        #Obtiene el listado de archivos
        directorio = '/var/www/html/VideosPostTv/'
        dirs = os.listdir(directorio)
        resultado = '';
        if nombreVideo in dirs:
            resultado = 'Existe'
        else:
            resultado = 'No existe'
            
        print(resultado)
        conn.sendall(resultado.encode())
        return "Resultado Enviado"
    
    def DatosReproduccionActual(self,conn):
        #va a buscar archivo con datos de reproduccion actual.
        archivoDatosReprroduccion = "/home/pi/TvPost/Resolutions/datos_reproduccion.txt"
        d = {}
        if (os.path.exists(archivoDatosReprroduccion)):
            with open(archivoDatosReprroduccion) as f:
                for line in f:
                    (key, val) = line.strip().split(",")
                    d[key] = val
        #Acá debe retornar el diccionario
        dTransformado = str(d)
        dTransformado = dTransformado.replace("'", '"')
        #print(dTransformado)
        conn.sendall(dTransformado.encode())
        #conn.sendall("{}".encode())

        return 'Datos reproduccion enviados'
    
    def SizeBase(self,conn):
        #va a buscar archivo con datos de reproduccion actual.
        archivoDatosReprroduccion = "/home/pi/TvPost/Resolutions/base_resolution.txt"
        d = {}
        if (os.path.exists(archivoDatosReprroduccion)):
            with open(archivoDatosReprroduccion) as f:
                for line in f:
                    if 'Width in pixels:-' in line:
                        d['anchoPantalla'] = line[len('Width in pixels:-'):].strip()
                    if 'Height in pixels:-' in line:
                        d['altoPantalla'] = line[len('Height in pixels:-'):].strip()
        #Acá debe retornar el diccionario
        dTransformado = str(d)
        dTransformado = dTransformado.replace("'", '"')
        #print(dTransformado)
        conn.sendall(dTransformado.encode())
        #conn.sendall("{}".encode())

        return 'Datos tamaño enviados'
    
    def DelImagenes(self, nombres):
        os.system('cd /var/www/html/ImagenesPostTv && rm -f{}'.format(nombres))
        os.system('cd /var/www/html/ImagenesPostTv10 && rm -f{}'.format(nombres))
        return 'Imagenes eliminadas'
    
    def EditImagen(self, nombres):
        nombre1 = nombres[1].replace('<!-!>', ' ')
        nombre2 = nombres[2].replace('<!-!>', ' ')
        #print(nombre1, nombre2)
        os.system('cd /var/www/html/ImagenesPostTv && mv {} {}'.format(nombre1, nombre2))
        os.system('cd /var/www/html/ImagenesPostTv10 && mv {} {}'.format(nombre1, nombre2))
        return 'Imagen editada'
    
    def DelVideos(self, nombres):
        os.system('cd /var/www/html/VideosPostTv && rm -f{}'.format(nombres))
        return 'Videos eliminados'
    
    def EditVideos(self, nombres):
        nombre1 = nombres[1].replace('<!-!>', ' ')
        nombre2 = nombres[2].replace('<!-!>', ' ')
        #print(nombre1, nombre2)
        os.system('cd /var/www/html/VideosPostTv && mv {} {}'.format(nombre1, nombre2))
        return 'Video editado'
    
    #Función que redondea números de forma normal
    def normal_round(self, n):
        if n - math.floor(n) < 0.5:
            return math.floor(n)
        return math.ceil(n)
    
    #Función que replica la imagen recibida en todos los formatos de
    #porción. hasta el momento solo se verá en el 10%
    def ReplicaImagen(self, nombre):
        #Remuevo caracteres extra
        nombreConEspacio = nombre.replace('<!-!>', ' ')
        
        #Obtengo tamaños de resolución
        datosSize = "/home/pi/TvPost/Resolutions/base_resolution.txt"
        ancho_total = 0
        alto_total = 0
        ancho_80 = 0
        alto_10 = 0

        if (os.path.exists(datosSize)):
            with open(datosSize) as f:
                for line in f:
                    if 'Width in pixels:-' in line:
                        ancho_total = int(line[len('Width in pixels:-'):].strip())
                    if 'Height in pixels:-' in line:
                        alto_total = int(line[len('Height in pixels:-'):].strip())
            
            #Asigno 80% de ancho y 10 de alto redondeados + 4 para abarcar
            #márgenes verticales
            ancho_80 = self.normal_round((ancho_total * .8))
            alto_10 = self.normal_round((alto_total * .1)) + 4
           
        try:
            #acá tengo que redimensionar la imagen
            os.system("convert /var/www/html/ImagenesPostTv/'{}' "
            "-resize {}x{}! /var/www/html/ImagenesPostTv10/'{}'".format(
                nombreConEspacio, ancho_80, alto_10, nombreConEspacio))
        except:
            print("Error!")
        
        return 'Imagen replicada'
        

    def run(self):
        #print("Conección desde: ", self.clientAddress)
        while True:
            data = conn.recv(8192) #Recive la data
            data = data.decode('utf-8')
            dataMessage = data.split(' ')
            command = dataMessage[0]
            
            if command == 'TVPOSTPING':
                reply = self.ResponderPing()
                conn.send(bytes(reply,"UTF-8"))
                print(reply)
                conn.close()
                return
            
            if command == 'TVPOSTRES':
                reply = self.CambiarResolucion(dataMessage[1], dataMessage[2])
                conn.send(bytes(reply,"UTF-8"))
                print(reply)
                conn.close()
                return
               
            elif command == 'TVPOSTMODLAYOUT':
                reply = self.ModificarLayout(dataMessage)
                conn.send(bytes(reply,"UTF-8"))
                print(reply)
                conn.close()
                return
            
            elif command == 'TVPOSTGETSCREEN':
                respuesta = self.CapturarPantalla(conn)
                print(respuesta)
                conn.close()
                return
            
            elif command == 'TVPOSTCANTIDADIMAGENES':
                respuesta = self.CantidadImagenes(conn)
                print(respuesta)
                conn.close()
                return
            
            #Entrega el listado completo de nombres de imágenes
            elif command == 'TVPOSTGETNOMBREIMAGENES':
                respuesta = self.NombresImagenes(conn)
                print(respuesta)
                conn.close()
                return
            #Comprueba el nombre entrante para ver si existe y no
            #reemplazarlo
            elif 'TVPOSTVERIFICANOMBREIMAGEN' in command:
                respuesta = self.VerificarNombreImagen(conn, dataMessage[1])
                print(respuesta)
                conn.close()
                return

            #Entrega el listado completo de nombres de videos
            elif command == 'TVPOSTGETNOMBREVIDEOS':
                respuesta = self.NombresVideos(conn)
                print(respuesta)
                conn.close()
                return
            #Verifica nombre de video
            elif 'TVPOSTVERIFICANOMBREVIDEO' in command:
                respuesta = self.VerificarNombreVideo(conn, dataMessage[1])
                print(respuesta)
                conn.close()
                return

            elif command == 'TVPOSTGETDATOSREPRODUCCIONACTUAL':
                respuesta = self.DatosReproduccionActual(conn)
                print(respuesta)
                conn.close()
                return
            
            elif command == 'TVPOSTGETSIZEPANTALLA':
                respuesta = self.SizeBase(conn)
                print(respuesta)
                conn.close()
                return
            
            elif command == 'TVPOSTDELIMGS':
                respuesta = self.DelImagenes(data[data.find(' '):])
                conn.send(bytes(respuesta,"UTF-8"))
                print(respuesta)
                conn.close()
                return
            
            elif command == 'TVPOSTEDITIMGS':
                respuesta = self.EditImagen(dataMessage)
                conn.send(bytes(respuesta,"UTF-8"))
                print(respuesta)
                conn.close()
                return
            
            elif command == 'TVPOSTDELVIDEOS':
                respuesta = self.DelVideos(data[data.find(' '):])
                conn.send(bytes(respuesta,"UTF-8"))
                print(respuesta)
                conn.close()
                return
            
            elif command == 'TVPOSTEDITVIDEOS':
                respuesta = self.EditVideos(dataMessage)
                conn.send(bytes(respuesta,"UTF-8"))
                print(respuesta)
                conn.close()
                return
            
            elif command == 'TVPOSTREPLICAIMAGEN':
                respuesta = self.ReplicaImagen(dataMessage[1])
                conn.send(bytes(respuesta,"UTF-8"))
                print(respuesta)
                conn.close()
                return
            
        return

host = ""
port = 5560


#Creates a socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket creado. Esperando conexión...")
except socket.error as msg:
    print("Error al crear socket: "+str(msg))
    
#Binding Socket
try:
    s.bind((host,port))
    
except socket.error as msg:
    print("Error al bind el socket: "+str(msg))
    
try:
    
    while True:
        try:
            s.listen(5)
            conn, address = s.accept()
            newthread = ClientThread(address, conn)
            newthread.start()
        except e as msg:
            print("Error al crear hilo: "+str(msg))
except e as msg:
            print("Error al iniciar loop: "+str(msg))
