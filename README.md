# opsAPI

Lightweight API framework with simple extension SDK to allow rapid prototype of fairly complex infrastructure-as-a-service concepts.

Use the apache htpasswd utility (from `apache2-utils` or `httpd-tools`), to create your htpasswd files.

## Quick dev environment

You will need to `pip install paver` first.

You can then leverage the following paver commands like a make/rake task:

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

## Usage

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
