import datetime
import os
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash


def create_db():
    os.chdir("/home/fuku/PycharmProjects/webtest/ICR/misc")
    if "ice_climbing.db" in os.listdir("."):
        os.remove("ice_climbing.db")
    DB = sqlite3.connect("ice_climbing.sqlite")
    cursor = DB.cursor()

    DB.execute("""
    CREATE TABLE users(
        id INT PRIMARY KEY NOT NULL,
        name TEXT,
        icon TEXT,
        email TEXT,
        hash TEXT NOT NULL)
    """)
    users = (
        (0, 'a', '', '', generate_password_hash("a")),
        (1, 'b', '', '', generate_password_hash("b")),
        (2, 'c', '', '', generate_password_hash("c")),
    )
    cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?)", users)

    DB.execute("""
    CREATE TABLE posts(
        post_id INT PRIMARY KEY NOT NULL,
        user_id INT NOT NULL,
        title TEXT NOT NULL,
        message TEXT,
        pictures TEXT,
        audios TEXT,
        location TEXT,
        datetime TIMESTAMP NOT NULL)
    """)

    posts = (
        {
            "post_id": 0,
            "user_id": 0,
            "title": "Post 1 title",
            "message": "This is the message of post 1!!!",
            "location": "Shawbridge",
            "datetime": datetime.datetime.strptime("2023-01-21 09:05:15",
                "%Y-%m-%d %H:%M:%S")
        },
        {
            "post_id": 1,
            "user_id": 1,
            "title": "Post 2 title",
            "message": "This is the message of post 2!!!",
            "location": "Lac Silvere",
            "datetime": datetime.datetime.strptime("2023-02-03 11:35:45",
                "%Y-%m-%d %H:%M:%S")
        },
        {
            "post_id": 2,
            "user_id": 0,
            "title": "Post 3 title",
            "message": "This is the message of post 3!!!",
            "location": "Weir",
            "datetime": datetime.datetime.strptime("2023-12-21 07:03:55",
                "%Y-%m-%d %H:%M:%S")
        },
        {
            "post_id": 3,
            "user_id": 2,
            "title": "Post 4 title",
            "message": "This is the message of post 4!!!",
            "location": "Shawbridge",
            "datetime": datetime.datetime.strptime("2024-01-02 08:06:25",
                "%Y-%m-%d %H:%M:%S")
        },
    )
    command = ("INSERT INTO posts (post_id, user_id, title, message, datetime) "
               "VALUES (:post_id, :user_id, :title, :message, :datetime)")
    cursor.executemany(command, posts)

    DB.execute("""
    CREATE TABLE pictures(
        id INT PRIMARY KEY NOT NULL,
        post_id INT NOT NULL,
        position INT NOT NULL,
        path TEXT NOT NULL)
    """)
    pictures = (
        {
            "id": 0,
            "post_id": 0,
            "position": 0,
            "path": "static/images/2025_01/thumbnails/2021_02_27_08_58_47_tmb.jpg"
        },
        {
            "id": 1,
            "post_id": 0,
            "position": 0,
            "path": "static/images/2025_01/thumbnails/2021_02_20_11_48_48_tmb.jpg"
        },
        {
            "id": 2,
            "post_id": 1,
            "position": 0,
            "path": "static/images/2025_01/thumbnails/2021_01_30_12_34_00_tmb.jpg"
        },
        {
            "id": 3,
            "post_id": 1,
            "position": 0,
            "path": "static/images/2025_01/thumbnails/2021_01_30_10_54_32_tmb.jpg"
        },
        {
            "id": 4,
            "post_id": 1,
            "position": 0,
            "path": "static/images/2025_01/thumbnails/2020_03_01_10_19_35_tmb.jpg"
        },
        {
            "id": 5,
            "post_id": 1,
            "position": 0,
            "path": "static/images/2024_12/thumbnails/2021_02_14_09_32_50_tmb.jpg"
        },
        {
            "id": 6,
            "post_id": 2,
            "position": 0,
            "path": "static/images/2024_12/thumbnails/2021_01_30_14_09_22_tmb.jpg"
        },
        {
            "id": 7,
            "post_id": 2,
            "position": 0,
            "path": "static/images/2024_12/thumbnails/2021_01_30_14_08_34_tmb.jpg"
        },
        {
            "id": 8,
            "post_id": 3,
            "position": 0,
            "path": "static/images/2024_12/thumbnails/2020_03_01_11_48_20_tmb.jpg"
        },
        {
            "id": 9,
            "post_id": 3,
            "position": 0,
            "path": "static/images/2024_12/thumbnails/2020_03_01_08_47_12_tmb.jpg"
        },
    )
    command = ("INSERT INTO pictures VALUES (:id, :post_id, :position, :path)")
    cursor.executemany(command, pictures)


    DB.execute("""
    CREATE TABLE tags(
        id INT PRIMARY KEY NOT NULL,
        post_id INT NOT NULL,
        tag TEXT NOT NULL)
    """)
    tags = (
        {"id": 0, "post_id": 0, "tag": "high"},
        {"id": 1, "post_id": 1, "tag": "melting"},
        {"id": 2, "post_id": 1, "tag": "formed"},
        {"id": 3, "post_id": 1, "tag": "plastic"},
        {"id": 4, "post_id": 4, "tag": "strong wind"},
    )
    command = ("INSERT INTO tags VALUES (:id, :post_id, :tag)")
    cursor.executemany(command, tags)

    DB.commit()

    # create a cursor object for select query
    cursor = DB.execute("SELECT * from users")
    for row in cursor:
        print(row)
    cursor = DB.execute("SELECT * from posts")
    for row in cursor:
        print(row)
    cursor = DB.execute("SELECT * from pictures")
    for row in cursor:
        print(row)
    cursor = DB.execute("SELECT * from tags")
    for row in cursor:
        print(row)


if __name__ == "__main__":
    create_db()