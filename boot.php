<?php

/*
 * The Mustached Pi Project
 * (c)2013
 *
 * Start processes
 */

echo "Starting processes";

$s = "";
echo "\n1. Starting voice server";
$s .= exec("php /home/pi/code/voice.php > /home/pi/share/voice.log &");
echo "\n2. Starting python client";
$s .= exec("python /home/pi/code/client.py > /home/pi/share/mpi.log &");
echo "\n3. Starting video server";
$s .= exec("motion -c /home/pi/code/motion.conf > /home/pi/share/motion.log &");

file_put_contents("/home/pi/share/boot.log", $s);
file_put_contents("/home/pi/share/voice", "Welcome to the Mustached Pi Project");
