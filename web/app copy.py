import os
import logging
import platform

from pathlib import Path
from flask import Flask, Blueprint, render_template, send_from_directory, jsonify
from utils.discordbot import Bot
from web.routes.api import api
from web.routes.pages import pages

app = Flask( __name__, template_folder="templates", static_folder="static" )
bot_instance: Bot = None

def register():
    api.bot_instance = bot_instance
    pages.bot_instance = bot_instance
    
    # Register them blueprints.
    app.register_blueprint(api)
    app.register_blueprint(pages)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# no loggie
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/")
def home():
    # return "am alive!!\n..maybe-"
    
    return send_from_directory("", "index.html")
    # return render_template('index.php')

@app.route("/<path:filename>")
def file(filename: str):
    # page_path = os.path.abspath(f"web/{filename}")

    # if filename.startswith("/content"):
    #     return send_from_directory("", filename)
    
    # if os.path.exists(f"{page_path}.php") or os.path.exists(f"{page_path}.html"):
    #     fileext = "php"
    #     if page_path.endswith("html"):
    #         fileext = "html"

    #     return render_template(f'{filename}.{fileext}')
    return send_from_directory("", filename)

def run():
    # print(platform.system())
    port = os.environ.get("SERVER_PORT", 5000)
    
    app.run(debug=False, host="0.0.0.0", port=port)