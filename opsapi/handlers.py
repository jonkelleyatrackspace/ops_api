#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: handlers.py
# authors: anthony tarola
# ---
# license: the mit license
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the above copyright notice and this permission notice shall being included
# in all copies or substantial portions of the Software.

import logging
import httplib
import json
import crypt
import base64
import difflib

from passlib.apache import HtpasswdFile
from tornado import gen
from tornado.web import RequestHandler, HTTPError, asynchronous

from opsapi.config import config
from opsapi.extensions import create_collection
from opsapi.util import route

log = logging.getLogger(__name__)


class BaseHandler(RequestHandler):
    """ Contains helper methods for all request handlers """

    def prepare(self):
        self.handle_params()
        self.handle_auth()

    def handle_params(self):
        """ automatically parse the json body of the request """

        self.params = {}
        content_type = self.request.headers.get(
            "Content-Type", 'application/json')

        if (content_type.startswith("application/json")) or (config['force_json']):
            if self.request.body in [None, ""]:
                return

            self.params = json.loads(self.request.body)
        else:
            # we only handle json, and say so
            raise HTTPError(
                400, "This application only support json, please set the http header Content-Type to application/json")

    def handle_auth(self):
        """ authenticate the user """

        # no passwords set, so they're good to go
        if config['passfile'] == None:
            return

        # grab the auth header, returning a demand for the auth if needed
        auth_header = self.request.headers.get('Authorization')
        if (auth_header is None) or (not auth_header.startswith('Basic ')):
            self.auth_challenge()
            return

        # decode the username and password
        auth_decoded = base64.decodestring(auth_header[6:])
        username, password = auth_decoded.split(':', 2)

        if not self.is_user_authenticated(username, password):
            self.auth_challenge()
            return

    def is_user_authenticated(self, username, password):
        passfile = HtpasswdFile(config['passfile'])

        # is the user in the password file?
        if not username in passfile.users():
            return False

        return passfile.check_password(username, password)

    def auth_challenge(self):
        """ return the standard basic auth challenge """

        self.set_header("WWW-Authenticate", "Basic realm=pyjojo")
        self.set_status(401)
        self.finish()

    def write(self, chunk):
        """ if we get a dict, automatically change it to json and set the content-type """

        if isinstance(chunk, dict):
            chunk = json.dumps(chunk)
            self.set_header("Content-Type", "application/json; charset=UTF-8")

        super(BaseHandler, self).write(chunk)

    def write_error(self, status_code, **kwargs):
        """ return an exception as an error json dict """

        if kwargs['exc_info'] and hasattr(kwargs['exc_info'][1], 'log_message'):
            message = kwargs['exc_info'][1].log_message
        else:
            # TODO: What should go here?
            message = ''

        self.write({
            'error': {
                'code': status_code,
                'type': httplib.responses[status_code],
                'message': message
            }
        })


@route(r"/extension_names/?")
class ExtensionNamesCollectionHandler(BaseHandler):

    def get(self):
        """ get the requirements for all of the extensions """

        tags = {'tags': [], 'not_tags': [], 'any_tags': []}

        for tag_arg in ['tags', 'not_tags', 'any_tags']:
            try:
                tags[tag_arg] = self.get_arguments(tag_arg)[0].split(',')
                break
            except IndexError:
                continue

        self.finish({'extension_names': self.settings[
                    'extensions'].name(tags)})


@route(r"/extensions/?")
class ExtensionCollectionHandler(BaseHandler):

    def get(self):
        """ get the requirements for all of the extensions """

        tags = {'tags': [], 'not_tags': [], 'any_tags': []}

        for tag_arg in ['tags', 'not_tags', 'any_tags']:
            try:
                tags[tag_arg] = self.get_arguments(tag_arg)[0].split(',')
                break
            except IndexError:
                continue

        self.finish({'extensions': self.settings['extensions'].metadata(tags)})


