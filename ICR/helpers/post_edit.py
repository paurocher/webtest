"""Functions related to data editing and deletion."""
from flask import flash, Request, current_app
import os.path
from pathlib import Path
from sqlite3 import Connection, Cursor

from ICR.db import get_db
from .image_process import image_process


def delete_post(post: dict) -> None:
    """Delete a post and all its dependencies.

    Args:
        post(dict): a complete post
    """
    db: Connection = get_db()

    # delete post
    db.execute("DELETE FROM posts WHERE id = ?", (post["id"],))
    db.commit()

    # delete images and thumbs
    delete_images(post)

    # locations (fn, nfn)
    delete_locations(post)

    # tags
    delete_tags(post)


def delete_images(post: dict) -> None:
    """Deletes all images associated with a post and its relationships.

    Args:
        post(dict): a complete post"""
    db: Connection = get_db()
    images = [img for  sublist in post["images"] for img in sublist]

    db.execute(
        "DELETE FROM pictures WHERE post_id = ?", (post["id"],)
    )
    db.commit()

    root_path = os.path.join(
        current_app.config["ROOT_PATH"],
        "ICR",
        "static",
    )
    for image in images:
        img_path: str = os.path.sep.join(image.split(os.path.sep)[1:])
        img_path: str = os.path.join(root_path, img_path)
        os.remove(img_path)


def delete_locations(post: dict) -> None:
    """Deletes all locations associated with a post and its relationships.

    Will only delete locations if they are not used by any other post.

    Args:
        post(dict): a complete post"""
    db: Connection = get_db()

    nations: dict = {
        "posts_fn_locations": "fn_locations",
        "posts_nfn_locations": "nfn_locations"
    }
    for relationship, locations in nations.items():
        # 1. figure out if any of the locations related to this post is related
        #    to other posts
        # Get each location id only referred by this post. As they are not
        # referred by other posts, we can safely delete these locations
        sql_select_command: str = (
            f"SELECT * FROM {relationship} WHERE location_id IN "
            f"(SELECT location_id FROM {relationship} WHERE post_id = ?) "
            "GROUP BY location_id "
            "HAVING COUNT (location_id) = 1"
        )
        delete_locs: list = db.execute(sql_select_command, (post["id"],
        )).fetchall()
        delete_locs: list = [loc["location_id"] for loc in delete_locs]

        # 2. delete any location that relates only to this post, not other posts
        if delete_locs:
            sql_del_command: str = (
                f"DELETE FROM {locations} WHERE id IN "
                f"({', '.join(['?']*len(delete_locs))})"
            )
            db.execute(sql_del_command, (delete_locs))
            db.commit()

        # 3. delete relationship
        sql_del_command: str = (
            f"DELETE FROM {relationship} WHERE post_id = ?"
        )
        db.execute(sql_del_command, (post["id"],))
        db.commit()


def delete_tags(post: dict) -> None:
    """Deletes all tags associated with a post and its relationships.

    Will only delete tags if they are not used by any other post.

    Args:
        post(dict): a complete post"""
    db: Connection = get_db()

    # same workflow as in the locations. I know, putting the same comments is
    # redundant, but it helps me keep track ...

    # 1. figure out if any of the tags related to this post is related
    #    to other posts
    # Get each tag id only referred by this post. As they are not
    # referred by other posts, we can safely delete these tags.
    sql_select_command: str = (
        f"SELECT * FROM posts_tags WHERE tag_id IN "
        f"(SELECT tag_id FROM posts_tags WHERE post_id = ?) "
        "GROUP BY tag_id "
        "HAVING COUNT (tag_id) = 1"
    )
    _delete_tags: list = db.execute(
        sql_select_command, (post["id"],)
    ).fetchall()
    _delete_tags: list = [tag["tag_id"] for tag in _delete_tags]

    # 2.
    if _delete_tags:
        sql_del_command: str = (
            f"DELETE FROM tags WHERE id IN "
            f"({', '.join(['?'] * len(_delete_tags))})"
        )
        db.execute(sql_del_command, (_delete_tags))
        db.commit()

    # 3. delete relationship
    sql_del_command: str = (
        f"DELETE FROM posts_tags WHERE post_id = ?"
    )
    db.execute(sql_del_command, (post["id"],))
    db.commit()


def update_post(post: dict, request: Request) -> bool:
    """Update a post and its dependencies.

    Args:
        post(dict): a complete post
        request(Request): the request object

    Returns:
        bool: True if the post was updated or left unchanged, False otherwise
    """
    # title
    title: bool = update_title(post, request)
    if not title:
        return False

    # message
    message: bool = update_message(post, request)
    if not message:
        return False

    # images and thumbs
    update_images(post, request)

    # locations
    update_locations(post, request)

    # tags
    update_tags(post, request)

    return True


