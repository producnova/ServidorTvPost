import os
import subprocess
import re
import math

#list of User folders
usr = os.listdir("/home")

def check_amount_monitors():
    info = subprocess.run("bash ~/TvPost/Bash_files/Screen_divitions_config/check_active_monitors.sh",
                          shell=True,
                          capture_output=True,
                          text=True)
    return info.stdout


def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)


def formato_80_20_10():
    
        #Check that the base resolutions file exsits
    os.system('python3 /home/pi/TvPost/Py_files/Screen_format/Screen_info.py')
    
    
    resolution_values=[]
    
    try:
        with open(os.path.join("/home", usr[0], "TvPost/Resolutions", "base_resolution.txt")) as file:
            for line in file:
                regex = re.search(r':-(.+)', line)
                if regex:
                    resolution_values.append(regex.group(1))
    except:
        print('No se encuentra el archivo')
        
    
    #Pass the argument to screen layout bash
    #$1 = width in pixels
    #$2 = width in mm
    #$3 = height in pixels
    #$4 = height in mm
    #$5 = width in pixels 80
    #$6 = width in mm 80
    #$7 = height in pixels 80
    #$8 = width in mm
    #$9 = video adapter name
    #$10 = amount of active monitors (Split screen already selected and functioning)
    #for value in resolution_values:
      #  print(value)
    #Gettin active monitors
    #####Calculate and round portions###
    width_pixel_80 = str(normal_round(float(resolution_values[0]) * .8))
    width_mm_80 = str(normal_round(float(resolution_values[1]) * .8))
    height_pixel_80 = str(normal_round(float(resolution_values[2]) * .9))
    height_mm_80 = str(normal_round(float(resolution_values[3]) * .9))
    
    valoresPorcentajesCalculados = []
    valoresPorcentajesCalculados.append(resolution_values[0])
    valoresPorcentajesCalculados.append(resolution_values[1])
    valoresPorcentajesCalculados.append(resolution_values[2])
    valoresPorcentajesCalculados.append(resolution_values[3])
    valoresPorcentajesCalculados.append(width_pixel_80)
    valoresPorcentajesCalculados.append(width_mm_80)
    valoresPorcentajesCalculados.append(height_pixel_80)
    valoresPorcentajesCalculados.append(height_mm_80)
    valoresPorcentajesCalculados.append(resolution_values[4])
    valoresPorcentajesCalculados.append(int(check_amount_monitors()))
    #print(valoresPorcentajesCalculados)
    os.system('bash ~/TvPost/Bash_files/Screen_divitions_config/80_20_10_reloj.sh {} {} {} {} {} {} {} {} {} {}'.format(
        valoresPorcentajesCalculados[0],
        valoresPorcentajesCalculados[1],
        valoresPorcentajesCalculados[2],
        valoresPorcentajesCalculados[3],
        valoresPorcentajesCalculados[4],
        valoresPorcentajesCalculados[5],
        valoresPorcentajesCalculados[6],
        valoresPorcentajesCalculados[7],
        valoresPorcentajesCalculados[8],
        valoresPorcentajesCalculados[9])
              )
    #print(resolution_values)

formato_80_20_10()
