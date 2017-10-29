from flask import Flask, render_template, json, request

import song_manager

application = Flask(__name__)


@application.route('/')
def index():
    return render_template('configuration.html')


@application.route('/get-songs')
def get_songs_list():
    songs = song_manager.get_all_songs()
    return json.dumps(songs)


@application.route('/song/<id>', methods=['DELETE'])
def delete_song(id):
    song_manager.delete_a_song(id)
    return '', 204


@application.route('/song', methods=['POST'])
def insert_song():
    song_manager.insert_new_song(request.get_json())
    return '', 201


def run():
    application.run(host="0.0.0.0")


if __name__ == "__main__":
    run()
