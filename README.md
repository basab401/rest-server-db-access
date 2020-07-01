
# rest-server-db-access

* [About](#about)
* [Prerequisites](#prerequisites)
* [How to use it](#use)
* [Maintainers](#maintainers)


## <a name="about">About</a>

```
This repo contains the source code for a Python-based REST API application that allows interactions document based databases. The repo structure is as below:

├── README.md
├── requirements.txt
├── rest_app
│   ├── config.py
│   ├── __init__.py
│   ├── mongodb.py
|   |── s3_access.py
├── server.py
├── setup.cfg
├── setup.py
└── tests
    ├── __init__.py
    └── test_app.py
```


## <a name="prerequisites">Prerequisites</a>

```
Primary requirements: Python3.6 or higher, Flask 1.1.1 or higher
For details, please see requirements.txt
```

## <a name="use">How to use it</a>

Run the following command from the source root to install the python application named `rest_app`:

```bash
python3.6 setup.py install
```

Run the following to start the server to listen on the API requests:

```bash
python3.6 server.py
```

Sample curl commands to fetch/store documents on Mongodb cluster:

```bash

curl -u <userid>:<pw> http://127.0.0.1:10443/v1/mongodb
curl -u <userid>:<pw> http://127.0.0.1:10443/v1/mongodb/fetch
curl -u <userid>:<pw> -H 'Content-type: application/json' -d '{"id":2, "test_key":"test_value"}' -X POST http://127.0.0.1:10443/v1/mongodb/insert

```

Sample curl commands to upload/download documents(json/text) on s3 store:

```bash

curl -u <userid>:<pw> -XGET  http://127.0.0.1:10443/v1/s3
curl -u <userid>:<pw> -XPOST -F File=@/tmp/uploads/test1.txt http://127.0.0.1:10443/v1/s3/upload
curl -u <userid>:<pw> -XGET  http://127.0.0.1:10443/v1/s3/download/test1.txt

```


## <a name="TODOs">Pending work</a>

* Replace hardcoded Mongodb DB or Collection entities
* Replace hardcoded S3 Bucket name
* Add unit tests for S3 access endpoints
* Support other http methods like PUT, DELETE etc.
* Use ssl certs or keypair based authentication
* Add support for API based credential stores


## <a name="maintainers">Maintainer</a>

* Basabjit Sengupta (basab401@yahoo.co.in)
