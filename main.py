# flask imports
from flask import (
    Flask,
    redirect,
    url_for,
    request,
    render_template as render)

# custom imports
from .blueprint import bp
from .models import db, Url

import uuid


@bp.route("/", methods=["GET", "POST"])
def home():
    unique_id = ""

    if request.method == "POST":
        data = request.form.get("url")

        # get all urls in database
        queryset = db.session.execute(db.select(Url)).scalars()

        exists = any([url.old_url == data for url in queryset])
        
        # checks if raw url already exists
        if exists:
            queryset = db.session.execute(db.select(Url)).scalars()
            for url in queryset:
                if url.old_url == data:
                    unique_id = url.new_url
                    break

        else:
            unique_id = str(uuid.uuid4())[:5]
            url = Url(
                    old_url=data,
                    new_url=unique_id
                )
            db.session.add(url)
            db.session.commit()
            
        return render("index.html", url=unique_id)
    return render("index.html")


@bp.route("/<string:unique_id>/", methods=["GET"])
def view_page(unique_id):
    """ Redirect user to original page """
    url = db.get_or_404(Url, unique_id)
    return redirect(url.old_url)

