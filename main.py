from flask import Flask, redirect
from flask_cors import CORS

from tracks import recently_played_tracks, get_tops
from util import random_key, generate_keys, is_key

app=Flask(__name__)
CORS(app, resources={r"/*/*/*": {"origins": "*"}})

keys: list[str] = generate_keys()
rk:str = random_key()

@app.route("/", methods=['GET'])
def index() -> str:
    return redirect("/key", code=302)

@app.route('/<key>/recents', methods=['GET'])
def key(key:str) -> dict:
    found: bool = is_key(key, keys)
    if found:
        return recently_played_tracks()
    return {
        "error": "invalid key was provided"
    }

@app.route('/key', methods=['GET'])
def get_key() -> dict:
      return {
            "key":rk,
            "readme":"add /<key>/recents -> get recent played"}

@app.route('/<key>/top', methods=['GET'])
def top(key: str) -> dict:
    found: bool = is_key(key, keys)
    if found:
        return get_tops()
    return {
        "error": "invalid key was provided"
    }

@app.route('/help', methods=['GET'])
def help_page() -> str:
    return '''
        <html><body>
            <div>
                <h1>App key</h1>
                <p>Store using an env file in your app root directory. Use at your own risk</p>
                <p>key: <a href="/key">use key</a></p>
                <h2>Server Directory:</h2>
                <ul>/help -> show help</ul>
                <ul>/key/client_id/client_secret -> get auth code</ul>
            </div>
        </body><html>
    '''

if __name__ == "__main__":
    app.run(port="5432", debug=True)