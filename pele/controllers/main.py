import os
import json
import requests
import types
from datetime import datetime
from flask import Blueprint, render_template, flash, request, redirect, url_for, Response, current_app, jsonify
from flask_login import login_user, logout_user, login_required

from pele import cache
from pele.forms import LoginForm
from pele.models.user import User


main = Blueprint('main', __name__)


#@cache.cached(timeout=1000)
@main.route('/')
def home():
    return redirect(url_for("api_v0-1.doc"))
