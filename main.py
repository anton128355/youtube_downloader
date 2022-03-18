import flask
import youtube_dl

app = flask.Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def post_video_url(): 
    global dict_of_content
    ydl_opts = {}
    dict_of_content = dict()
    if flask.request.method == "POST":
        video_url = flask.request.form.get("video_url")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            json_data = ydl.extract_info(video_url, download=False)
        for content in json_data["formats"]:
            if content["width"] == None:
                dict_of_content.update({f"audio-{content['ext']}": content['url']})
            elif content["width"] != None:
                dict_of_content.update({f"video-{content['ext']}-{content['width']}": content['url']})
        return flask.redirect("/additional_data")
    else:
        return flask.render_template("main_page.html")

@app.route("/additional_data", methods=['GET', 'POST'])
def additional_data():
    if flask.request.method == "POST":
        return flask.redirect(dict_of_content[flask.request.form.get("list_of_contents")])
    else:
        return flask.render_template("download_data.html", dict_of_content=dict_of_content.keys())

if __name__ == "__main__":
    app.run(debug=True)
