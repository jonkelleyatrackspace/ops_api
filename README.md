# opsApi

OpsAPI is a lightweight API/HTTP framework in Tornado which allows users to extend and prototype infrastructure-as-a-service designs in hours not weeks!

This project was built for systems engineers and developers who need to automate orchestration of tasks on a system and can appreciate the speed and convienence of a stateless API. You can automate anything with the built in extensions for subprocess, fabric, ansible, postgres, mysql or memcache.  Your imagination is your prototypes limit. Combined with a tool such as [marmelab/ng-admin](https://github.com/marmelab/ng-admin) and HTTP proxies anyone can consume the services securely!

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

The API has input string management classes to handle the possibility of bad-actor injection attempts. This API should never be exposed without authentication, but if you do then there are a few precautions to delay compromise.

Do I want to CREATE a role or DROP the postgres role?

    curl -XPOST http://localhost:3000/extensions/psql_create_role -H "Content-Type: application/json" -d '{ "role": "jonkelley", "password": "SERVER'\''; DROP ROLE postgres;HACKED", "connection_limit": "3"}'

This request is audited by a log event `SecurityFaultDangerousUserInput value: "SERVER'; DROP ROLE postgres;HACKED"`

You should see this response:

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

## Command Line Usage

NOTE: You can use the apache htpasswd utility (from `apache2-utils` or `httpd-tools`), to create your htpasswd files.


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

This API can support YAML configuration files from some usual locations or with the --config startup parameter, if you want to get fancy. The aggregated configurations are merged into a running configuration.  NOTE: Syntax is key: v. Only python objects allowed as values. Native YAML lists and hash syntax are unsupported!

The a default config file sample is located in `opsapi.yaml` and will be used if you start `opsapi` from the git repository.

The default load locations for configuration files are:

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
    
### Extensions List

Returns information about all the extension.

    GET /extensions

Optional Tag Query Parameters:
 - format: ?param=tag1,tag2
 - only one param type may be used per query.
 - params available
   - tags: only those extensions which match *ALL* tags will be returned
   - not_tags: only those extensions which do no have *ANY* of the tags will be returned
   - any_tags: extensions that match *ANY* tags will be returned


### Extensions Names List

Returns list of names of all pluggable extensions

    GET /extension_names

Optional Tag Query Parameters:
 - format: ?param=tag1,tag2
 - only one param type may be used per query.
 - params available
   - tags: only those extensions which match *ALL* tags will be returned
   - not_tags: only those extensions which do no have *ANY* of the tags will be returned
   - any_tags: extensions that match *ANY* tags will be returned


### Get Information about an extension

This will return the help parameters, description, and other data about an extension.

    OPTIONS /extensions/{extension_name}

### Run a extension

You would execute POST data to an extension and return results with

    POST /extensions/{extension_name}

### Reload the extension directories

This request will reload updates to code in the extensions

    POST /reload
