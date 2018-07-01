from flask import Flask
from wtforms import *
#from app import db, models
class SignUpForm(Form):
    name = TextField('Name', [validators.Length(min=1, max=190),validators.InputRequired()])
    email = TextField('Email Address', [validators.Length(min=1, max=190),validators.InputRequired(),validators.Email()])
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password',[validators.DataRequired()])
class LoginForm(Form):
    email = TextField('email',[validators.InputRequired(), validators.Email()])
    password = PasswordField('password',[validators.InputRequired()])
    remember = BooleanField('remember', default=False)
class AdminLoginForm(Form):
    username = TextField('User Name',[validators.InputRequired()])
    password = PasswordField('Password',[validators.InputRequired()])
    remember = BooleanField('Remember', default=False)
class AdminCategory(Form):
    category_name=TextField('Category Name',[validators.Length(min=1, max=190),validators.InputRequired()])
    category_image=FileField('Category Logo')
class AdminProduct(Form):
    product_name=TextField('Product Name',[validators.InputRequired()])
    category=StringField('select Category',[validators.InputRequired()])
    sub_category=StringField('select sub Category',[validators.InputRequired()])
    is_feature_product=StringField('Is feature product',[validators.InputRequired()])
    is_appear_on_banner=StringField('Appear on banner',[validators.InputRequired()])
    product_descriptions=TextAreaField('Product Descriptions',[validators.InputRequired()])
    product_price=DecimalField('Product Price',[validators.InputRequired()],default=0, places=2, rounding=None, use_locale=False, number_format=None)
    product_discount_percent=DecimalField('Product Discount Percent',[validators.InputRequired()],default=0,places=2, rounding=None, use_locale=False, number_format=None)
    product_default_image=FileField('Product Default Image')
    product_other_images=FileField('Product Other Images')
    banner_image=FileField('Product Other Images')
class AdminSubCategory(Form):
    category_name=TextField('Category Name',[validators.Length(min=1, max=190),validators.InputRequired()])
    category_image=FileField('Category Logo')
    parent_category=StringField('select Parent Category',[validators.InputRequired()])
class AdminColor(Form):
    color_code=TextField('Color Code',[validators.InputRequired()])
class AdminSize(Form):
    size=TextField('Size',[validators.InputRequired()])