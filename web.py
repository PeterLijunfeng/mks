#!/usr/bin/env python
# -*- coding: utf-8 -*-

' novnc console url '

__author__ = 'Chaoyi Zhang'

import json

import requests
from flask import Flask, request, abort, Response

import settings
from mks import console

app = Flask(__name__)


@app.route('/console', methods=['GET'])
def get_console_url():
    # get header
    token = request.headers['X-Subject-Token']
    myheaders = {
        'Content-Type': 'application/json',
        'X-Subject-Token': token
    }

    # get querystring
    ids = request.args.get('id').split(',')
    if ids is None:
        abort(400)

    urls = []
    for id in ids:
        # sent request get provider_id by instance
        resp = requests.get(settings.UCMP_URL + '/ucmp3/service_instance/ecs/' + id, headers=myheaders, verify=False)
        if resp.ok:
            resp_json = resp.json()
            provider_id = resp_json.get('provider_id')
            if provider_id is None:
                abort(400, 'cant find provider_id by instance %s' % id)

            # send request get provider by provider_id
            resp = requests.get(settings.UCMP_URL + '/iaasmgt3/provider/%s' % provider_id, headers=myheaders,
                                verify=False)
            if resp.ok:
                resp_json = resp.json()
                default_auth = resp_json.get('default_auth')
                if default_auth is None:
                    abort(400, 'cant find default_auth by provider %s' % provider_id)
                user = default_auth.get('user')
                if user is None:
                    abort(400, 'cant find user by provider %s' % provider_id)
                password = default_auth.get('password')
                if password is None:
                    abort(400, 'cant find password by provider %s' % provider_id)
                vsphere_server = default_auth.get('vsphere_server')
                if vsphere_server is None:
                    abort(400, 'cant find vsphere_server by provider %s' % provider_id)

                url = console('mks://%s:%s@%s/?uuid=%s' % (user, password, vsphere_server, id))
                urls.append(url)
            else:
                abort(401, 'token %s is invalid' % token)
        else:
            abort(401, 'token %s is invalid' % token)
    return Response(json.dumps(urls), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6070)
