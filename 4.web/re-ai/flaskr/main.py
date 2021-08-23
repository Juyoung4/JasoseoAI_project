# main.py => home 부분

from flask import Flask, jsonify, Blueprint, render_template, redirect, url_for, session

bp = Blueprint("main", __name__, url_prefix="/")

@bp.route("/")
def main():
    username = session.get('username', None)
    return render_template('index.html', username = username)