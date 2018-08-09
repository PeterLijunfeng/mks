#!/usr/bin/env python
# -*- coding: utf-8 -*-

' novnc console url '

__author__ = 'Chaoyi Zhang'

from flask import Flask, request, abort

from mks import console

app = Flask(__name__)


@app.route('/console', methods=['GET'])
def get_console_url():
    id = request.args.get('id')
    if id is None:
        abort(400)
    return console('mks://root:1qaz@WSX@192.168.16.32/?name=vmware-3')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
