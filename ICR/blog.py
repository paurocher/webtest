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
from flask.wrappers import Response
import os
from pprint import pprint as pp
from user_agents import parse
from werkzeug.user_agent import UserAgent
from werkzeug.utils import secure_filename

from ICR.__app import app
from ICR.auth import login_required
from ICR.db import get_db
from ICR.helpers.sql_functions import insert, get_complete_posts, get_post
from ICR.helpers.image_process import image_process

bp = Blueprint("blog", __name__)

@bp.route("/")
def index():
    db = get_db()

    # get all entries in the posts table
    # posts = db.execute(
    #     "SELECT p.id pid, p.title, p.message, p.datetime, u.id uid, u.name "
    #     "FROM posts p "
    #     "JOIN users u ON p.user_id = u.id "
    #     "ORDER BY datetime DESC"
    # ).fetchall()
    post_ids = db.execute(
        "SELECT id FROM posts ORDER BY datetime DESC"
    ).fetchall()

    post_ids = [post_id["id"] for post_id in post_ids]
    print(post_ids)

    # get all related data from ech post
    complete_posts = get_complete_posts(post_ids)
    print("f")
    return render_template("blog/index.html", posts=complete_posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create() -> str or Response:
    # get device
    user_agent: str = request.headers.get("User-Agent")
    user_agent_parsed: UserAgent = parse(user_agent)
    device_type: str = (
        "Mobile" if user_agent_parsed.is_mobile else
        "Tablet" if user_agent_parsed.is_tablet else
        "Desktop"
    )
    mobile: bool = True
    if device_type == "Desktop":
        mobile = False

    if request.method == "POST":
        title: str = request.form["title"]
        body: str = request.form["message"]

        # check that required fields are not empty
        error: str or None = None
        if not title:
            error = "Title is required."
        if not body:
            error = "Message is required."
        if error is not None:
            flash(error)
            return render_template("blog/create.html", mobile=mobile)

        # get and process images
        images: list or None = None
        if "files" in request.files:
            images = image_process(
                [
                    request.files.getlist("files"),
                    request.files.getlist("cam_files")
                ]
            )

        # get locations, filter out empty strings
        fn_locations: list = request.form["fn_location"].split(",")
        fn_locations: list = [loc for loc in fn_locations if loc]
        nfn_locations: list = request.form["nfn_location"].split(",")
        nfn_locations: list = [loc for loc in nfn_locations if loc]
        locations: dict = {"fn": fn_locations, "nfn": nfn_locations}
        # print(f"{locations=}")

        # get tags
        tags: list = request.form["tags"].split(",")

        post_data: dict = {
            "title": title,
            "body": body,
            "images": images,
            "locations": locations,
            "tags": tags
        }
        insert(post_data)

        return redirect(url_for("blog.index"))

    return render_template("blog/create.html", mobile=mobile)



@bp.route("/<int:post_id>/edit", methods=("GET", "POST"))
@login_required
def edit(post_id):
    db = get_db()
    # post = get_post(post_id)

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
                "UPDATE posts SET title = ?, message = ? "
                "WHERE id = ?",
                (title, body, post_id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    # get all entries in the posts table
    post_id = db.execute(
        "SELECT id FROM posts ORDER BY datetime DESC"
    ).fetchone()

    print("POST")
    print(f"{post_id=}")

    post = get_complete_posts(post_id)[0]
    return render_template("blog/edit.html", post=post)

# TODO: add image upload
# TODO: add tag add
# TODO: add tag remove
# TODO: location tag add
# TODO: location tag remove


@bp.route("/<int:post_id>/delete", methods=("POST",))
@login_required
def delete(post_id):
    # TODO: add image deletion
    get_post(post_id)
    db = get_db()
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
    return redirect(url_for("blog.index"))






