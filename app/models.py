from app import db, login_manager
from datetime import datetime
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username =db.Column(db.String(250), index = True,unique = True)
    first_name =db.Column(db.String(250), index = True)
    last_name =db.Column(db.String(250), index = True)
    password=db.Column(db.String(250), index = True)
    #messages = db.relationship('Message', backref = 'recipient', lazy = 'dynamic')
    user_type = db.Column(db.Integer, db.ForeignKey("user_types.id"))
    def __repr__(self):
        return "<User %s>" % self.username
    # Methods needed by Flask-Login
    def is_authenticated(self):
        # Just true is enough for our purposes
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.id)
    def get_user_type_id(self):
        return unicode(self.user_type)
#==============================================================================================
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))  
#==============================================================================================
class UserTypes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type =db.Column(db.String)
    type_name =db.Column(db.String)
#==============================================================================================
class Categories(db.Model):
    __tablename__ = 'categories' # define tabel name
    id=db.Column(db.Integer, primary_key = True)
    parent_id=db.Column(db.Integer, db.ForeignKey('categories.id'),nullable=False)
    name=db.Column(db.String,nullable=True)
    logo=db.Column(db.String,nullable=True)
    logo_path=db.Column(db.String,nullable=True)
    status= db.Column(db.Enum('A','D'),nullable=True)
    created_at=db.Column(db.DateTime, default=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at=db.Column(db.DateTime,nullable=True)
    subCategory = db.relationship('Categories', order_by="asc(Categories.name)", uselist=True) # self join from foreignkey to primarykey
    parentCategory = db.relationship('Categories', remote_side=id, backref='parent_category') # self join from  primarykey to foreignkey
#==============================================================================================
class Products(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    cat_id=db.Column(db.Integer, db.ForeignKey('categories.id'),nullable=False)
    sub_cat_id=db.Column(db.Integer,db.ForeignKey('categories.id'),nullable=False)
    p_name=db.Column(db.String(250),nullable=True)
    p_descriptions=db.Column(db.Text,nullable=True)
    p_price=db.Column(db.Float,default=0)
    p_discount_percent=db.Column(db.Float,default=0)
    default_image=db.Column(db.String(250),nullable=True)
    default_image_path=db.Column(db.String(250),nullable=True)
    created_by=db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    status=  db.Column(db.Enum('A','D'),nullable=True)
    is_feature=  db.Column(db.Enum('N','Y'),default='N')
    is_banner_appear= db.Column(db.Enum('N','Y'),default='N')
    banner_image=db.Column(db.String(255),nullable=True)
    banner_image_path=db.Column(db.String(255),nullable=True)
    created_at=db.Column(db.DateTime, default=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at=db.Column(db.DateTime,nullable=True)
    size_id=db.Column(db.Integer,db.ForeignKey('sizes.id'),default=0)
    color_id=db.Column(db.Integer,db.ForeignKey('colors.id'),default=0)
    total_review=db.Column(db.Integer,default=0)
    total_rating=db.Column(db.Integer,default=0)
    total_rating_points=db.Column(db.Float,default=0)
    #images = db.relationship('ProductImages', backref='product', lazy=True)
    images = db.relationship('ProductImages',order_by="desc(ProductImages.id)", lazy='select',backref=db.backref('products', lazy='joined'))
    parentCategory = db.relationship('Categories', primaryjoin='Products.cat_id==Categories.id', lazy='joined',uselist=False) # primary table jon
    subCategory = db.relationship('Categories', primaryjoin='Products.sub_cat_id==Categories.id', lazy='joined',uselist=False) # primary table jon
    color=db.relationship("Colors", backref=db.backref("colors",lazy='joined', uselist=False))
    size=db.relationship("Sizes", backref=db.backref("sizes",lazy='joined', uselist=False))
    productReviews=db.relationship('ProductReviews',order_by="desc(ProductReviews.id)" ,primaryjoin='Products.id==ProductReviews.p_id', lazy='joined',uselist=True) 
    productRatings=db.relationship('ProductRatings', primaryjoin='Products.id==ProductRatings.p_id', lazy='joined',uselist=True)
#==============================================================================================
class ProductImages(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    p_id = db.Column(db.Integer, db.ForeignKey('products.id'),nullable=False)
    image=db.Column(db.String(250),nullable=True)
    image_path=db.Column(db.String(255),nullable=True)
    type=db.Column(db.Enum('D','O'),default='D')
    created_at=db.Column(db.DateTime, default=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at=db.Column(db.DateTime,nullable=True)
#==============================================================================================
class Colors(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    color_code=db.Column(db.String(255),nullable=True)
    status=  db.Column(db.Enum('A','D'),nullable=True)
#==============================================================================================
class Sizes(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    size_name=db.Column(db.String(255),nullable=True)
    status=  db.Column(db.Enum('A','D'),nullable=True)
#==============================================================================================
class Wishlist(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    p_id = db.Column(db.Integer, db.ForeignKey('products.id'),nullable=False)
    created_by=db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at=db.Column(db.DateTime,nullable=True)
#==============================================================================================
class ProductReviews(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    p_id = db.Column(db.Integer, db.ForeignKey('products.id'),nullable=False)
    review=db.Column(db.String(255),nullable=True)
    status=  db.Column(db.Enum('A','R'),nullable=True)
    created_by=db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at=db.Column(db.DateTime,nullable=True)
    reviewBy=db.relationship("Users", backref=db.backref("Reviews",lazy='joined', uselist=False))
#==============================================================================================
class ProductRatings(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    p_id = db.Column(db.Integer, db.ForeignKey('products.id'),nullable=False)
    rating_points=db.Column(db.Float,default=0)
    created_by=db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at=db.Column(db.DateTime,nullable=True)
    ratingBy=db.relationship("Users", backref=db.backref("Rating", lazy='joined', uselist=False))
#==============================================================================================