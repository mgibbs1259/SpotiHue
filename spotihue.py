#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import logging
import urllib.request

import cv2
import numpy as np
import spotipy
from phue import Bridge
from spotipy import Spotify
from sklearn.cluster import KMeans

import credentials


class SpotiHue(object):
    def __init__(self):
        self.hue_bridge = Bridge(credentials.hue_bridge_ip_address)
        self.spotify = Spotify(auth=spotipy.util.prompt_for_user_token(credentials.spotify_username,
                                                                       credentials.spotify_scope,
                                                                       credentials.spotify_client_id,
                                                                       credentials.spotify_client_secret,
                                                                       credentials.spotify_redirect_uri))

    def retrieve_current_track_information(self):
        """Returns the current track's name, artist, and album."""
        current_track = self.spotify.currently_playing()
        current_track_name = current_track["item"]["name"]
        current_track_artist = current_track["item"]["album"]["artists"][0]["name"]
        current_track_album = current_track["item"]["album"]["name"]
        return current_track_name, current_track_artist, current_track_album

    def retrieve_current_track_album_artwork(self):
        """Returns the current track's album artwork URL."""
        return self.spotify.currently_playing()["item"]["album"]["images"][1]["url"]

    def download_current_track_album_artwork(self):
        """Downloads the current track's album artwork."""
        album_artwork = self.retrieve_current_track_album_artwork()
        urllib.request.urlretrieve(album_artwork, "album_artwork.jpg")

    def resize_current_track_album_artwork(self):
        """Resizes the current track album artwork to 50% of the original size."""
        self.download_current_track_album_artwork()
        album_artwork = cv2.imread("album_artwork.jpg")
        album_artwork = cv2.cvtColor(album_artwork, cv2.COLOR_BGR2RGB)
        dimensions = (int(album_artwork.shape[1] * 50 / 100), int(album_artwork.shape[0] * 50 / 100))
        return cv2.resize(album_artwork, dimensions, interpolation=cv2.INTER_AREA)

    def convert_current_track_album_artwork_to_2D_array(self):
        """Converts the current track album artwork from a 3D to a 2D array."""
        album_artwork_array = self.resize_current_track_album_artwork()
        return album_artwork_array.reshape(album_artwork_array.shape[0] * album_artwork_array.shape[1], 3)

    def obtain_kmeans_clusters(self):
        """Returns the cluster centers obtained by fitting K-Means with 3 clusters."""
        album_artwork_array = self.convert_current_track_album_artwork_to_2D_array()
        kmeans = KMeans(n_clusters=3, random_state=1259)
        kmeans.fit(album_artwork_array)
        return kmeans.cluster_centers_

    def check_black_clusters(self):
        """Returns the RGB values for white if the RGB values of a cluster are black."""
        clusters = []
        for cluster in self.obtain_kmeans_clusters():
            if np.all(cluster == 0):
                cluster = np.array([255, 255, 255])
            clusters.append(cluster)
        return clusters

    def standardize_rgb_values(self, cluster):
        """Returns the standardized RGB values between 0 and 1."""
        R, G, B = (cluster / 255).T
        return R, G, B

    def apply_gamma_correction(self, cluster):
        """Returns RGB values after a gamma correction has been applied."""
        R, G, B = self.standardize_rgb_values(cluster)
        R = [((R + 0.055) / (1.0 + 0.055)) ** 2.4 if R > 0.04045 else R / 12.92][0]
        G = [((G + 0.055) / (1.0 + 0.055)) ** 2.4 if G > 0.04045 else G / 12.92][0]
        B = [((B + 0.055) / (1.0 + 0.055)) ** 2.4 if B > 0.04045 else B / 12.92][0]
        return R, G, B

    def convert_rgb_to_xyz(self, cluster):
        """Returns XYZ values after a RGB to XYZ conversion using the Wide RGB D65
        conversion formula has been applied."""
        R, G, B = self.apply_gamma_correction(cluster)
        X = R * 0.649926 + G * 0.103455 + B * 0.197109
        Y = R * 0.234327 + G * 0.743075 + B * 0.022598
        Z = R * 0.0000000 + G * 0.053077 + B * 1.035763
        return X, Y, Z

    def convert_xyz_to_xy(self):
        """Returns xy values in the CIE 1931 colorspace after a XYZ to xy conversion has been applied."""
        # Only using one cluster for now
        cluster = self.check_black_clusters()[0]
        X, Y, Z = self.convert_rgb_to_xyz(cluster)
        x = round(X / (X + Y + Z), 4)
        y = round(Y / (X + Y + Z), 4)
        return x, y

    def connect_hue_bridge_first_time(self):
        """Connects to the Hue Bridge for the first time. Ensure Hue Bridge button is pressed."""
        self.hue_bridge.connect()

    def turn_lights_on(self):
        """Turns all of the lights on to half brightness."""
        logging.info("Turning the lights on to half brightness")
        for light in self.hue_bridge.lights:
            light.on = True
            light.brightness = 127

    def change_light_color_album_artwork(self):
        """Change all of the lights to one of the prominent colors in the current track's album artwork."""
        track, artist, album = self.retrieve_current_track_information()
        logging.info(f"Changing the color of the lights based on the current track: {track}, {artist}, {album}")
        x, y = self.convert_xyz_to_xy()
        for light in self.hue_bridge.lights:
            light.xy = [x, y]

    def change_light_color_normal(self):
        """Change all of the lights to normal."""
        logging.info(f"Changing the color of the lights to normal")
        for light in self.hue_bridge.lights:
            light.hue = 10000
            light.saturation = 120

    def determine_track_playing_status(self):
        """Returns a boolean indicating if Spotify is still playing a track or not.
        Changes the lights back to normal if Spotify is not playing."""
        try:
            track_playing_status = self.spotify.currently_playing()["is_playing"]
            if track_playing_status:
                logging.info("Spotify is still playing")
            else:
                logging.info("Spotify stopped playing")
                self.change_light_color_normal()
            return track_playing_status
        except:
            logging.info("Spotify stopped playing")
            self.change_light_color_normal()

    def sync_current_track_album_artwork_lights(self):
        """Syncs the current track's album artwork colors with the lights."""
        self.turn_lights_on()
        while self.determine_track_playing_status():
            self.change_light_color_album_artwork()
            time.sleep(5.3)
