iVelum Proxy
=================

Code challenge 
https://github.com/ivelum/job/blob/master/code_challenges/python.md

***Build***
```bash
docker build -t habr-proxy -f docker/Dockerfile .
```

***Available options***

```bash
docker run -it --rm habr-proxy -h
```

```
usage: main.py [-h] [-l [WORD_LENGTH]] [-t [WORD_APPEND]] [-u [UPSTREAM]] [--host [HOST]] [--port [PORT]]

iVelum proxy

optional arguments:
  -h, --help            show this help message and exit
  -l [WORD_LENGTH], --len [WORD_LENGTH]
                        Word length
  -t [WORD_APPEND], --text [WORD_APPEND]
                        Text appended to words
  -u [UPSTREAM], --up [UPSTREAM], --upstream [UPSTREAM]
                        Upstream URL (e.g. 'https://example.com')
  --host [HOST]         HTTP server listen address
  --port [PORT]         HTTP server listen port
```

***Run proxy***

```bash
docker run -it --rm -p 8080:8080 habr-proxy
```
