from flask import Flask,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect
import flask_resize
from datetime import datetime
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

csrf = CSRFProtect(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

app.config["RESIZE_URL"] = '/static/uploads'
app.config["RESIZE_ROOT"] = 'app/static/uploads/'
app.config["RESIZE_CACHE"] = 'app/static/cache/'
app.config["RESIZE_TARGET_DIRECTORY"] = 'cache'
resize = flask_resize.Resize(app)

# Function to easily find your assets
# In your template use <link rel=stylesheet href="{{ static('filename') }}">
app.jinja_env.globals['static'] = lambda filename: url_for('static', filename = filename)
app.jinja_env.globals['get_authenticated_user'] = lambda: current_user if current_user.is_authenticated else None

angular_syntax = {
    'block_start_string': '{{{%',
    'block_end_string': '%}}}',
    'variable_start_string': '{{{',
    'variable_end_string': '}}}',
    'comment_start_string': '{{{#',
    'comment_end_string': '}}}',
}
app.angular_env = app.jinja_env.overlay(**angular_syntax)
from app import views, models, forms, api
app.jinja_env.globals['get_unread_count'] = views.get_unread_count
#================== Category list broadcast ==============================
app.jinja_env.globals['getCategoryList'] = views.getCategoryList
app.jinja_env.globals['dateTime'] = datetime
# This is the path to the upload directory
app.config['UPLOAD_TEMP_FOLDER'] = '/static/uploads/temp/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_IMAGE_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['MAX_ONETIME_FILE_UPLOAD']=20
app.config['PER_PAGE_RECORD']=12
app.config['dateTime']=datetime