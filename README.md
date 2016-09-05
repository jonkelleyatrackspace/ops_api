# opsApi

OpsAPI is a lightweight API/HTTP framework in Tornado which allows users to extend and prototype mid complexity API designs and process solutions -- hours not weeks. I promise. 

This is intended to empower systems engineers and developers looking to cut the lifting out of running their ops shop. Yes there's Rundeck/Jenkin's but you can't build a larger platform on top of that -- this API is the missing loose couple. Use the pluggable nature of this API and you can hook Ansible, Fabric, or local Postgres bindings from Rundeck OR Jenkins.

A real wizard could have multiple opsAPI deployments interconnected with Python-requests to create complex build pipelines and processes. Then they would use the beautiful [marmelab/ng-admin](https://github.com/marmelab/ng-admin) to create a browser app. Ditch Jenkins. Now where's the beach?

## Quick dev environment

You will need to `pip install paver` first, then just type `make`!

These other paver tasks are available to you.

    paver setup           - Copy, Install & configure the components for running a local server (sudo)
    paver start           - Install & configure git repo to system and start local dev instance (sudo)
    paver load_extensions - Copy the git repo extensions to /srv/extensions (sudo)
    paver build_rpm       - Build an RPM artefact
    paver clean           - Clean up paver/build/artefacts so you can do git stuff

## Tutorial

After installing with paver, start the API and perform a test request:

    opsapi -d --dir /srv/extensions
    curl -XPOST http://localhost:3000/extensions/test -H "Content-Type: application/json" -d '{ "name": "bob", "age": "31"}'

You should see this response:

    {
        "debug": {
            "err": [],
            "out": []
        },
        "request": {
            "age": 31,
            "current_datetime": "2016-09-03 21:35:00.877164",
            "name": "bob",
            "return": "You were born in 1985"
        }
    }

## Real-World Examples

### Postgres Examples

Create a Postgres role called jonkelley. 

    curl -XPOST http://localhost:3000/extensions/psql_create_role -H "Content-Type: application/json" -d '{ "role": "jonkelley", "password": "qwerty", "connection_limit": "3"}' 

You should see this response:

    {
        "debug": {
            "err": [],
            "out": [
                "BEGIN; CREATE ROLE jonkelley WITH  CONNECTION LIMIT 3  NOCREATEUSER  NOCREATEROLE  NOCREATEDB  NOINHERIT  NOLOGIN  UNENCRYPTED  PASSWORD 'qwerty' ; END;",
                "BEGIN",
                "CREATE ROLE",
                "COMMIT",
                ""
            ]
        },
        "request": {
            "result": "ok",
            "status": 0
        }
    }

Attempt to drop the role billgates

    curl -XPOST http://localhost:3000/extensions/psql_drop_role -H "Content-Type: application/json" -d '{ "role": "billgates"}'

You should see this response:

    {
        "debug": {
            "err": [
                "psql:/tmp/tmpVeJay3:1: ERROR:  role \"billgates\" does not exist",
                "psql:/tmp/tmpVeJay3:1: ERROR:  role \"billgates\" does not exist",
                "ROLLBACK"
            ],
            "out": [
                "BEGIN; DROP ROLE billgates; END;",
                "BEGIN",
                "psql:/tmp/tmpVeJay3:1: ERROR:  role \"billgates\" does not exist",
                "ROLLBACK",
                ""
            ]
        },
        "request": {
            "errors": [
                "TRANSACTION_ROLLBACK",
                "SQL_ERROR",
                "ROLE_DOES_NOT_EXIST"
            ],
            "result": "rollback",
            "status": 1
        }
    }


### Ansible Examples

Todo

### Fabric Examples

Todo

### MySQL Examples

Todo

### Memcache Examples

Todo

## API Input Parsing / Limit Features

Depending on how you set up your param requirements in the SDK, the API has a bunch of built in filtering and input management options you can manage.

Example of integer enforcement using `param.max_int` for invalid age:

    curl -XPOST http://localhost:3000/extensions/test -H "Content-Type: application/json" -d '{ "name": "bob", "age": "wat}'

You should see this response:
   
    {
        "debug": {
            "err": [
                "Parameter `age` provided with value: wat, expected: PARAMETER_ERROR_IS_NOT_INTEGER value."
        ],
            "out": []
        },
        "request": {
             "status": "422 Unprocessable Entity",
             "troubleshoot": [
                 "INPUT_NOT_AN_INT"
             ]
        }
    }

Example of parameter size limits using `param.max_length`:

    curl -XPOST http://localhost:3000/extensions/test -H "Content-Type: application/json" -d '{ "name": "jon", "age": "2030"}'

You should see this response:

    {
        "debug": {
            "err": [
                "Parameter `age` provided with value: too large, expected: input less than 3 bytes value."
            ],
            "out": []
        },
        "request": {
            "status": "422 Unprocessable Entity",
            "troubleshoot": [
                "BUFFER_SIZE"
            ]
        }
    }

    
Example of of handling empty input parameters (when they are required)

    curl -XPOST http://localhost:3000/extensions/psql_create_role -H "Content-Type: application/json" -d '{ "role": "jonkelley"}'

You should see this response:

    {
        "debug": {
            "err": [
                "Parameter `password` provided with value: <NULL> which cannot be undefined"
            ],
            "out": []
        },
        "request": {
            "status": "422 unprocessable_entity",
            "troubleshoot": [
                "UNDEFINED_INPUT_ERROR"
            ]
        }
    }


## Security Model

The API has input string management classes to handle the possibility of bad-actor injection attempts. This will prevent most casual to intermediate attempts of injection using a variety of known methods. **Absolutely no security will be foolproof.** Always use trusted authentication in front of this service or htpasswd.


Here is a demonstration attempt of SQL injection, naughty naughty.

    curl -XPOST http://localhost:3000/extensions/psql_create_role -H "Content-Type: application/json" -d '{ "role": "jonkelley", "password": "SERVER'\''; DROP ROLE postgres;HACKED", "connection_limit": "3"}'

System Log: `EXCEPTION: SecurityFaultDangerousUserInput value: "SERVER'; DROP ROLE postgres;HACKED"`

The user should see this response:

    {
        "debug": {
            "err": [
                "Internal Server Error"
            ],
            "out": [
                ""
            ]
        },
        "request": {
            "errors": "",
            "status": "500 Internal Server Error"
        }
    }

Special characters and other items that JSON cannot tokenize are invalid. Any knwon abilities to fuzz past the escape filters seems pretty difficult at this stage. 

## Command Line Usage

NOTE: You can use the apache htpasswd utility to create a htpasswd file for embedded www-basic-auth. That means install the `apache2-utils` deb or `httpd-tools` rpm while you're at it.

    Usage: opsapi [options] <htpasswd>

    This will expose a set of opsapi extensions as a REST API.

    Note: Please make sure this application is behind authentication for security.
    Please use the SSL config options, give a passwd file, and either whitelist
    access to the API via firewall or keep it on a privately routed network.

    Use the apache htpasswd utility to create your htpasswd files.

    Options:
      -h, --help            show this help message and exit
      -d, --debug           Start the application with debug enabled.
      --dir=DIRECTORY       Directory to load SDK extensions from
      --force-json          Force the application to treat all incoming requests
                            as 'Content-Type: application/json'
      --config              Provide a YAML file to load config options from.
                            NOTE: Syntax is key: v; python objects allowed as values.
                            Native YAML lists and hash syntax are unsupported.

      -p PORT, --port=PORT  The listening port
      -a ADDRESS, --address=ADDRESS
                            Listening interface. Can be a hostname or an IPv4/v6
                            address.
      -c CERTFILE, --certfile=CERTFILE
                            SSL Cert File
      -k KEYFILE, --keyfile=KEYFILE
                            SSL Private Key File
      -u UNIX_SOCKET, --unix-socket=UNIX_SOCKET
                            Bind opsapi to a unix domain socket

## Configuration File Options

Some features may require additional configuration.

This API can support YAML configuration files from some usual locations or with the --config option if you really need it. NOTE: All the configurations are merged into the running configuration if loaded.  NOTE: Syntax supports key: v with full python eval support. NOTE:  YAML Style list and hashes are not supported.

The default config has some interesting options in `opsapi.yaml`, you should take a look and configure.

The default load locations on startup are:

* `/etc/opsapi.{yaml,yml}`
* `./opsapi.{yaml,yml}`
* `/etc/opsapi/opsapi.{yaml,yml}`
* `~/opsapi.{yaml,yml}`

## Using the extension SDK

### Extension file header config blocks

Config blocks help build metadata about the extension that opsapi is loading into memory.  Config blocks are not mandatory for the extension to run (only if you reference params).

Example block:

    # -- config --
    # description: This is just an example extension
    # param: text - text to echo back
    # param: secret1 - sensitive text you don't want logged
    # param: secret2 - more sensitive stuff
    # filtered_params: secret1, secret2
    # tags: test, staging
    # http_method: get
    # lock: False
    # -- end config -- 

Fields:

  - **description**: information about what an extension does
    - format: description: [*text*]
  - **param**: specifies a parameter to the extension, will be passed in as environment params, with the name in all caps.  One per line.
    - format: param: *name* [- *description*]
  - **filtered_params**: specifies a list of parameters that you have already specified, but want to ensure that the values are not logged.
    - format: filtered_params: item1 [,item2]
  - **tags**: specifies a list of tags that you want displayed when querying opsapi about extensions.
    - format: tags: item1 [,item2]
  - **http_method**: specifies the http method the extension should respond to.
    - format: http_method: get
    - allowed_values: get|put|post|delete
    - default: post
  - **output**: specifies if the output should be 'split' into stderr and stdout or 'combined' into stdout.
    - format: output: combined
    - allowed_values: split|combined
    - default: split
  - **lock**: if true, only one instance of the extension will be allowed to run. useful to prevent RACE conditions if your code cannot support parallelism 
    - format: lock: True
    - default: False

### Extension Python SDK

Todo

### Extensions List

Get a list of all loaded extensions with parameters and options.

    GET /extensions

Optional Tag Query Parameters:
 - format: ?param=tag1,tag2
 - only one param type may be used per query.
 - params available
   - tags: only those extensions which match *ALL* tags will be returned
   - not_tags: only those extensions which do no have *ANY* of the tags will be returned
   - any_tags: extensions that match *ANY* tags will be returned


### Extensions Names List

Returns list of names of all loaded extensions

    GET /extension_names

Optional Tag Query Parameters:
 - format: ?param=tag1,tag2
 - only one param type may be used per query.
 - params available
   - tags: only those extensions which match *ALL* tags will be returned
   - not_tags: only those extensions which do no have *ANY* of the tags will be returned
   - any_tags: extensions that match *ANY* tags will be returned

### Get help on specific extension

This will return config block metadata for one specific extension. Note the rarely used OPTIONS http method.

    OPTIONS /extensions/{extension_name}

### Trigger an extension

You would execute POST data to an extension and return results with

    POST /extensions/{extension_name}

You would execute GET to an extension to just read data from it.

    GET /extensions/{extension_name}

### Reload the extension directories

Reloads *Disk Configs* and all *Extension* code into memory without restart.

    POST /reload
