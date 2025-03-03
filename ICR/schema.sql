DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS pictures;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS posts_tags;
DROP TABLE IF EXISTS icons;
DROP TABLE IF EXISTS fn_locations;
DROP TABLE IF EXISTS nfn_locations;
DROP TABLE IF EXISTS posts_fn_locations;
DROP TABLE IF EXISTS posts_nfn_locations;
DROP TABLE IF EXISTS likes;

CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        icon TEXT,
        email TEXT UNIQUE,
        hash TEXT NOT NULL
);

CREATE TABLE posts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        message TEXT,
        datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pictures(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        picture_order INTEGER NOT NULL,
        path TEXT NOT NULL,
        thumb TEXT NOT NULL
);

CREATE TABLE tags(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag TEXT NOT NULL UNIQUE
);

CREATE TABLE posts_tags(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        tag_id INTEGER NOT NULL
);

CREATE TABLE icons(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        icon TEXT NOT NULL,
        alt_text TEXT NOT NULL
);

CREATE TABLE fn_locations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        toponym TEXT UNIQUE
);

CREATE TABLE nfn_locations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        toponym TEXT UNIQUE
);

CREATE TABLE posts_fn_locations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        location_id INTEGER NOT NULL
);

CREATE TABLE posts_nfn_locations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        location_id INTEGER NOT NULL
);

CREATE TABLE likes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL
);




INSERT INTO users (name, icon, email, hash)
VALUES ('x', '1', 'x@gmail.com', 'scrypt:32768:8:1$zLtRUFbZGzVPNrpk$1c275fa1bdd388d80806a3af953b3c717052b648f39faaa5de0208d14b915172e50151ed4d0ab587bc1f287e0b5dd8f56e76dc6e90b510c03f9a0d9a1405aa75');
INSERT INTO users (name, icon, email, hash)
VALUES ('y', '2', 'y@gmail.com', 'scrypt:32768:8:1$A6n4gQYyUazMo5ht$d3184c265be64b343a96fb7bd35db2adb9f167b45d970ff34297ba26d4cbef6f0675fe841c9ec6766abf00722e5acb53da5c5482f9c3309c41825a4904abace2');
INSERT INTO users (name, icon, email, hash)
VALUES ('z', '3', 'z@gmail.com', 'scrypt:32768:8:1$uSWOxm9ncW10TAVg$79fdbc186871ce029e0f8ab211ee10b001632c96c3d557ec98b58e47f788ee8bf967fcbb5471bb674b47e305a949c1af0bd8db77123f2b2fc38f7b20a1b348fe');

INSERT INTO posts (user_id, title, message, datetime)
VALUES (
1,
'First time ice climbing',
'Before I started ice climbing, I thought ice axes were like wood axes, used to chop through ice. I was wrong. The first time I held ice axes, I was struck by their lightness and precision. The instructor demonstrated how to use them to make precise placements in the ice.',
'2022-01-01 11:03:27'
);
INSERT INTO posts (user_id, title, message, datetime)
VALUES (
1,
'The first fall',
'My first ice climbing fall was a memorable one. I was trying to make a tricky placement when my axe slipped out of the ice. I landed on my side, and as I sat up, I felt something peculiar poking into my left leg. I looked down to see six sausages sizzling on the fire my friends had built, stuck to my crampon. I laughed as my friends cheered and snapped photos. It was a surreal moment, and I was grateful that my first fall was not more serious. And of course, I had a snack ready to go afterwards!',
'2023-02-01 12:01:47'
);
INSERT INTO posts (user_id, title, message, datetime)
VALUES (
1,
'Third experience',
'The third time I went ice climbing was a surreal experience. We ventured to a remote location, and as we hiked up the mountain, the sound of crunching snow beneath our feet was all that broke the silence. The ice wall glinted in the morning sun, and I felt a rush of excitement as I strapped on my crampons and harness. But as I began to climb, I noticed we were not alone. A herd of Rocky Mountain goats emerged from the forest, their eyes fixed on us. They wandered closer, their fur fluffed up against the cold, and I felt a sense of wonder. We shared the frozen turf of grass as popsicles, and I felt a deep connection to these creatures and this land. The climb was challenging, but the experience was made all the more special by the presence of these majestic animals. As I reached the top, I felt a sense of accomplishment, not just because of the climb, but because I had shared it with the goats.',
'2023-12-21 08:21:43'
);

