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
$string = utf8_decode($string); // For some reason, this is utf8-encoded twice?
$string = iconv("UTF-8", "ISO-8859-1//TRANSLIT", $string); // convert with char matching

output($string);

function output ($string, $count=0) {
    setlocale(LC_CTYPE, "de_DE@euro"); // This is important to have escapeshellarg working properly

    $output = "/home/rzl/ping-plus-host/pingplus.py -c -s ".escapeshellarg($string);

    exec($output, $returnstring, $retval);

    if ($retval == 1 && $count < 6) {
        output($string, $count++);
    }
}
