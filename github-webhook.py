from flask import render_template, request, redirect, url_for, jsonify
import subprocess

app = Flask(__name__)

@app.route("/payload")
def github_payload():      
      if request.headers.get('X-GitHub-Event') == "ping":
        print(request.get_json())
        return jsonify({'msg': 'Ok'})
      if request.headers.get('X-GitHub-Event') == "push":
          payload = request.get_json()
          if  payload['commits'][0]['distinct'] == True:
              cmd = subprocess.Popen(['bash','git_commands.bash'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
              out,error = cmd.communicate()                 
              return jsonify({'msg': 'successfully ran git pull'})

if __name__ == "__main__":
    app.run()