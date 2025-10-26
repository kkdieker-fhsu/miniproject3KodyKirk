# Please submit a link to your GitHub project. Do not submit your project files here!
#
# This project will be using Flask to deploy a small web app of your choice. The goal here is to come up with a small web application that meets the requirements below. If you get stuck here, please email me!
#
#     (5/5 points) Initial comments with your name, class and project at the top of your .py file.
#     (5/5 points) Proper import of packages used.
#     (70/70 points) Using Flask you need to setup the following:
#     (10/10 points) Setup a proper folder structure, use the tutorial as an example.
#     (20/20 points) You need to have a minimum of 5 pages, using a proper template structure.
#     (10/10 points) You need to have at least one page that utilizes a form and has the proper GET and POST routes setup.
#     (10/10 points) You need to setup a SQLlite database with a minimum of two tables, linked with a foreign key.
#     (10/10) You need to use Bootstrap in your web templates. I won't dictate exactly what modules you need to use but the more practice here the better. You need to at least make use of a modal.
#     (10/10) You need to setup some sort of register and login system, you can use the tutorial as an example.
#     (5/5 points) There should be a minimum of 5 commits on your project, be sure to commit often!
#     (5/5 points) I will be checking out the main branch of your project. Please be sure to include a requirements.txt file which contains all the packages that need installed. You can create this fille with the output of pip freeze at the terminal prompt.
#     (10/10 points) There should be a README.md file in your project that explains what your project is, how to install the pip requirements, and how to execute the program. Please use the GitHub flavor of Markdown. Be thorough on the explanations. You will need to explain the steps of initializing the database and then how to run the development server for your project.

import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='landing')

    return app
