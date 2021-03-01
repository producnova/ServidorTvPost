#!/bin/sh
echo "*****Renombrando servidor anterior*****"
sudo mv ~/TvPost ~/TvPostAnterior
echo "*****Descargando Repositorios*****"
cd ~
if ! git clone --recurse-submodules -j8 https://github.com/producnova/ServidorTvPost TvPost
then
	echo "***************************ERROR***********************************"
	echo "Descarga de repositorio fallida.Revise la dirección del repositorio";
	echo "*****Volviendo a versión anterior*****"
	sudo mv ~/TvPostAnterior ~/TvPost
else
	echo "*****Eliminando servidor TvPost anterior*****"
	sudo rm -rf ~/TvPostAnterior
	echo "*****Moviendo WebSockify*****"
	sudo cp ~/TvPost/websockify ~/TvPost/noVNC/utils/
	echo "*****Instalando Pyrebase (Comunicación Cloud)*****"
	sudo pip3 install pyrebase
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
fi

