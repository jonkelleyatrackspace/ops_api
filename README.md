# opsAPI

Expose directory routes with a simple Python SDK and API
Use the apache htpasswd utility to create your htpasswd files.

## Quick dev environment

You will need to `pip install paver` first.

Install the cloned opsapi source with paver:

    paver setup

Start a local dev server:

    paver start

Start a local dev server:

    paver start

## Tutorial

Start up opsapi and hit it with curl:

    opsapi -d --dir /srv/extensions
    curl -XPOST http://localhost:3000/extensions/echo -H "Content-Type: application/json" -d '{"text": "hello world!"}'

You should see this as a response:

    "debug": {
        "err": [],
        "out": [
            "echo'd text: hello world!"
        ]
    },
    "job": {
        "results": {
            "age": "99",
            "name": "bob"
        },
        "status": 0
    }

## Usage

    Usage: opsapi [options] <htpasswd>

    This will expose a set of opsapi extensions as a REST API.

    Options:
      -h, --help            show this help message and exit
      -d, --debug           Start the application in debugging mode.
      --dir=DIRECTORY       Base directory to parse the extensions out of
      --force-json          Treats all calls as if they sent the 'Content-Type: application/json' header.  May produce unexpected results
      -p PORT, --port=PORT  Set the port to listen to on startup.
      -a ADDRESS, --address=ADDRESS
                            Set the address to listen to on startup. Can be a
                            hostname or an IPv4/v6 address.
      -c CERTFILE, --certfile=CERTFILE
                            SSL Certificate File
      -k KEYFILE, --keyfile=KEYFILE
                            SSL Private Key File
      -u UNIX_SOCKET, --unix-socket=UNIX_SOCKET
                            Bind opsapi to a unix domain socket

## API

### Configuration Block Markup

Config blocks are metadata about the extension that opsapi will use to execute it.  Config blocks are not mandatory for the extension to run.

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
    # -- config -- 

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
  - **lock**: if true, only one instance of the extension will be allowed to run
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

Returns information about the specified extension.

    OPTIONS /extensions/{extension_name}

### Run a extension

Executes the specified extension and returns the results.

    POST /extensions/{extension_name}

### Reload the extension directories

Reloads the extensions in the extension directory.

    POST /reload
