import os
import requests

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import apology

import spacexpy

# spacex variable is set as global variable before flask is configured due to flask using multiple threads which breaks spacexpy
spacex = spacexpy.SpaceX()

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# URL base
BASE_URL = 'https://api.spacexdata.com/v4'

# Welcome page
@app.route("/", methods=["GET", "POST"])
def home():
    """Display welcome page"""
    if request.method == "GET":
        return render_template("welcome.html")

# Results page
@app.route("/index")
def index():
    
    # Get latest launch details
    latest_launch = spacex.launches(schedule='latest')

    # Get ships details and store in list
    # spacex.ships(ship_id=ids[i]) is an attributeDict type
    ids = latest_launch['ships']
    ship0 = spacex.ships(ship_id=ids[0])
    ship1 = spacex.ships(ship_id=ids[1])
    ship2 = spacex.ships(ship_id=ids[2])
    ship3 = spacex.ships(ship_id=ids[3])
    ship4 = spacex.ships(ship_id=ids[4])
    all_ships = [ship0, ship1, ship2, ship3, ship4]

    # Display information on index page
    return render_template("index.html", latest_launch=latest_launch, all_ships=all_ships)

if __name__ == "__main__":
    app.run(debug=True)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)