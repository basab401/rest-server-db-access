
# rest-server-db-access

* [About](#about)
* [Prerequisites](#prerequisites)
* [How to use it](#use)
* [Maintainers](#maintainers)


## <a name="about">About</a>

This repo contains the source code for a Python-based REST server that allows interactions with JSON data


## <a name="prerequisites">Prerequisites</a>

```
Python3.6 or higher, Flask 1.1.1
```

## <a name="use">How to use it</a>

Run the application as follows.


```bash
python3 rest-server-db-access.py
```


```bash
Ex: curl -XPOST -F "files[]=@/test/1.json" http://localhost:7000/query
Ex: curl -XPOST -F "files[]=@/test/2.json" http://localhost:7000/insert
```

## <a name="maintainers">Maintainers</a>

* Basabjit Sengupta (basab401@yahoo.co.in)