INSERT INTO posts (user_id, title, message, datetime)
VALUES (2,
'Shawbridge in great shape',
'I climbed the ice wall at Shawbridge yesterday and it was in great shape! The ice was thick and solid, and the anchors were all in good condition. The ice was a bit brittle, but not so much that it was a problem. The approach was easy, with good snow cover and no crevasses. The climb was challenging, but the scenery was beautiful and it was a great workout. I highly recommend it if you are looking for a fun and challenging ice climb.',
'2023-12-21 08:21:43'
);
INSERT INTO posts (user_id, title, message, datetime)
VALUES (2,
'Weir is over',
'The ice waterfall at Weir is all melted and is dangerous to climb. The ice is thin and brittle, and there are open holes everywhere. The anchors are also in bad condition, and the approach is a muddy mess. Don t bother going.',
'2024-02-11 08:00:56'
);

INSERT INTO posts (user_id, title, message, datetime)
VALUES (3,
'Frozen river risks',
'Crossing a frozen river presents significant hazards. Ice thickness can vary unpredictably, leading to potential breakthroughs. Hidden currents weaken ice integrity, increasing danger. Temperature fluctuations may cause cracks. Frostbite and hypothermia are real threats in cold conditions. Always assess safety before attempting a crossing.',
'2024-02-11 08:10:33'
);
INSERT INTO posts (user_id, title, message, datetime)
VALUES (3,
'How to tie the figure 8 knot',
'To tie the figure 8 knot, make a loop in the rope, passing the end over itself. Thread the end through the loop, creating an 8 shape. Pull tight. To secure, retrace the knot by following the path of the original loop with the rope end.',
'2024-03-14 12:11:11'
);
INSERT INTO posts (user_id, title, message, datetime)
VALUES (3,
'Sharpening your ice axe and crampons',
'Sharpen your ice axe by holding it at a 20 degree angle and running it along a whetstone. Switch sides and repeat. Sharpen crampons by holding them vertically and running them along a whetstone at a 20 degree angle. Do not sharpen crampons too much, as it can weaken them.',
'2024-04-20 12:11:53'
);

INSERT INTO pictures (post_id, picture_order, path, thumb)
VALUES (1, 1, 'static/images/2024_12/pictures/2020_03_01_08_47_12.jpg',
'static/images/2024_12/thumbnails/2020_03_01_08_47_12_tmb.jpg');
INSERT INTO pictures (post_id, picture_order, path, thumb)
VALUES (1, 2, 'static/images/2024_12/pictures/2020_03_01_10_24_16.jpg',
'static/images/2024_12/thumbnails/2020_03_01_10_24_16_tmb.jpg');
INSERT INTO pictures (post_id, picture_order, path, thumb)
VALUES (1, 3, 'static/images/2024_12/pictures/2020_03_01_11_48_17.jpg',
'static/images/2024_12/thumbnails/2020_03_01_11_48_17_tmb.jpg');
INSERT INTO pictures (post_id, picture_order, path, thumb)
VALUES (1, 4, 'static/images/2024_12/pictures/2020_03_01_11_48_26.jpg',
'static/images/2024_12/thumbnails/2020_03_01_11_48_26_tmb.jpg');

INSERT INTO pictures (post_id, picture_order, path, thumb)
VALUES (2, 1, 'static/images/2024_12/pictures/2020_03_01_13_39_21.jpg',
'static/images/2024_12/thumbnails/2020_03_01_13_39_21_tmb.jpg');
INSERT INTO pictures (post_id, picture_order, path, thumb)
VALUES (2, 2, 'static/images/2024_12/pictures/2020_03_01_13_39_29.jpg',
'static/images/2024_12/thumbnails/2020_03_01_13_39_29_tmb.jpg');
INSERT INTO pictures (post_id, picture_order, path, thumb)
VALUES (2, 3, 'static/images/2024_12/pictures/2021_01_30_09_50_38.jpg',
'static/images/2024_12/thumbnails/2021_01_30_09_50_38_tmb.jpg');
INSERT INTO pictures (post_id, picture_order, path, thumb)
VALUES (2, 4, 'static/images/2024_12/pictures/2021_01_30_14_08_19.jpg',
'static/images/2024_12/thumbnails/2021_01_30_14_08_19_tmb.jpg');

