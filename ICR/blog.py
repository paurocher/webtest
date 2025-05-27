from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask.wrappers import Response
from sqlite3 import Connection

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


# associate the URL /index with the index view function
@bp.route("/")
def index() -> str:
    """Shows all the posts currently in the database.

    Returns:
        str: The rendered HTML template with all the posts.
    """
    db: Connection = get_db()

    # get all post ids
    post_ids: list = db.execute(
        "SELECT id FROM posts ORDER BY datetime DESC"
    ).fetchall()
    post_ids: list = [post_id["id"] for post_id in post_ids]

    # get all related data from each post
    complete_posts: list = get_complete_posts(post_ids)
    return render_template("blog/index.html", posts=complete_posts)


# associate the URL /create with the create view function
@bp.route("/create", methods=("GET", "POST"))
# Trigger the login_required decorator so the create page is returned only if
# the user is logged in.
@login_required
def create() -> str or Response:
    """Create new post.

    Returns:
        str or Response: rendered template
    """
    # is the user on a mobile device?
    mobile: bool = is_mobile()

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

        # get tags
        tags: list = request.form["tags"].split(",")
        tags: list = [tag for tag in tags if tag]

        # Build a tidy dictionary with all the data ready for the DB
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


# associate the URL /edit with the edit view function
@bp.route("/edit/<int:post_id>", methods=("GET", "POST"))
# Trigger the login_required decorator so the create page is returned only if
# the user is logged in.
@login_required
def edit(post_id: int) -> str or Response:
    """Edit a post.

    Args:
        post_id (int): post id to edit
    """
    # is the user on a mobile device?
    mobile: bool = is_mobile()
    print(f"{mobile=}")

    post: dict = get_complete_posts([post_id])[0]
    # quckly generating a list of tuples to pair thumbs and pictures and
    # adding them to the post, so I can pass them to the switches and easily
    # find both paths to delete
    post["images"] = [
        (img, thmb) for img, thmb in zip(post["images"], post["thumbs"])
    ]

    if request.method == "GET":
        # get the edit page filled in with the post data
        return render_template("blog/edit.html", post=post, mobile=mobile)

    # POST (Submit, Cancel, Delete)
    action: str = request.form.get("action")
    # delete post from DB
    if action == "Delete":
        delete_post(post)
        return redirect(url_for("blog.index"))

    elif action == "Submit":
        # update post
        update: bool = update_post(post, request)
        if not update:
            # something went wrong, return to post edit
            return render_template("blog/edit.html", post=post, mobile=mobile)

    # all good, post got updated, go to index
    return redirect(url_for("blog.index"))


# associate the URL /carousel with the carousel view function
@bp.route("/carousel/<int:post_id>")
def carousel(post_id: int) -> str:
    """Render the carousel view for a specific post.

    Args:
        post_id (int): The ID of the post to display.

    Returns:
        str: The rendered carousel view as a string.
    """
    # get the current post complete dict

    post: dict = get_complete_posts([post_id])[0]

    # place to store the images of the post
    images: dict = {}

    # One of the carousel images must have the "active" class, so the carousel
    # starts up showing an image. This class is only added to the first image.
    active: str = "active"
    for i, image in enumerate(post["images"]):
        if i > 0:
            active = ""
        images[i] = [f"/static/{image}", active]
    return (
        render_template(
            "blog/full_screen_carousel.html",
            images=images
        )
    )
