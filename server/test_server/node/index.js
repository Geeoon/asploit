import fs from 'fs';
import http from 'http';

const server = http.createServer((req, res) => {
    try {
    if (req.url == "/" && req.method == "GET") {
            fs.readFile('pages/home.html', 'utf-8', (err, data) => {
                if (err) {
                    throw err;
                }
                res.writeHead(200, { "Content-Type": "text/html" });
                const [major, minor, patch] = process.versions.node.split('.').map(Number);
                let out = data.replace('{NODE_VERSION}', major+'.'+minor+'.'+patch);
                res.end(out);
            });
        } else {
            fs.readFile('pages/404.html', (err, data) => {
                if (err) {
                    throw err;
                }
                res.writeHead(404, { "Content-Type": "text/html" });
                res.end(data);
            });
        }
    } catch (e) {
        res.writeHead(500, { "Content-Type": "text/text" });
        res.end("Internal Server Error");
        console.log(e);
    }
});

server.listen(8000, () => {
    console.log("Running.");
});
