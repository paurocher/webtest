"""All functions related to communicating with the database."""

from flask import g
from sqlite3 import Connection, Cursor, Row
from werkzeug.exceptions import abort

from ICR.db import get_db


def get_complete_posts(ids: list) -> list:
    """Get all post and dependencies.

    Build a dict with all the data from the post itself and all its
    relationships.

    Args:
        ids (list): a list of post ids

    Returns:
        list
    """
    complete_posts: list = []

    db: Connection = get_db()
    for post_id in ids:
        container: dict = {}

        # add the already existing keys in the post
        post: dict = get_post(post_id, False)
        for key in post.keys():
            container[key] = post[key]

        # add images
        picts: list = db.execute(
            "SELECT path, thumb FROM pictures WHERE post_id = ?",
            (post_id,)
        ).fetchall()
        container["images"]: list = [pict["path"] for pict in picts]
        container["thumbs"]: list = [pict["thumb"] for pict in picts]

        # add locations
        fn_locations: list = db.execute(
            "SELECT * FROM fn_locations where id IN "
            "(SELECT location_id FROM posts_fn_locations WHERE post_id = "
            "? )",
            (post_id,)
        ).fetchall()
        nfn_locations: list = db.execute(
            "SELECT * FROM nfn_locations where id IN "
            "(SELECT location_id FROM posts_nfn_locations WHERE post_id = "
            "? )",
            (post_id,)
        ).fetchall()
        container["locations"]: dict = {
            "fn": [loc["toponym"] for loc in fn_locations],
            "nfn": [loc["toponym"] for loc in nfn_locations]
        }

        # add tags
        tags: list = db.execute(
            "SELECT * FROM tags WHERE id IN "
            "(SELECT tag_id FROM posts_tags WHERE post_id = ? )",
            (post_id,)
        ).fetchall()
        container["tags"]: list = [tag["tag"] for tag in tags]

        complete_posts.append(container)

    return complete_posts


def get_post(id: int, check_author: bool = True) -> dict:
    """Get a post based on its id.

    Args:
        id (int): a post number id
        check_author (bool): if True will only return the post if the logged in
                             user is the creator of the post.

    Returns:
        sqlite3.Row  /  abort exception
    """
    post: dict = get_db().execute(
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


def insert(post_data: dict) -> None:
    """Inserts a new post and all related data into the database.

    Args:
        post_data (dict):

    Returns:
        None
    """
    title: str = post_data["title"]
    body: str = post_data["body"]
    images: list = post_data["images"]
    locations: list = post_data["locations"]
    tags: list = post_data["tags"]

    # first insert the post, so we can get its id
    db: Connection = get_db()
    cursor: Cursor = db.execute(
        "INSERT INTO posts (title, message, user_id) "
        "VALUES (?, ?, ?)",
        (title, body, g.user["id"])
    )
    db.commit()
    last_post_id: int = cursor.lastrowid

    # insert images using the post id reference
    if images:
        # print(images)
        db: Connection = get_db()
        for i, image in enumerate(images):
            # print(image)
            db.execute(
                "INSERT INTO pictures (post_id, picture_order, path, "
                "thumb) "
                "VALUES (?, ?, ?, ?)",
                (last_post_id, i + 1, image[0], image[1])
            )
            db.commit()

    # insert locations using the post id reference
    last_locations_ids: dict = {"fn": [], "nfn": []}
    for loc in locations["fn"]:
        # detect if string only has spaces
        if loc.strip() == '':
            continue
        loc: str = loc.strip()
        db: Connection = get_db()
        db.execute(
            "INSERT OR IGNORE INTO fn_locations (toponym) "
            "VALUES (?)",
            (loc,)
        )
        db.commit()
        # doing an INSERT then a SELECT in two steps to still get the id of the
        # last inserted element, even if it was IGNORED
        lastrowid: Row = db.execute(
            "SELECT id from fn_locations WHERE toponym = ?",
            (loc,)
        ).fetchone()
        last_locations_ids["fn"].append(lastrowid["id"])
    for loc in locations["nfn"]:
        if loc.strip() == '':
            continue
        loc: str = loc.strip()
        db: Connection = get_db()
        db.execute(
            "INSERT OR IGNORE INTO nfn_locations (toponym) "
            "VALUES (?)",
            (loc,)
        )
        db.commit()
        lastrowid: Row = db.execute(
            "SELECT id from nfn_locations WHERE toponym = ?",
            (loc,)
        ).fetchone()
        last_locations_ids["nfn"].append(lastrowid["id"])

    # insert the location - post relationship
    db: Connection = get_db()
    for loc in last_locations_ids["fn"]:
        db.execute(
            "INSERT INTO posts_fn_locations (post_id, location_id) "
            "VALUES (?, ?)",
            (last_post_id, loc)
        )
        db.commit()
    for loc in last_locations_ids["nfn"]:
        db.execute(
            "INSERT INTO posts_nfn_locations (post_id, location_id) "
            "VALUES (?, ?)",
            (last_post_id, loc)
        )

    # insert tags using the post id reference
    db: Connection = get_db()
    last_tags_ids: list = []
    for tag in tags:
        if tag.strip() == '':
            continue
        tag: str = tag.strip()
        db.execute(
            "INSERT OR IGNORE INTO tags (tag) "
            "VALUES (?)",
            (tag,)
        )
        db.commit()
        tag_id = db.execute(
            "SELECT id from tags WHERE tag = ?",
            (tag,)
        ).fetchone()
        last_tags_ids.append(tag_id["id"])

    # insert the tag - post relationship
    db: Connection = get_db()
    for tag in last_tags_ids:
        db.execute(
            "INSERT INTO posts_tags (post_id, tag_id) "
            "VALUES (?, ?)",
            (last_post_id, tag)
        )
        db.commit()
