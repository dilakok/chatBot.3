<?php
header('Content-Type: text/html; charset=utf-8');
$gelen_veri = $_POST["veri"];

echo json_encode($gelen_veri, JSON_UNESCAPED_UNICODE);
?>