@route(r"/extensions/([\w\-]+)/?")
class ExtensionDetailsHandler(BaseHandler):

    def options(self, extension_name):
        """ get the requirements for this extension """

        extension = self.get_extension(extension_name, 'options')
        self.finish({'extension': extension.metadata()})

    @asynchronous
    @gen.engine
    def get(self, extension_name):
        """ run the extension """

        if config['force_json']:
            self.set_header("Content-Type", "application/json; charset=UTF-8")

        extension = self.get_extension(extension_name, 'get')

        if extension.output == 'combined':
            retcode, stdout = yield gen.Task(extension.execute, self.params)
            self.finish({
                "out": self.filter_return_values(stdout),
                "values": self.find_return_values(stdout),
                "status": retcode
            })
        else:
            retcode, stdout, stderr = yield gen.Task(extension.execute, self.params)
            self.finish({
                "out": self.filter_return_values(stdout),
                "err": self.filter_return_values(stderr),
                "values": self.find_return_values(stdout),
                "status": retcode
            })

    @asynchronous
    @gen.engine
    def delete(self, extension_name):
        """ run the extension """

        if config['force_json']:
            self.set_header("Content-Type", "application/json; charset=UTF-8")

        extension = self.get_extension(extension_name, 'delete')

        if extension.output == 'combined':
            retcode, stdout = yield gen.Task(extension.execute, self.params)
            self.finish({
                "out": self.filter_return_values(stdout),
                "values": self.find_return_values(stdout),
                "status": retcode
            })
        else:
            retcode, stdout, stderr = yield gen.Task(extension.execute, self.params)
            self.finish({
                "out": self.filter_return_values(stdout),
                "err": self.filter_return_values(stderr),
                "values": self.find_return_values(stdout),
                "status": retcode
            })

    @asynchronous
    @gen.engine
    def put(self, extension_name):
        """ run the extension """

        if config['force_json']:
            self.set_header("Content-Type", "application/json; charset=UTF-8")

        extension = self.get_extension(extension_name, 'put')

        if extension.output == 'combined':
            retcode, stdout = yield gen.Task(extension.execute, self.params)
            self.finish({
                "out": self.filter_return_values(stdout),
                "values": self.find_return_values(stdout),
                "status": retcode,
            })
        else:
            retcode, stdout, stderr = yield gen.Task(extension.execute, self.params)
            self.finish({
                "out": self.filter_return_values(stdout),
                "err": self.filter_return_values(stderr),
                "values": self.find_return_values(stdout),
                "status": retcode
            })

    @asynchronous
    @gen.engine
    def post(self, extension_name):
        """ run the extension """

        if config['force_json']:
            self.set_header("Content-Type", "application/json; charset=UTF-8")

        extension = self.get_extension(extension_name, 'post')

        if extension.output == 'combined':
            retcode, stdout = yield gen.Task(extension.execute, self.params)
            self.finish({
                "out": self.filter_return_values(stdout),
                "values": self.find_return_values(stdout),
                "status": retcode
            })
        else:
            retcode, stdout, stderr = yield gen.Task(extension.execute, self.params)
            self.finish({
                "out": self.filter_return_values(stdout),
                "err": self.filter_return_values(stderr),
                "values": self.find_return_values(stdout),
                "status": retcode
            })

    def get_extension(self, extension_name, http_method):
        extension = self.settings['extensions'].get(extension_name, None)

        if extension is None:
            raise HTTPError(
                404, "Extension with name '{0}' not found".format(extension_name))

        if http_method == 'options':
            return extension

        if extension.http_method != http_method:
            raise HTTPError(405, "Wrong HTTP method for extension '{0}'. Use '{1}'".format(
                extension_name, extension.http_method.upper()))

        return extension

    def find_return_values(self, output):
        """ parse output array for return values """

        return_values = {}
        for line in output:
            if line.startswith('return_value'):
                temp = line.replace("return_value", "").strip()
                key, value = [item.strip() for item in temp.split('=')]
                return_values[key] = value

        return return_values

    def filter_return_values(self, output):
        """ do not return the return values in the stdout
            or stderr as we're displaying that with
            self.find_return_values()
        """
        lines = []
        for line in output:
            if not line.startswith('return_value'):
                lines.append(line)

        return lines


@route(r"/reload/?")
class ReloadHandler(BaseHandler):

    def post(self):
        """ reload the extensions from the extensions directory """
        self.settings['extensions'] = create_collection(config['directory'])
        self.finish({"status": "ok"})
