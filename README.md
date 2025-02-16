# ICE CLIMBING REPORTS
#### Video Demo:  <URL HERE>
#### Description:

explain what your project is, what each of the files you wrote for the project contains and does, and if you debated certain design choices, explaining why you made them


## Sources
docs.python.org
Documentation about python modules I used like SQLite3

https://flask.palletsprojects.com/en/stable/tutorial/
Amazing tutorial that takes you deeper to dynamic web apps with flask than what we did on CS50. I took it as a base for this project. Many concepts were new to me. But searching documentation about them online I was able to learn so much more. Things like
 - creating SQL scripts so I can initialize the database on the first run
 - defining command line commands with the click package
 - using flask blueprints (something we did not learn in CS50)

https://flask.palletsprojects.com/en/stable/api/#
https://jinja.palletsprojects.com/en/stable/api/
https://werkzeug.palletsprojects.com/en/stable/
https://pillow.readthedocs.io
 - the manual reference for these various apis

https://getbootstrap.com/docs/5.3/getting-started/introduction/
https://www.sitepoint.com/bootstrap-grid-mastering-flexbox/
https://www.sitepoint.com/understanding-and-using-rem-units-in-css/
 - I got at bit more at ease with html, css and bootstrap. The bootstrap documentation feels less cryptic now. Also thanks to the many tutorials and guides I found online, I was able to unblock many of the design choices I decided to make.

https://www.stackoverflow.com
https://www.w3schools.com/
 - For all and any questions about html, jinja, css, python, bootstrap, flask, ...

www.rogers.com
 - Playing with my modem to open ports was a total failure. Then I realized I did not have my username and password to reconfigure the modem. The gentle people at Rogers helped me set it up back again. And this time I made sure to note down the configuration, username and password!! Now I can test my site in my computers and phones!! 



## Motivations
- Centralize communication channels between ice climbers. 
  So far we use a lot FaceBook and Messenger but finding past messages gets often difficult.
- Reduce hazard.
  Communication is a key part of safety. Quickly sharing current  conditions can make for more informed decision-making.
- Bring back the use of the first-nation toponomy.
  Increase importance, care and culture levels by making people more aware of their surroundings history and cultural heritage.
- Consolidate CS50 knowledge.
  One of my favorite things I have learned during this course has been the database creation and management (even though I apparently failed at the Fiftyville project :D ).
  Also, Flask has sparked a lot of interest on me!

## The project
The "Ice Climbing Reports" project is a web application that allows users to communicate with each other about their ice climbing experiences. These experiences can be either weather reports, state of the ice in a particular climbing site, personal stories about a particular ice climbing experience, tips and tricks, car-pooling, etc ...

I wanted it to be like a kind of facebook wall: a never ending scroll of reports organized by date where posts can have both text and images.
These posts have the following fields:
 - author and date
 - images (optional)
 - title
 - body
 - location tag (optional)
 - other tags (optional)


Even though I have taken care of the visual aspects of the site (to a certain extent), my main focus was to make a database-heavy project. Databases has been one of the topics that has excited me the most during this course. 
Hence, I wanted to practice and learn more about them.
Flask and Jinja have opened a whole new world of possibilities for me. I have never been a big fan of html and css. But now, thanks to CS50's teachings about flask and jinja, I am feeling more open to it. 


##Technical details
I have started this project with a diagram in which I have been noting down all ideas I wanted to implement, database organization and web-site design. This is a step I like doing before I start coding. Eventually I leave it on the side because the coding and the program has enough presence to make me comfortable enough to concentrate more on the technical aspects. Eventually the diagram ad the final product might not have much in common but at least it helped me to kickstart the project.

Here, I am going to describe the things I have been implementing in the project. I will present the information either file by file or folder by folder.


Here is a trimmed structure of the project:
```
ICR
├── __app.py
├── auth.py
├── blog.py
├── db.py
├── helpers.py
├── __init__.py
├── misc
│         ├── database_utils.py
│         ├── ice_climbing.sqlite
│         ├── icons.kra
│         └── xnview_scale_crop_preset_001.xbs
├── schema.sql
├── static
│         ├── css
│         │         └── main.css
│         ├── icons
│         │         └── icons
│         │             ├── icon_01.PNG
│         │             └── ...
│         └── images
│             ├── 2024_12
│             │         ├── pictures
│             │         │         ├── 2020_03_01_08_47_12.jpg
│             │         │         └── ...
│             │         └── thumbnails
│             │             ├── 2020_03_01_08_47_12_tmb.jpg
│             │             └── file_tmb.jpg
│             ├── 2025_01
│             │         ├── pictures
│             │         │         ├── 2020_03_01_10_18_12.jpg
│             │         │         └── ...
│             │         └── thumbnails
│             │             ├── 2020_03_01_10_18_12_tmb.jpg
│             │             └── ...
│             ├── 2025_02
│             │         ├── pictures
│             │         │         ├── 2020_12_30_09_18_34.jpg
│             │         │         └── ...
│             │         └── thumbnails
│             │             ├── 2020_12_30_09_18_34_tmb.jpg
│             │             └── ...
│             ├── favicon.ico
│             └── I_heart_validator.png
└── templates
    ├── apology.html
    ├── auth
    │         ├── login.html
    │         └── register.html
    ├── base.html
    ├── blog
    │         ├── create.html
    │         ├── index_grid.html
    │         ├── _index.html
    │         ├── index.html
    │         └── update.html
    ├── create_report.html
    ├── full_screen_carousel1.html
    ├── full_screen_carousel.html
    ├── index_old.html
    └── post_template.html
```

###misc
#####database_utils.py

#####ice_climbing.sqlite

###static
####css
####icons
####images

###templates
Write a general ru about the templates and blueprnts. Enter into more detail into any particular template or blueprint that has something special.

####__app.py
####__init__.py
####auth.py
####blog.py
####db.py
####helpers.py

####schema.sql
details about this script and how I structured the database. Maybe include the drawin!!!

Git
I do not feel very at ease with git still. I have mostly worked off-line, mainly on a branch and not pushing to it very often. Many tests have been deleted when the right recipe was found.
I have used it professionally for many years, but always like an alchemist 
working on the philosopher stone but fearing a big explosion that would fry my brain.
I know the day I will lose this fear a bit I will feel much more comfortable with it.


file uploads:
https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
