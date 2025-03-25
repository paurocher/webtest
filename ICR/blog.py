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
from sqlite3 import Connection, Cursor
from user_agents import parse
from werkzeug.user_agent import UserAgent
from werkzeug.utils import secure_filename

# from ICR.__app import app
from ICR.auth import login_required
from ICR.db import get_db
from ICR.helpers.sql_functions import insert, get_complete_posts
from ICR.helpers.image_process import image_process
from ICR.helpers.post_edit import (
    delete_post,
    update_post
)
from ICR.helpers.misc import is_mobile

bp = Blueprint("blog", __name__)

@bp.route("/")
def index() -> str:
    db: Connection = get_db()

    post_ids: list = db.execute(
        "SELECT id FROM posts ORDER BY datetime DESC"
    ).fetchall()

    post_ids: list = [post_id["id"] for post_id in post_ids]

    # get all related data from each post
    complete_posts: list = get_complete_posts(post_ids)
    return render_template("blog/index.html", posts=complete_posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create() -> str or Response:
    # get device
    # user_agent: str = request.headers.get("User-Agent")
    # user_agent_parsed: UserAgent = parse(user_agent)
    # device_type: str = (
    #     "Mobile" if user_agent_parsed.is_mobile else
    #     "Tablet" if user_agent_parsed.is_tablet else
    #     "Desktop"
    # )
    # mobile: bool = True
    # if device_type == "Desktop":
    #     mobile = False
    mobile = is_mobile()


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
        tags: list = [tag for tag in tags if tag]

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


@bp.route("/edit/<int:post_id>", methods=("GET", "POST"))
@login_required
def edit(post_id):
    post = get_complete_posts([post_id])[0]
    # quckly generating a list of tuples to pair thumbs and pictures so I can
    # pass them to the switches and easily find both paths to delete
    post["images"] = [
        (img, thmb) for img, thmb in zip(post["images"], post["thumbs"])
    ]

    if request.method == "GET":
        # get the post and dependencies
        return render_template("blog/edit.html", post=post)

    # POST
    pp(request.form)
    # delete post
    if request.form.get("action") == "Delete":
        delete_post(post)
        return redirect(url_for("blog.index"))

    # update post
    update = update_post(post, request)
    if not update:
        # something went wrong, return to post edit
        return render_template("blog/edit.html", post=post)

    # all good, go to index with updated post
    return redirect(url_for("blog.index"))


@bp.route("/carousel/<int:post_id>")
def carousel(post_id):
    post = get_complete_posts([post_id])[0]
    print("post")
    pp(post)
    images = {}
    active = "active"
    for i, image in enumerate(post["images"]):
        if i > 0:
            active = ""
        images[i] = [f"/static/{image}", active]
    return (
        render_template("blog/full_screen_carousel.html",
        images=images)
    )