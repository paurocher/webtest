from flask import (
    Blueprint,
    flash,
    Flask,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
import os
from pprint import pprint as pp
from user_agents import parse
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from ICR.__app import app
from ICR.auth import login_required
from ICR.db import get_db
from ICR.helpers.misc import validate_file_type
from ICR.helpers.image_process import image_process

bp = Blueprint("blog", __name__)

@bp.route("/")
def index():
    # posts = db.execute(
    #     "SELECT p.id pid, p.title, p.message, p.datetime, u.id uid, u.name "
    #     "FROM posts p "
    #     "JOIN users u ON p.user_id = u.id "
    #     "ORDER BY datetime DESC"
    # ).fetchall()

    db = get_db()

    complete_posts = {}

    posts = db.execute(
        "SELECT p.id pid, p.title, p.message, p.datetime, u.id uid, u.name "
        "FROM posts p "
        "JOIN users u ON p.user_id = u.id "
        "ORDER BY datetime DESC"
    ).fetchall()

    for post in posts:
        keys = post.keys()
        container = {}
        for key in keys:
            container[key] = post[key]

            picts = db.execute(
                "SELECT path, thumb FROM pictures WHERE post_id = ?",
                (post["pid"],)
            ).fetchall()
            container["picts"] = [pict["path"] for pict in picts]
            container["thumb"] = [pict["thumb"] for pict in picts]

            locations = db.execute(
                "SELECT * from locations where "
                "id IN "
                "(SELECT location_id FROM posts_locations WHERE post_id = ? )",
                (post["pid"],)
            ).fetchall()
            container["locations"] = {"fnn": [], "nfnn": []}
            container["locations"]["fnn"] = [
                location["first_nation_name"] for location in locations
            ]
            container["locations"]["nfnn"] = [
                location["non_first_nation_name"] for location in locations
            ]
        print(container["locations"])
        for loc in container["locations"]["fnn"]:
            print(loc, type(loc))

        complete_posts[post["pid"]] = container
        # TODO: pass in full picts (for carousel) and thumbnails (for blog)
    # pp(complete_posts)
    return render_template("blog/index.html", posts=complete_posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    # get device
    user_agent = request.headers.get("User-Agent")
    user_agent_parsed = parse(user_agent)
    device_type = ("Mobile" if user_agent_parsed.is_mobile else
                   "Tablet" if user_agent_parsed.is_tablet else
                   "Desktop")
    mobile = True
    if device_type == "Desktop":
        mobile = False

    if request.method == "POST":
        # process images
        images = None
        if "files" in request.files:
            images = image_process(
                [
                    request.files.getlist("files"),
                    request.files.getlist("cam_files")
                ]
            )

        title = request.form["title"]
        body = request.form["message"]

        # check that required fields are not empty
        error = None
        if not title:
            error = "Title is required."
        if not body:
            error = "Message is required."
        if error is not None:
            flash(error)
            return render_template("blog/create.html", mobile=mobile)

        db = get_db()
        cursor = db.execute(
            "INSERT INTO posts (title, message, user_id) "
            "VALUES (?, ?, ?)",
            (title, body, g.user["id"])
        )
        db.commit()
        last_post = cursor.lastrowid

        if images:
            # print(images)
            db = get_db()
            for i, image in enumerate(images):
                # print(image)
                db.execute(
                    "INSERT INTO pictures (post_id, picture_order, path, "
                    "thumb) "
                    "VALUES (?, ?, ?, ?)",
                    (last_post, i + 1, image[0], image[1])
                )
                db.commit()

        return redirect(url_for("blog.index"))

    return render_template("blog/create.html", mobile=mobile)


def get_post(id, check_author=True):
    post = get_db().execute(
        "SELECT p.id, title, message, datetime, user_id, name"
        " FROM posts p JOIN users u ON p.user_id = u.id"
        " WHERE p.id = ?",
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["user_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["message"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE posts SET title = ?, message = ?"
                " WHERE id = ?",
                (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/edit.html", post=post)

# TODO: add image upload
# TODO: add tag add
# TODO: add tag remove
# TODO: location tag add
# TODO: location tag remove


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    # TODO: add image deletion
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM posts WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))






