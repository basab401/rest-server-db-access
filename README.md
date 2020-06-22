
# rest-server-db-access

* [About](#about)
* [Prerequisites](#prerequisites)
* [How to use it](#use)
* [Maintainers](#maintainers)


## <a name="about">About</a>

This repo contains the source code for a Python-based REST server that allows interactions with JSON data


## <a name="prerequisites">Prerequisites</a>

```
Primary requirements: Python3.6 or higher, Flask 1.1.1 or higher
For details, please see requirements.txt
```

## <a name="use">How to use it</a>

Start the API server as follows:


```bash
cd rest_server
python3 server.py
```


```bash
Ex:
curl -u <userid>:<pw> http://127.0.0.1:10443/v1/mongodb
curl -u <userid>:<pw> -H 'Content-type: application/json' -d '{"id"}' -X GET http://127.0.0.1:10443/v1/mongodb
curl -u <userid>:<pw> -H 'Content-type: application/json' -d '{"id":2, "test_key":"test_value"}' -X POST http://127.0.0.1:10443/v1/mongodb
curl -u <userid>:<pw> -H 'Content-type: application/json' -d '{"id":3, "test_key":"test_value"}' -X POST http://127.0.0.1:10443/v1/mongodb 
```

## <a name="maintainers">Maintainers</a>

* Basabjit Sengupta (basab401@yahoo.co.in)
