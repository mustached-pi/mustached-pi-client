<?php

/*
 * The Mustached Pi Project
 * (c)2013
 *
 * Voice server
 */

$file = "/home/pi/share/voice";

while ( true ) {

    $s = file_get_contents($file);
    if ( $s ) {
	file_put_contents($file, "");
        exec("flite -voice slt \"{$s}\"");
	echo date("d-m-Y H:i:s") . " |  " . strtoupper($s) . "\n";
    }
    usleep(10000);

}
