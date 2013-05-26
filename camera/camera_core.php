<?php

/*
 * ©2013 The Mustached Pi Project
 * == CAMERA EVENTS' CORE FILE ==
 */

function speak ( $what )
{
	file_put_contents('/home/pi/share/voice', $what);
}


