<?php
	$prefix = "http://localhost/stock";

	$host = "localhost";
	$username = "root";
	$password = "";
	$database = "stock";

	if (stripos($_SERVER['SERVER_ADDR'], '172') === false && stripos($_SERVER['SERVER_ADDR'], '10') === false && $_SERVER['SERVER_ADDR'] !== '::1')
	{
		$prefix = "http://www.cuzn1024.com/stock";
		$host = "localhost";
		$username = "cuzncom_zqzb";
		$password = "Cuzn1024";
		$database = "cuzncom_zqzb";
	}
?>