from flask import render_template, request

from tibetan_lookup import app

from tibetan_lookup import tibetan

@app.after_request
def add_header(r):    
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Expires"] = "0"
    r.headers["Pragma"] = "no-cache"

    return r

@app.route('/dictionary_lookup', methods=['GET','POST'])
def dictionary_lookup():

    from .models.dictionary_lookup import dictionary_lookup

    return dictionary_lookup(request)