INSERT INTO pictures (post_id, picture_order, path, thumb)
VALUES (3, 1, 'static/images/2024_12/pictures/2021_01_30_14_09_19.jpg',
'static/images/2024_12/thumbnails/2021_01_30_14_09_19_tmb.jpg');
INSERT INTO pictures (post_id, picture_order, path, thumb)
VALUES (3, 2, 'static/images/2024_12/pictures/2021_01_30_14_09_22.jpg',
'static/images/2024_12/thumbnails/2021_01_30_14_09_22_tmb.jpg');
INSERT INTO pictures (post_id, picture_order, path, thumb)
VALUES (3, 3, 'static/images/2024_12/pictures/2021_01_30_14_10_12.jpg',
'static/images/2024_12/thumbnails/2021_01_30_14_10_12_tmb.jpg');
INSERT INTO pictures (post_id, picture_order, path, thumb)
VALUES (3, 4, 'static/images/2024_12/pictures/2021_01_30_14_10_17.jpg',
'static/images/2024_12/thumbnails/2021_01_30_14_10_17_tmb.jpg');

INSERT INTO tags (tag) VALUES ('ice');
INSERT INTO tags (tag) VALUES ('conditions');
INSERT INTO tags (tag) VALUES ('accident');

INSERT INTO icons (icon, alt_text)
VALUES ('static/icons/icon_01.png', 'icon1');
INSERT INTO icons (icon, alt_text)
VALUES ('static/icons/icon_02.png', 'icon2');
INSERT INTO icons (icon, alt_text)
VALUES ('static/icons/icon_03.png', 'icon3');

INSERT INTO fn_locations (toponym)
VALUES ("native-Lac Du Rocher");
INSERT INTO fn_locations (toponym)
VALUES ("native_Weir");
INSERT INTO fn_locations (toponym)
VALUES ("native-Lac Sylvère");
INSERT INTO fn_locations (toponym)
VALUES ("Coaticook");

INSERT INTO nfn_locations (toponym)
VALUES ("Shawbridge");
INSERT INTO nfn_locations (toponym)
VALUES ("Weir");
INSERT INTO nfn_locations (toponym)
VALUES ("Lac Sylvère");

INSERT INTO posts_tags (post_id, tag_id) VALUES (1, 1);
INSERT INTO posts_tags (post_id, tag_id) VALUES (1, 2);
INSERT INTO posts_tags (post_id, tag_id) VALUES (1, 3);
INSERT INTO posts_tags (post_id, tag_id) VALUES (2, 1);
INSERT INTO posts_tags (post_id, tag_id) VALUES (3, 2);
INSERT INTO posts_tags (post_id, tag_id) VALUES (4, 3);
INSERT INTO posts_tags (post_id, tag_id) VALUES (5, 3);
INSERT INTO posts_tags (post_id, tag_id) VALUES (5, 1);
INSERT INTO posts_tags (post_id, tag_id) VALUES (6, 1);
INSERT INTO posts_tags (post_id, tag_id) VALUES (7, 2);
INSERT INTO posts_tags (post_id, tag_id) VALUES (8, 3);
INSERT INTO posts_tags (post_id, tag_id) VALUES (8, 2);
--
INSERT INTO posts_fn_locations (post_id, location_id) VALUES (1, 1);
INSERT INTO posts_fn_locations (post_id, location_id) VALUES (1, 3);
INSERT INTO posts_fn_locations (post_id, location_id) VALUES (3, 2);
INSERT INTO posts_fn_locations (post_id, location_id) VALUES (4, 3);
INSERT INTO posts_fn_locations (post_id, location_id) VALUES (5, 3);
INSERT INTO posts_fn_locations (post_id, location_id) VALUES (7, 2);
INSERT INTO posts_fn_locations (post_id, location_id) VALUES (8, 1);

INSERT INTO posts_nfn_locations (post_id, location_id) VALUES (1, 2);
INSERT INTO posts_nfn_locations (post_id, location_id) VALUES (2, 1);
INSERT INTO posts_nfn_locations (post_id, location_id) VALUES (4, 2);
INSERT INTO posts_nfn_locations (post_id, location_id) VALUES (4, 3);
INSERT INTO posts_nfn_locations (post_id, location_id) VALUES (6, 3);
INSERT INTO posts_nfn_locations (post_id, location_id) VALUES (7, 2);
INSERT INTO posts_nfn_locations (post_id, location_id) VALUES (7, 1);