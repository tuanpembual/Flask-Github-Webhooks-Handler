from flask import Flask, render_template, request, redirect, url_for, jsonify
#http://pymotw.com/2/hmac/
import hmac
import hashlib
#http://techarena51.com/index.php/how-to-install-python-3-and-flask-on-linux/
import subprocess

app = Flask(__name__)


def verify_hmac_hash(data, signature):
    digest_maker = hmac.new(bytes('some secret', 'UTF-8'), data, hashlib.sha1)
    digest = digest_maker.hexdigest()
    print(digest)
    return hmac.compare_digest(digest, signature)



@app.route("/payload", methods=['POST'])
def github_payload():
      if request.headers.get('X-GitHub-Event') == "ping":
        signature = request.headers.get('X-Hub-Signature')
        print(signature)
        #print(request.get_json())
        return jsonify({'msg': 'Ok'})
      if request.headers.get('X-GitHub-Event') == "push":
          signature = request.headers.get('X-Hub-Signature')
          data = request.get_json()
          verify_result = verify_hmac_hash(data, signature)
          print(verify_result)
          payload = request.get_json()
          if  payload['commits'][0]['distinct'] == True:
              cmd = subprocess.Popen(['bash','git_commands.bash'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
              out,error = cmd.communicate()
              return jsonify({'msg': 'successfully ran git pull'})

if __name__ == "__main__":
    app.debug = True
    app.run(host="23.250.18.72")