def update_title(post: dict, request: Request) -> bool:
    """Update the title of a post.

    Args:
        post(dict): a complete post
        request(Request): the request object
    Returns:
        bool: True if the title was updated or left unchanged, False otherwise
    """
    title: str = request.form["title"]

    if not title:
        flash("Title is required.")
        return False

    # compare title from request (new) and from post (old)
    if title == post["title"]:
        # returning true means nothing happens and the other functions
        # are triggered
        return True

    # title has changed, let's update it
    db: Connection = get_db()
    db.execute("UPDATE posts SET title = ? WHERE id = ?", (title, post["id"]))
    db.commit()
    return True


def update_message(post: dict, request: Request) -> bool:
    """Update the message of a post.

    Args:
        post(dict): a complete post
        request(Request): the request object
    Returns:
        bool: True if the message was updated or left unchanged, False otherwise
    """
    message: str = request.form["message"]

    if not message:
        flash("Message is required.")
        return False

    if message == post["message"]:
        # message did not change
        return True

    # message has changed, let's update it
    db: Connection = get_db()
    db.execute(
        "UPDATE posts SET message = ? WHERE id = ?", (message, post["id"])
    )
    db.commit()
    return True


def update_images(post: dict, request: Request) -> None:
    """Update the images of a post.

    Args:
        post(dict): a complete post
        request (Request): the request object
        """

    # get the switches for the existing images
    checkboxes: dict = {
        k: v for k, v in request.form.items() if "checkbox" in k
    }

    root_path = os.path.join(
        current_app.config["ROOT_PATH"],
        "ICR",
        "static",
    )

    db: Connection = get_db()
    for checkbox, paths in checkboxes.items():
        paths: list = eval(paths)
        # delete paths
        for path in paths:
            path: str = os.path.sep.join([root_path, path])
            path: Path = Path(path)
            path.unlink()

        # delete the image relationship
        db.execute("DELETE FROM pictures WHERE path = ?", (paths[0],))
    db.commit()


    # get the new images
    images: list = image_process(
        [
            request.files.getlist("files"),
            request.files.getlist("cam_files")
        ]
    )
    # create the image relationship
    # 1. get latest image order number
    latest = db.execute("SELECT MAX(picture_order) FROM pictures "
               "WHERE post_id = ?", (post["id"],))
    order: int = latest.fetchone()[0]

    for i, image_group in enumerate(images):
        if order:
            order += 1
        else:
            order = 1
        img_path = image_group[0]
        thmb_path = image_group[1]
        db.execute(
            "INSERT INTO pictures (post_id, picture_order, path, thumb) "
            "VALUES (?, ?, ?, ?)",
            (post["id"], order, img_path, thmb_path)
        )
    db.commit()

