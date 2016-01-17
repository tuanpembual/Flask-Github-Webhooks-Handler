from flask import Flask, render_template, request, redirect, url_for, jsonify

import hmac
import hashlib
import subprocess
import os

app = Flask(__name__)

def verify_hmac_hash(data, signature):
    github_secret = bytes('your seceret', 'UTF-8')
    mac = hmac.new(github_secret, msg=data, digestmod=hashlib.sha1)
    return hmac.compare_digest('sha1=' + mac.hexdigest(), signature)


@app.route("/payload", methods=['POST'])
def github_payload():
    signature = request.headers.get('X-Hub-Signature')
    data = request.data
    if verify_hmac_hash(data, signature):
        if request.headers.get('X-GitHub-Event') == "ping":
            return jsonify({'msg': 'Ok'})
        if request.headers.get('X-GitHub-Event') == "push":
            payload = request.get_json()
            if payload['commits'][0]['distinct'] == True:
                try:
                    cmd_output = subprocess.check_output(
                        ['git', 'pull', 'origin', 'master'],)
                    return jsonify({'msg': str(cmd_output)})
                except subprocess.CalledProcessError as error:
                    return jsonify({'msg': str(error.output)})
            else:
                return jsonify({'msg': 'nothing to commit'})

    else:
        return jsonify({'msg': 'invalid hash'})

if __name__ == "__main__":
    app.debug = True
    app.run(host="127.0.0.1", port=5001)
