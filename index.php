<?php
/**
 * Receives a json request via HTTP POST
 * 
 * The request is specified with the following keys:
 * from: The username
 * text: The text
 * time: The time (not used yet)
 * 
 */
$postdata = file_get_contents("php://input");

$data = json_decode($postdata,true);

$string = "<".$data["from"].":".$data["time"]."> " .$data["text"];

output(utf8_decode($string));

function output ($string, $count=0) {
    $output = "/home/rzl/ping-plus-host/pingplus.py -c -s ".escapeshellarg($string);

    exec($output, $returnstring, $retval);

    if ($retval == 1 && $count < 6) {
        output($string, $count++);
    }
}