def update_locations(post: dict, request: Request) -> bool or None:
    """Update the locations of a post.

    Args:
        post(dict): a complete post
        request(Request): the request object
    Returns:
        bool: True if locations were updated or left unchanged, False otherwise
    """
    # fn locations
    fn_locations: list = request.form["fn_locations"].split(",")
    fn_locations: list = [loc for loc in fn_locations if loc]
    # nfn locations
    nfn_locations: list = request.form["nfn_locations"].split(",")
    nfn_locations: list = [loc for loc in nfn_locations if loc]

    locations: dict = {
        "fn_locations": fn_locations,
        "nfn_locations": nfn_locations
    }

    if (locations["fn_locations"] == post["locations"]["fn"] and
        locations["nfn_locations"] == post["locations"]["nfn"]):
        # locations did not change
        return True

    # removed locations
    deleted_locations: dict = {
        "fn_locations": [
            loc for loc in post["locations"]["fn"] if loc not in fn_locations
        ],
        "nfn_locations": [
            loc for loc in post["locations"]["nfn"] if loc not in nfn_locations
        ]
    }

    # search if any other post has this tag assigned. If so, only delete
    # relationship, otherwise delete relationship and tag
    db: Connection = get_db()
    for nation, locs in deleted_locations.items():
        for loc in locs:
            # get location id
            location_id: int = db.execute(
                f"SELECT id FROM {nation} WHERE toponym = ?", (loc,)
            ).fetchone()["id"]
            # check if this location is only assigned to one post (which would
            # be this post we are dealing with)
            location_rels: list = db.execute(
                f"SELECT post_id FROM posts_{nation} WHERE location_id = "
                f"(SELECT id FROM {nation} WHERE toponym = ?) "
                "GROUP by location_id "
                "HAVING COUNT (location_id) = 1",
                (loc,)
            ).fetchall()
            location_rels = [post["post_id"] for post in location_rels if loc]

            if location_rels:
                # delete locaion as it is used only by this post
                db.execute(f"DELETE FROM {nation} WHERE toponym = ?", (loc,))
            # delete relationship
            db.execute(
                f"DELETE FROM posts_{nation} WHERE post_id = ? AND "
                f"location_id = ?", (post["id"], location_id)
            )
            db.commit()

    # added locations
    new_fn_locs: list = [
        loc for loc in locations["fn_locations"] if loc not in
        post["locations"]["fn"]
    ]
    new_nfn_locs: list = [
        loc for loc in locations["nfn_locations"] if loc not in
        post ["locations"]["nfn"]
    ]
    new_locations: dict = {
        "fn_locations": new_fn_locs,
        "nfn_locations": new_nfn_locs
    }
    for nation, locations in new_locations.items():
        for loc in locations:
            # figure out if this tag already exists
            duplicate: dict = db.execute(
                f"SELECT id FROM {nation} WHERE toponym = ?", (loc,)
            ).fetchone()
            if duplicate:
                # if it does exits, lets grab its id and assign it to this var
                new_loc_id: int = duplicate["id"]
            else:
                # if it doesn't exist, let's add it to the db
                new_loc_id: Cursor = db.execute(
                    f"INSERT INTO {nation} (toponym) VALUES (?)", (loc,)
                )
                new_loc_id: int = new_loc_id.lastrowid

            # create relationship of this new location and the post we are
            # editing
            db.execute(
                f"INSERT INTO posts_{nation} (post_id, location_id) VALUES ("
                f"?, ?)", (post["id"], new_loc_id)
            )
        db.commit()

def update_tags(post: dict, request: Request) -> bool:
    """Update the tags of a post.

    Args:
        post(dict): a complete post
        request(Request): the request object
    Returns:
        bool: True if tags were updated or left unchanged, False otherwise
    """
    # get tags from the form
    tags: list = request.form["tags"].split(",")
    tags: list = [tag for tag in tags if tag]

    # tags didn't change, return True so we go to index page
    if tags == post["tags"]:
        return True

    # removed tags
    deleted_tags: list = [tag for tag in post["tags"] if tag not in tags]
    # search if any other post has this tag assigned. If so, only delete
    # relationship, otherwise delete relationship and tag
    db: Connection = get_db()
    for tag in deleted_tags:
        # get tag id
        tag_id: int = db.execute(
            "SELECT id FROM tags WHERE tag = ?", (tag,)
        ).fetchone()["id"]
        # check if this tag is only assigned to one post (which would be this
        # post we are dealing with)
        tag_rels: list = db.execute(
            "SELECT post_id FROM posts_tags WHERE tag_id = "
            "(SELECT id FROM tags WHERE tag = ?) "
            "GROUP BY tag_id "
            "HAVING COUNT (tag_id) = 1"
            , (tag,)
        ).fetchall()
        tag_rels: list = [post["post_id"] for post in tag_rels if tag]

        if tag_rels:
            # delete tag, beause it is not used by any other post
            db.execute("DELETE FROM tags WHERE tag = ?", (tag,))
            db.commit()
        # delete relationship
        db.execute(
            "DELETE FROM posts_tags WHERE post_id = ? AND tag_id = ?",
            (post["id"], tag_id)
        )
        db.commit()

    # added tags
    new_tags: list = [tag for tag in tags if tag not in post["tags"]]
    for tag in new_tags:
        # figure out if this tag already exists
        duplicate: dict = db.execute(
            "SELECT id FROM tags WHERE tag = ?", (tag,)
        ).fetchone()
        if duplicate:
            # if it does exist, let's grab its id and assign it to this var
            new_tag_id = duplicate["id"]
        else:
            # if it doesn't exist, let's add it to the database
            new_tag_id: Cursor = db.execute(
                "INSERT INTO tags (tag) VALUES (?)", (tag,)
            )
            new_tag_id: int = new_tag_id.lastrowid
            # db.execute(
            #     "INSERT INTO posts_tags (post_id, tag_id) VALUES (?, ?)",
            #     (post["id"], new_tag_id))

        # create relationship of this new tag and the post we are editing
        db.execute(
            "INSERT INTO posts_tags (post_id, tag_id) VALUES (?, ?)",
            (post["id"], new_tag_id)
        )
    db.commit()

    # return true to go back to the index page
    return True
