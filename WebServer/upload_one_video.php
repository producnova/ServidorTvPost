<?php
	$video = $_POST['video'];
	$name = $_POST['name'];
	$ruta = "/var/www/html/VideosPostTv/{$name}";

	$videoFinal = base64_decode($video);

	file_put_contents($ruta, $videoFinal);

	echo "Video subido exitosamente";

?>
