# opsAPI

Expose the routes directory as simple extensible automation scripts

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

    opsapi -d --dir /srv/pyjojo
    curl -XPOST http://localhost:3000/scripts/echo -H "Content-Type: application/json" -d '{"text": "hello world!"}'

You should see this as a response:

    {
      "status": 0,
      "values": {
          "age": "99", 
          "name": "bob"
      },
      "err": [],
      "out": [
          "echo'd text: hello world!"
      ]
    }

## Usage

    Usage: opsapi [options] <htpasswd>

    Expose a directory of bash scripts as an API.

    Note: This application gives you plenty of bullets to shoot yourself in the
    foot!  Please use the SSL config options, give a password file, and either
    whitelist access to it via a firewall or keep it in a private network.

    You can use the apache htpasswd utility to create your htpasswd files.

    Options:
      -h, --help            show this help message and exit
      -d, --debug           Start the application in debugging mode.
      --dir=DIRECTORY       Base directory to parse the scripts out of
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

### JoJo Block Markup

JoJo blocks are metadata about the script that opsapi will use to execute it.  JoJo blocks are not mandatory for the script to run.

Example block:

    # -- jojo --
    # description: echo script
    # param: text - text to echo back
    # param: secret1 - sensitive text you don't want logged
    # param: secret2 - more sensitive stuff
    # filtered_params: secret1, secret2
    # tags: test, staging
    # http_method: get
    # lock: False
    # -- jojo -- 

Fields:

  - **description**: information about what a script does
    - format: description: [*text*]
  - **param**: specifies a parameter to the script, will be passed in as environment params, with the name in all caps.  One per line.
    - format: param: *name* [- *description*]
  - **filtered_params**: specifies a list of parameters that you have already specified, but want to ensure that the values are not logged.
    - format: filtered_params: item1 [,item2]
  - **tags**: specifies a list of tags that you want displayed when querying opsapi about scripts.
    - format: tags: item1 [,item2]
  - **http_method**: specifies the http method the script should respond to.
    - format: http_method: get
    - allowed_values: get|put|post|delete
    - default: post
  - **output**: specifies if the output should be 'split' into stderr and stdout or 'combined' into stdout.
    - format: output: combined
    - allowed_values: split|combined
    - default: split
  - **lock**: if true, only one instance of the script will be allowed to run
    - format: lock: True
    - default: False
    
### Script List

Returns information about all the scripts.

    GET /scripts

Optional Tag Query Parameters:
 - format: ?param=tag1,tag2
 - only one param type may be used per query.
 - params available
   - tags: only those scripts which match *ALL* tags will be returned
   - not_tags: only those scripts which do no have *ANY* of the tags will be returned
   - any_tags: scripts that match *ANY* tags will be returned


### Script Names List

Returns list of names of all scripts

    GET /script_names

Optional Tag Query Parameters:
 - format: ?param=tag1,tag2
 - only one param type may be used per query.
 - params available
   - tags: only those scripts which match *ALL* tags will be returned
   - not_tags: only those scripts which do no have *ANY* of the tags will be returned
   - any_tags: scripts that match *ANY* tags will be returned


### Get Information about a Script

Returns information about the specified script.

    OPTIONS /scripts/{script_name}

### Run a Script

Executes the specified script and returns the results.

    POST /scripts/{script_name}

### Reload the script directories

Reloads the scripts in the script directory.

    POST /reload
