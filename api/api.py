#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import celery
from celery import Celery
from flask import Flask, session, request
from flask_cors import CORS, cross_origin

import api.config
from api.spotihue import SpotiHue


app = Flask(__name__)
cors = CORS(app)

app.config.from_object("api.config.DevConfig")
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

@celery.task()
def run_spotihue():
    return SpotiHue().sync_current_track_album_artwork_lights()

@app.route("/", methods=["GET"])
@cross_origin()
def spotihue_welcome():
    return "Welcome to SpotiHue!"

@app.route("/connect", methods=["POST"])
@cross_origin()
def spotihue_connect():
    if request.method == "POST":
        try:
            SpotiHue().connect_hue_bridge_first_time()
            return {"connection_status": "true"}
        except:
            return {"connection_status": "false"}

@app.route("/start", methods=["POST"])
@cross_origin()
def spotihue_play():
    if request.method == "POST":
        task_id = run_spotihue.delay()
        session["task_id"] = str(task_id)
        return {"control_status": "SpotiHue is playing"}

@app.route("/stop", methods=["POST"])
@cross_origin()
def spotihue_stop():
    if request.method == "POST":
        SpotiHue().change_light_color_normal()
        celery.control.revoke(session["task_id"], terminate=True)
        return {"control_status": "SpotiHue is stopped"}

if __name__== "__main__":
    app.run()
