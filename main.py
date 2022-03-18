import flask
import youtube_dl

app = flask.Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def get_info_about_video(): 
    global lst_variants_of_content, dict_variants_of_content
    ydl_opts = {}
    json_data = None
    lst_variants_of_content, dict_variants_of_content = [], dict()
    if flask.request.method == "POST":
        video_url = flask.request.form.get("video_url")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            json_data = ydl.extract_info(video_url, download=False)
    
        for content in json_data["formats"]:
            if content["width"] == None:
                lst_variants_of_content.append(f"audio-{content['ext']}")
                dict_variants_of_content.update({f"audio-{content['ext']}": content['url']})
            elif content["width"] != None:
                lst_variants_of_content.append(f"video-{content['ext']}-{content['width']}")
                dict_variants_of_content.update({f"video-{content['ext']}-{content['width']}": content['url']})
        
        return flask.redirect("/additional_data")
    else:
        return flask.render_template("main_page.html")

@app.route("/additional_data", methods=['GET', 'POST'])
def additional_data():
    if flask.request.method == "POST":
        result = flask.request.form.get("variants_of_video_and_audio")
        return flask.redirect(dict_variants_of_content[result])
    else:
        return flask.render_template("download_data.html", lst_variants_of_content=lst_variants_of_content)

if __name__ == "__main__":
    app.run(debug=True)
