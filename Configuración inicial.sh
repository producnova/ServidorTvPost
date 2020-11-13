#!/bin/sh
echo "*****Descargando Repositorios*****"
cd ~
git clone --recurse-submodules -j8 https://github.com/producnova/TvPost
echo "*****Configurando Web Server*****"
bash ~/TvPost/Bash_files/First_config/WebServer_TvPost.sh
echo "*****Software de terceros*****"
bash ~/TvPost/Bash_files/First_config/Third_party_software.sh
echo "Recuerde configurar xscreensaver para deshabilitar el apagado de pantalla"
sleep 2
echo "Reiniciando en 5 segundos..."
sleep 1
echo "Reiniciando en 4 segundos..."
sleep 1
echo "Reiniciando en 3 segundos..."
sleep 1
echo "Reiniciando en 2 segundos..."
sleep 1
echo "Reiniciando en 1 segundo..."
sleep 1
sudo reboot
