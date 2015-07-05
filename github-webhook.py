from flask import Flask, render_template, request, redirect, url_for, jsonify
#http://pymotw.com/2/hmac/
import hmac
import hashlib
#http://techarena51.com/index.php/how-to-install-python-3-and-flask-on-linux/
import subprocess

app = Flask(__name__)


def verify_hmac_hash(data, signature):
    github_secret = bytes('some secret', 'UTF-8');
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
          if  payload['commits'][0]['distinct'] == True:
              try:
                  subprocess.check_output(['git', 'pull', 'origin', 'master' ]
                  return jsonify({'msg': 'successfully ran git pull'})
              except subprocess.CalledProcessError:
                  error = subprocess.CalledProcessError.output
                  return jsonify({'msg': error})

    else:
        return jsonify({'msg': 'invalid hash'})


if __name__ == "__main__":
    app.debug = True
    app.run(host="23.250.18.72")
