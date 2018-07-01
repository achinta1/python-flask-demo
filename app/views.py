import os
from flask import render_template, url_for, redirect, request, flash, abort,jsonify
from app import db, app, forms, models, api, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from app.decorators import json_result
from datetime import datetime
from werkzeug import secure_filename
import random
import uuid
from flask_paginate import Pagination, get_page_parameter
basedir = os.path.abspath(os.path.dirname(__file__))
#=================================================================
@app.route('/',methods=["GET"])
def index():
    user = None
    passData={}
    if current_user.is_authenticated:
        user = current_user
        if user_type()=='sadmin':
            return redirect(url_for('adminDashboard'))
    #-----------------------------------------------
    passData['bannerList']=models.Products.query.filter_by(status='A',is_banner_appear='Y').order_by(models.Products.created_at.desc()).all()
    #-----------------------------------------------
    passData['featureProductList']=models.Products.query.filter_by(status='A',is_feature='Y').order_by(models.Products.created_at.desc()).all()
    #-----------------------------------------------
    passData['latestProductList']=models.Products.query.filter_by(status='A',is_banner_appear='N',is_feature='N').order_by(models.Products.created_at.desc()).all()
    return render_template("Front/home.html", user=user,passData=passData)
#app.login_manager.login_view = "login"
#=================================================================
@app.route('/product-list')
def productList():
    user = None
    passData={}
    if current_user.is_authenticated:
        user = current_user
        if user_type()=='sadmin':
            return redirect(url_for('adminDashboard'))
    #passData['UX']=models.Products.query.filter_by(status='A').order_by(models.Products.created_at.desc()).paginate(1,2,error_out=False)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    if page<=0:
        page=1
    passData['listRecord']=models.Products.query.filter_by(status='A').order_by(models.Products.created_at.desc())
    totalRecord=0
    if passData['listRecord']!=None:
        totalRecord=passData['listRecord'].count()
    passData['listRecord']=passData['listRecord'].paginate(page,app.config['PER_PAGE_RECORD'],error_out=False)
    passData['pagination'] = Pagination(page=page, total=totalRecord, search='', record_name='items',per_page=app.config['PER_PAGE_RECORD'])

    return render_template("Front/productList.html", user=user,passData=passData)
#################### :::: ADMIN SECTION ::::: #########################
#====================================================================================
@app.route('/admin/login', methods=["GET", "POST"])
def adminLogin():
    if current_user.is_authenticated:
        return redirect(url_for('adminDashboard'))
    else:
        form = forms.AdminLoginForm()
        next_url = request.args.get('next', url_for('index'))
        if request.method == "POST":
            form = forms.AdminLoginForm(request.form)
            if form.validate():
                u = authenticate_user(form)
                if u:
                    login_user(u)
                    next_url = request.args.get('next', url_for('adminDashboard'))
                    return redirect(next_url)
                flash("Invalid User Name or Password", "danger")
            else:
                flash("Please fill all the input field", "danger")
        return render_template("Admin/login.html", form=form, next_url=next_url)
#====================================================================================
@app.route('/admin/logout')
def AdminLogout():
    if current_user.is_authenticated:
        logout_user()
        flash("You have been logged out", "success")
    return redirect(url_for('adminLogin'))
#====================================================================================
@login_required
@app.route('/admin/dashboard')
def adminDashboard():
    #dashboardData=api.MessageList().get()
    dashboardData = None
    pageMetaTitle="Dashboard"
    activeMenu="Dashboard"
    pageTitle="Welcome to Flask Dashboard"
    return render_template('Admin/dashboard.html', user=current_user, dashboardData=dashboardData,pageMetaTitle=pageMetaTitle,activeMenu=activeMenu,pageTitle=pageTitle)
############### Category Section [Start] #############################
#====================================================================================
@app.route('/admin/category/list', methods=['GET'])
def adminCategoryList():
    categoryList=None
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            categoryList=models.Categories.query.filter_by(parent_id=0).order_by(models.Categories.created_at.desc(),models.Categories.name.asc()).all()
    pageMetaTitle="Manage Categories"
    activeMenu="ManageCategories"
    activeSubMenu="ManageParentCategories"
    pageTitle="Category List"
    return render_template('Admin/category/list.html', user=current_user, categoryList=categoryList,pageMetaTitle=pageMetaTitle,activeMenu=activeMenu,pageTitle=pageTitle,activeSubMenu=activeSubMenu)
#====================================================================================
@app.route('/admin/category/add', methods=['GET','POST'])
def adminCategoryAdd():
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            pageMetaTitle="Category Add"
            activeMenu="ManageCategories"
            activeSubMenu="ManageParentCategories"
            pageTitle="Category Add"
            form = forms.AdminCategory()
            if request.method == "POST":
                form = forms.AdminCategory(request.form)
                if form.validate():
                    errorCounter=1
                    uploadedFileName=None
                    uploadedFilePath=None
                    uploadDirectoryPath="/static/uploads/"
                    if request.files!=None and  'category_logo' in request.files:
                        if allowed_image_file(request.files['category_logo'].filename):
                            # Make the filename safe, remove unsupported chars
                            uploadedFileName=uuid.uuid4().hex+'.'+request.files['category_logo'].filename.rsplit('.', 1)[1]
                            uploadedFileName = secure_filename(uploadedFileName)
                            # Move the file form the temporal folder to the upload
                            # load in server temp folder
                            #request.files['category_logo'].save(os.path.join(basedir+app.config['UPLOAD_TEMP_FOLDER'], uploadedFileName))
                            request.files['category_logo'].save(os.path.join(basedir+uploadDirectoryPath, uploadedFileName))
                            uploadedFilePath="uploads/"+uploadedFileName
                        else:
                            errorCounter=errorCounter+1
                    if errorCounter==1:
                        db.session.add(models.Categories(name=form.category_name.data,logo=uploadedFileName,logo_path=uploadedFilePath,status='A',created_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
                        db.session.commit()
                        flash("Record has been added successfully.", "success")
                        return redirect(url_for('adminCategoryList'))
                else:
                    flash("Please fill all the input field", "danger")
            return render_template('Admin/category/add.html', user=current_user, form=form,pageMetaTitle=pageMetaTitle,activeMenu=activeMenu,pageTitle=pageTitle,activeSubMenu=activeSubMenu)
        else:
            return "!Oops invalid user."
    else:
        return "!Oops you are not a valid member."
#====================================================================================
@app.route('/admin/category/edit/<int:id>', methods=['GET','POST'])
def adminCategoryEdit(id):
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            pageMetaTitle="Category Update"
            activeMenu="ManageCategories"
            activeSubMenu="ManageParentCategories"
            pageTitle="Category Update"
            categoryData=models.Categories.query.filter_by(id=id).first_or_404()
            if categoryData!=None:
                form = forms.AdminCategory()
                if request.method == "POST":
                    form = forms.AdminCategory(request.form)
                    if form.validate():
                        errorCounter=1
                        uploadedFileName=None
                        uploadedFilePath=None
                        uploadDirectoryPath="/static/uploads/"
                        if request.files!=None and  'category_logo' in request.files:
                            if allowed_image_file(request.files['category_logo'].filename):
                                # Make the filename safe, remove unsupported chars
                                uploadedFileName=uuid.uuid4().hex+'.'+request.files['category_logo'].filename.rsplit('.', 1)[1]
                                uploadedFileName = secure_filename(uploadedFileName)
                                # Move the file form the temporal folder to the upload
                                # load in server temp folder
                                request.files['category_logo'].save(os.path.join(basedir+uploadDirectoryPath, uploadedFileName))
                                uploadedFilePath="uploads/"+uploadedFileName
                                #-------------------------------------------------------
                                oldLogoName=categoryData.logo
                                categoryData.logo=uploadedFileName
                                categoryData.logo_path=uploadedFilePath
                                if oldLogoName!=None and oldLogoName!='':
                                    os.remove(os.path.join(basedir+uploadDirectoryPath, oldLogoName))
                            else:
                                errorCounter=errorCounter+1
                        if errorCounter==1:
                            categoryData.name=form.category_name.data
                            categoryData.upadted_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                            db.session.commit()
                            flash("Record has been updated successfully.", "success")
                            return redirect(url_for('adminCategoryList'))
                    else:
                        flash("Please fill all the input field", "danger")
                return render_template('Admin/category/edit.html', user=current_user, form=form,pageMetaTitle=pageMetaTitle,activeMenu=activeMenu,pageTitle=pageTitle,categoryData=categoryData,activeSubMenu=activeSubMenu)
            else:
               return "!Oops invalid request." 
        else:
            return "!Oops invalid user."
    else:
        return "!Oops you are not a valid member."
#====================================================================================
@app.route('/admin/category/change/status', methods=['POST'])   
def categoryChangeStatus():
    returnData={}
    returnData['status']='error'
    returnData['msg']='Invalid Request.'
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            if request.method == "POST":
                if request.form['action_id']:
                    statusChageData=models.Categories.query.filter_by(id=request.form['action_id']).first()
                    if statusChageData!=None: 
                        if statusChageData.status=='A':
                            statusChageData.status=None
                            statusChageData.updated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                            returnData['msg']="Record status has been changed in Dective."
                            returnData['status']='success'
                        else:
                            statusChageData.status='A'
                            statusChageData.updated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                            returnData['msg']="Record status has been changed in Active."
                            returnData['status']='success'
                        db.session.commit()
        else:
            returnData['msg']='!Oops your are not a valid member.'
    else:
        returnData['msg']='!Oops your login sessions has been expire.'
    return jsonify(returnData)
#====================================================================================
@app.route('/admin/category/delete', methods=['POST'])   
def categoryDelete():
    returnData={}
    returnData['status']='error'
    returnData['msg']='Invalid Request.'
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            if request.method == "POST":
                if request.form['action_id']:
                    statusChageData=models.Categories.query.filter_by(id=request.form['action_id']).first_or_404()
                    if statusChageData!=None and statusChageData.status!='D': 
                        statusChageData.status='D'
                        statusChageData.updated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                        returnData['msg']="Record status has been deleted successfully."
                        returnData['status']='success'
                        db.session.commit()
        else:
            returnData['msg']='!Oops your are not a valid member.'
    else:
        returnData['msg']='!Oops your login sessions has been expire.'
    return jsonify(returnData)
#====================================================================================
@app.route('/admin/subcategory/list', methods=['GET'])
def adminSubcategoryList():
    categoryList=None
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            categoryList=models.Categories.query.filter(models.Categories.parent_id!=0).order_by(models.Categories.created_at.desc(),models.Categories.name.asc()).all()
    pageMetaTitle="Manage Sub Categories"
    activeMenu="ManageCategories"
    activeSubMenu="ManageSubCategories"
    pageTitle="Sub Category List"
    return render_template('Admin/subcategory/list.html', user=current_user, categoryList=categoryList,pageMetaTitle=pageMetaTitle,activeMenu=activeMenu,pageTitle=pageTitle)
#====================================================================================
@app.route('/admin/subcategory/add', methods=['GET','POST'])
def adminSubCategoryAdd():
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            pageMetaTitle="Sub Category Add"
            activeMenu="ManageCategories"
            activeSubMenu="ManageSubCategories"
            pageTitle="Sub Category Add"
            categoryList=models.Categories.query.filter_by(parent_id=0,status='A').order_by(models.Categories.created_at.desc(),models.Categories.name.asc()).all()
            form = forms.AdminSubCategory()
            if request.method == "POST":
                form = forms.AdminSubCategory(request.form)
                if form.validate():
                    errorCounter=1
                    uploadedFileName=None
                    uploadedFilePath=None
                    uploadDirectoryPath="/static/uploads/"
                    if request.files!=None and  'category_logo' in request.files:
                        if allowed_image_file(request.files['category_logo'].filename):
                            # Make the filename safe, remove unsupported chars
                            uploadedFileName=uuid.uuid4().hex+'.'+request.files['category_logo'].filename.rsplit('.', 1)[1]
                            uploadedFileName = secure_filename(uploadedFileName)
                            # Move the file form the temporal folder to the upload
                            # load in server temp folder
                            #request.files['category_logo'].save(os.path.join(basedir+app.config['UPLOAD_TEMP_FOLDER'], uploadedFileName))
                            request.files['category_logo'].save(os.path.join(basedir+uploadDirectoryPath, uploadedFileName))
                            uploadedFilePath="uploads/"+uploadedFileName
                        else:
                            errorCounter=errorCounter+1
                    if errorCounter==1:
                        db.session.add(models.Categories(name=form.category_name.data,parent_id=form.parent_category.data,logo=uploadedFileName,logo_path=uploadedFilePath,status='A',created_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
                        db.session.commit()
                        flash("Record has been added successfully.", "success")
                        return redirect(url_for('adminSubcategoryList'))
                else:
                    flash("Please fill all the input field", "danger")
            return render_template('Admin/subcategory/add.html', user=current_user, form=form,pageMetaTitle=pageMetaTitle,activeMenu=activeMenu,pageTitle=pageTitle,categoryList=categoryList)
        else:
            return "!Oops invalid user."
    else:
        return "!Oops you are not a valid member."
#====================================================================================
@app.route('/admin/subcategory/edit/<int:id>', methods=['GET','POST'])
def adminSubCategoryEdit(id):
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            pageMetaTitle="Sub Category Update"
            activeMenu="ManageCategories"
            activeSubMenu="ManageSubCategories"
            pageTitle="Sub Category Update"
            categoryList=models.Categories.query.filter_by(parent_id=0,status='A').order_by(models.Categories.created_at.desc(),models.Categories.name.asc()).all()
            categoryData=models.Categories.query.filter_by(id=id).first_or_404()
            if categoryData!=None:
                form = forms.AdminSubCategory()
                if request.method == "POST":
                    form = forms.AdminSubCategory(request.form)
                    if form.validate():
                        errorCounter=1
                        uploadedFileName=None
                        uploadedFilePath=None
                        uploadDirectoryPath="/static/uploads/"
                        if request.files!=None and  'category_logo' in request.files:
                            if allowed_image_file(request.files['category_logo'].filename):
                                # Make the filename safe, remove unsupported chars
                                uploadedFileName=uuid.uuid4().hex+'.'+request.files['category_logo'].filename.rsplit('.', 1)[1]
                                uploadedFileName = secure_filename(uploadedFileName)
                                # Move the file form the temporal folder to the upload
                                # load in server temp folder
                                request.files['category_logo'].save(os.path.join(basedir+uploadDirectoryPath, uploadedFileName))
                                uploadedFilePath="uploads/"+uploadedFileName
                                #-------------------------------------------------------
                                oldLogoName=categoryData.logo
                                categoryData.logo=uploadedFileName
                                categoryData.logo_path=uploadedFilePath
                                if oldLogoName!=None and oldLogoName!='':
                                    os.remove(os.path.join(basedir+uploadDirectoryPath, oldLogoName))
                            else:
                                errorCounter=errorCounter+1
                        if errorCounter==1:
                            categoryData.name=form.category_name.data
                            categoryData.parent_id=form.parent_category.data
                            categoryData.upadted_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                            db.session.commit()
                            flash("Record has been updated successfully.", "success")
                            return redirect(url_for('adminSubcategoryList'))
                    else:
                        flash("Please fill all the input field", "danger")
                return render_template('Admin/subcategory/edit.html', user=current_user, form=form,pageMetaTitle=pageMetaTitle,activeMenu=activeMenu,pageTitle=pageTitle,categoryData=categoryData,categoryList=categoryList)
            else:
               return "!Oops invalid request." 
        else:
            return "!Oops invalid user."
    else:
        return "!Oops you are not a valid member."
#====================================================================================
############## Category Section [End] ############################
#---------------------------::::::::::::::-------------------------------------
#-------------------------------------------------------------------------------
############# Product Section [Start] ##############################
#====================================================================================
@app.route('/admin/product/list', methods=['GET'])
def adminProductList():
    productList=None
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            productList=models.Products.query.order_by(models.Products.created_at.desc()).all()
    pageMetaTitle="Manage Products"
    activeMenu="ManageProducts"
    pageTitle="Product List"
    return render_template('Admin/product/list.html', user=current_user, productList=productList,pageMetaTitle=pageMetaTitle,activeMenu=activeMenu,pageTitle=pageTitle)
#====================================================================================
@app.route('/admin/product/add', methods=['GET','POST'])
def adminProductAdd():
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            pageMetaTitle="Product Add"
            activeMenu="ManageProducts"
            pageTitle="Product Add"
            form = forms.AdminProduct()
            categoryList=models.Categories.query.filter_by(status='A').order_by(models.Categories.name.asc()).all()
            #try:
            if request.method == "POST":
                form = forms.AdminProduct(request.form)
                if form.validate():
                    errorCounter=1
                    uploadedFileName=None
                    uploadedFilePath=None
                    uploadedBannerFileName=None
                    uploadedBannerFilePath=None
                    uploadDirectoryPath="/static/uploads/"
                    #------------------ Default Image -----------------------------------
                    if request.files!=None and 'product_default_image' in request.files:
                        if not allowed_image_file(request.files['product_default_image'].filename):
                            form.errors['product_default_image']=[u'Please upload png, jpg, jpeg or gif image']
                            errorCounter=errorCounter+1
                        elif allowed_image_file(request.files['product_default_image'].filename):
                            # Make the filename safe, remove unsupported chars
                            uploadedFileName=uuid.uuid4().hex+'.'+request.files['product_default_image'].filename.rsplit('.', 1)[1]
                            uploadedFileName = secure_filename(uploadedFileName)
                            # upload file
                            request.files['product_default_image'].save(os.path.join(basedir+uploadDirectoryPath, uploadedFileName))
                            uploadedFilePath="uploads/"+uploadedFileName
                        else:
                            form.errors['product_default_image']=[u'Invalid image']
                            errorCounter=errorCounter+1
                    else:
                        form.errors['product_default_image']=[u'This field is required.']
                        errorCounter=errorCounter+1
                    #-------------------- banner Image -----------------------------------------
                    if request.files!=None and 'banner_image' in request.files:
                        if not allowed_image_file(request.files['banner_image'].filename):
                            form.errors['banner_image']=[u'Please upload png, jpg, jpeg or gif image']
                            errorCounter=errorCounter+1
                        elif allowed_image_file(request.files['banner_image'].filename):
                            # Make the filename safe, remove unsupported chars
                            uploadedBannerFileName=uuid.uuid4().hex+'.'+request.files['banner_image'].filename.rsplit('.', 1)[1]
                            uploadedBannerFileName = secure_filename(uploadedBannerFileName)
                            # upload file
                            request.files['banner_image'].save(os.path.join(basedir+uploadDirectoryPath, uploadedBannerFileName))
                            uploadedBannerFilePath="uploads/"+uploadedBannerFileName
                        else:
                            form.errors['banner_image']=[u'Invalid image']
                            errorCounter=errorCounter+1
                    else:
                        form.errors['banner_image']=[u'This field is required.']
                        errorCounter=errorCounter+1
                    if errorCounter==1:
                        db.session.add(
                            models.Products(
                                cat_id=form.category.data,
                                sub_cat_id=form.sub_category.data,
                                p_name=form.product_name.data,
                                p_descriptions=form.product_descriptions.data,
                                p_price=form.product_price.data,
                                p_discount_percent=form.product_discount_percent.data,
                                default_image=uploadedFileName,
                                default_image_path=uploadedFilePath,
                                created_by=current_user.get_id(),
                                status='A',
                                is_feature=form.is_feature_product.data,
                                is_banner_appear=form.is_appear_on_banner.data,
                                banner_image=uploadedBannerFileName,
                                banner_image_path=uploadedBannerFilePath,
                                created_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                            )
                        )
                        db.session.commit()
                        flash("Record has been added successfully.", "success")
                        return redirect(url_for('adminProductList'))
                    else:
                        flash("Please fill all the *field", "danger")
                else:
                    if request.files==None or 'product_default_image' not in request.files:
                        form.errors['product_default_image']=[u'This field is required.']
                    elif request.files!=None and 'product_default_image' in request.files:
                        if not allowed_image_file(request.files['product_default_image'].filename):
                            form.errors['product_default_image']=[u'Please upload png, jpg, jpeg or gif image']
                    if request.files==None or 'banner_image' not in request.files:
                        form.errors['banner_image']=[u'This field is required.']
                    elif request.files!=None and 'banner_image' in request.files:
                        if not allowed_image_file(request.files['banner_image'].filename):
                            form.errors['banner_image']=[u'Please upload png, jpg, jpeg or gif image']
                    flash("Please fill all the input field", "danger")
            #except requests.exceptions.RequestException as e:
                #return "Exception, Please realod the page."
            return render_template('Admin/product/add.html', user=current_user, form=form,pageMetaTitle=pageMetaTitle,activeMenu=activeMenu,pageTitle=pageTitle,categoryList=categoryList)
        else:
            return "!Oops invalid user."
    else:
        return "!Oops you are not a valid member."
#====================================================================================
@app.route('/admin/product/edit/<int:id>', methods=['GET','POST'])
def adminProductEdit(id):
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            pageMetaTitle="Product Update"
            activeMenu="ManageProducts"
            pageTitle="Product Update"
            form = forms.AdminProduct()
            categoryList=models.Categories.query.filter_by(status='A').order_by(models.Categories.name.asc()).all()
            productData=models.Products.query.filter_by(id=id).first_or_404()
            #try:
            if request.method == "POST":
                form = forms.AdminProduct(request.form)
                if form.validate():
                    errorCounter=1
                    uploadedFileName=None
                    uploadedFilePath=None
                    uploadDirectoryPath="/static/uploads/"
                    #-------------------- Default Image -----------------------------------------
                    if request.files!=None and 'product_default_image' in request.files:
                        if not allowed_image_file(request.files['product_default_image'].filename):
                            form.errors['product_default_image']=[u'Please upload png, jpg, jpeg or gif image']
                            errorCounter=errorCounter+1
                        elif allowed_image_file(request.files['product_default_image'].filename):
                            # Make the filename safe, remove unsupported chars
                            uploadedFileName=uuid.uuid4().hex+'.'+request.files['product_default_image'].filename.rsplit('.', 1)[1]
                            uploadedFileName = secure_filename(uploadedFileName)
                            # upload file
                            request.files['product_default_image'].save(os.path.join(basedir+uploadDirectoryPath, uploadedFileName))
                            uploadedFilePath="uploads/"+uploadedFileName
                            oldLogoName=productData.default_image
                            productData.default_image=uploadedFileName
                            productData.default_image_path=uploadedFilePath
                            if oldLogoName!=None and oldLogoName!='':
                                os.remove(os.path.join(basedir+uploadDirectoryPath, oldLogoName))
                        else:
                            form.errors['product_default_image']=[u'Invalid image']
                            errorCounter=errorCounter+1
                    #-------------------- banner Image -----------------------------------------
                    if request.files!=None and 'banner_image' in request.files:
                        if not allowed_image_file(request.files['banner_image'].filename):
                            form.errors['banner_image']=[u'Please upload png, jpg, jpeg or gif image']
                            errorCounter=errorCounter+1
                        elif allowed_image_file(request.files['banner_image'].filename):
                            # Make the filename safe, remove unsupported chars
                            uploadedBannerFileName=uuid.uuid4().hex+'.'+request.files['banner_image'].filename.rsplit('.', 1)[1]
                            uploadedBannerFileName = secure_filename(uploadedBannerFileName)
                            # upload file
                            request.files['banner_image'].save(os.path.join(basedir+uploadDirectoryPath, uploadedBannerFileName))
                            uploadedBannerFilePath="uploads/"+uploadedBannerFileName
                            productData.banner_image=uploadedBannerFileName
                            productData.banner_image_path=uploadedBannerFilePath
                        else:
                            form.errors['banner_image']=[u'Invalid image']
                            errorCounter=errorCounter+1
                    if errorCounter==1:
                        productData.cat_id=form.category.data
                        productData.sub_cat_id=form.sub_category.data
                        productData.p_name=form.product_name.data
                        productData.p_descriptions=form.product_descriptions.data
                        productData.p_price=form.product_price.data
                        productData.p_discount_percent=form.product_discount_percent.data
                        productData.is_feature=form.is_feature_product.data
                        productData.is_banner_appear=form.is_appear_on_banner.data
                        productData.updated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                        db.session.commit()
                        flash("Record has been updated successfully.", "success")
                        return redirect(url_for('adminProductList'))
                    else:
                        flash("Please fill all the *field", "danger")
                else:
                    if request.files==None or 'product_default_image' not in request.files:
                        form.errors['product_default_image']=[u'This field is required.']
                    elif request.files!=None and 'product_default_image' in request.files:
                        if not allowed_image_file(request.files['product_default_image'].filename):
                            form.errors['product_default_image']=[u'Please upload png, jpg, jpeg or gif image']
                    if request.files==None or 'banner_image' not in request.files:
                        form.errors['banner_image']=[u'This field is required.']
                    elif request.files!=None and 'banner_image' in request.files:
                        if not allowed_image_file(request.files['banner_image'].filename):
                            form.errors['banner_image']=[u'Please upload png, jpg, jpeg or gif image']
                    flash("Please fill all the input field", "danger")
            #except requests.exceptions.RequestException as e:
                #return "Exception, Please realod the page."
            return render_template('Admin/product/edit.html', user=current_user, form=form,pageMetaTitle=pageMetaTitle,activeMenu=activeMenu,pageTitle=pageTitle,categoryList=categoryList,productData=productData)
        else:
            return "!Oops invalid user."
    else:
        return "!Oops you are not a valid member."
#====================================================================================
@app.route('/admin/product/multipleimage/upload/<int:id>', methods=['POST'])
def adminProductMultipleimageUpload(id):
    returnData={}
    returnData['status']='error'
    returnData['msg']='Invalid Request.'
    returnData['fileName']='';
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            if request.method == "POST":
                productData=models.Products.query.filter_by(id=id).first()
                if productData!=None:
                    if request.form!=None and request.form.get('type')!=None:
                        if request.form['remove_file_id']!=None and request.form['remove_file_id']>0:
                            productIamge=models.ProductImages.query.filter_by(id=request.form['remove_file_id']).first()
                            if productIamge!=None:
                                db.session.delete(productIamge)
                                db.session.commit()
                                os.remove(os.path.join(basedir+'/static/uploads/', productIamge.image))
                                returnData['status']='success'
                                returnData['msg']='File has been removed successfully.'
                    else:
                        uploadedFileName=None
                        uploadedFilePath=None
                        uploadDirectoryPath="/static/uploads/"
                        if request.files!=None and 'file' in request.files:
                            if not allowed_image_file(request.files['file'].filename):
                                form.errors['file']=[u'Please upload png, jpg, jpeg or gif image']
                                errorCounter=errorCounter+1
                            elif allowed_image_file(request.files['file'].filename):
                                # Make the filename safe, remove unsupported chars
                                uploadedFileName=uuid.uuid4().hex+'.'+request.files['file'].filename.rsplit('.', 1)[1]
                                uploadedFileName = secure_filename(uploadedFileName)
                                # upload file
                                request.files['file'].save(os.path.join(basedir+uploadDirectoryPath, uploadedFileName))
                                uploadedFilePath="uploads/"+uploadedFileName
                                newIamge=models.ProductImages(
                                   p_id=productData.id,
                                   image=uploadedFileName,
                                   image_path=uploadedFilePath,
                                   type='O',
                                   created_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                                )
                                db.session.add(newIamge)
                                db.session.commit()
                                if newIamge!=None and newIamge.id!=None:
                                    returnData['status']='success'
                                    returnData['msg']='File has been upload successfully.'
                                    returnData['fileName']=uploadedFileName
                                    returnData['file_uplad_path']=uploadedFilePath
                                    returnData['fileId']=newIamge.id
                                else:
                                    os.remove(os.path.join(basedir+uploadDirectoryPath, uploadedFileName))
                                    returnData['status']='error'
                                    returnData['msg']='File is not stored in to storage.'
                            else:
                                returnData['status']='error'
                                returnData['msg']='Invalid File.'
                        else:
                            returnData['status']='error'
                            returnData['msg']='Please select a file.'   
                else:
                    returnData['status']='error'
                    returnData['msg']='Invalid request.'      
        else:
            returnData['msg']='!Oops your are not a valid member.'
    else:
        returnData['msg']='!Oops your login sessions has been expire.'
    return jsonify(returnData)
#====================================================================================
@app.route('/admin/product/changeStatus', methods=['POST'])
def adminProductChangeStatus():
    returnData={}
    returnData['status']='error'
    returnData['msg']='Invalid Request.'
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            if request.method == "POST":
                if request.form['action_id']:
                    statusChageData=models.Products.query.filter_by(id=request.form['action_id']).first()
                    if statusChageData!=None: 
                        if statusChageData.status=='A':
                            statusChageData.status=None
                            statusChageData.updated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                            returnData['msg']="Record status has been changed in Dective."
                            returnData['status']='success'
                        else:
                            statusChageData.status='A'
                            statusChageData.updated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                            returnData['msg']="Record status has been changed in Active."
                            returnData['status']='success'
                        db.session.commit()
        else:
            returnData['msg']='!Oops your are not a valid member.'
    else:
        returnData['msg']='!Oops your login sessions has been expire.'
    return jsonify(returnData)
#====================================================================================
@app.route('/admin/product/Delete', methods=['POST'])
def adminProductDelete():
    returnData={}
    returnData['status']='error'
    returnData['msg']='Invalid Request.'
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            if request.method == "POST":
                if request.form['action_id']:
                    statusChageData=models.Products.query.filter_by(id=request.form['action_id']).first_or_404()
                    if statusChageData!=None and statusChageData.status!='D': 
                        statusChageData.status='D'
                        statusChageData.updated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                        returnData['msg']="Record status has been deleted successfully."
                        returnData['status']='success'
                        db.session.commit()
        else:
            returnData['msg']='!Oops your are not a valid member.'
    else:
        returnData['msg']='!Oops your login sessions has been expire.'
    return jsonify(returnData)
#====================================================================================
################ Product Section [End] ###############################
#----------------------------::::::::::::::------------------------------------
#------------------------------------------------------------------------------
################ Color Section [Start] ###############################
#====================================================================================
@app.route('/admin/color/list', methods=['GET'])
def adminColorList():
    colorList=None
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            colorList=models.Colors.query.filter(models.Colors.status!='D').all()
    pageMetaTitle="Manage Colors"
    activeMenu="ManageColors"
    pageTitle="Color List"
    return render_template('Admin/color/list.html', user=current_user, colorList=colorList,pageMetaTitle=pageMetaTitle,activeMenu=activeMenu,pageTitle=pageTitle)
#====================================================================================
@app.route('/admin/color/add', methods=['GET','POST'])
def adminColorAdd():
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            pageMetaTitle="Color Add"
            activeMenu="ManageColors"
            pageTitle="Color Add"
            form = forms.AdminColor()
            if request.method == "POST":
                form = forms.AdminColor(request.form)
                if form.validate():
                    db.session.add(models.Colors(color_code=form.color_code.data,status='A'))
                    db.session.commit()
                    flash("Record has been added successfully.", "success")
                    return redirect(url_for('adminColorList'))
                else:
                    flash("Please fill all the input field", "danger")
            return render_template('Admin/color/add.html', user=current_user, form=form,pageMetaTitle=pageMetaTitle,activeMenu=activeMenu,pageTitle=pageTitle)
        else:
            return "!Oops invalid user."
    else:
        return "!Oops you are not a valid member."
#====================================================================================
@app.route('/admin/color/edit/<int:id>', methods=['GET','POST'])
def adminColorEdit(id):
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            pageMetaTitle="Color Update"
            activeMenu="ManageColors"
            pageTitle="Color Update"
            colorData=models.Colors.query.filter_by(id=id).first_or_404()
            if colorData!=None:
                form = forms.AdminColor()
                if request.method == "POST":
                    form = forms.AdminColor(request.form)
                    if form.validate():
                        colorData.color_code=form.color_code.data
                        #colorData.upadted_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                        db.session.commit()
                        flash("Record has been updated successfully.", "success")
                        return redirect(url_for('adminColorList'))
                    else:
                        flash("Please fill all the input field", "danger")
                return render_template('Admin/color/edit.html', user=current_user, form=form,pageMetaTitle=pageMetaTitle,activeMenu=activeMenu,pageTitle=pageTitle,colorData=colorData)
            else:
               return "!Oops invalid request." 
        else:
            return "!Oops invalid user."
    else:
        return "!Oops you are not a valid member."
#====================================================================================
@app.route('/admin/color/change/status', methods=['POST'])   
def colorChangeStatus():
    returnData={}
    returnData['status']='error'
    returnData['msg']='Invalid Request.'
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            if request.method == "POST":
                if request.form['action_id']:
                    statusChageData=models.Colors.query.filter_by(id=request.form['action_id']).first()
                    if statusChageData!=None: 
                        if statusChageData.status=='A':
                            statusChageData.status=None
                            #statusChageData.updated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                            returnData['msg']="Record status has been changed in Dective."
                            returnData['status']='success'
                        else:
                            statusChageData.status='A'
                            #statusChageData.updated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                            returnData['msg']="Record status has been changed in Active."
                            returnData['status']='success'
                        db.session.commit()
        else:
            returnData['msg']='!Oops your are not a valid member.'
    else:
        returnData['msg']='!Oops your login sessions has been expire.'
    return jsonify(returnData)
#====================================================================================
@app.route('/admin/color/delete', methods=['POST'])   
def colorDelete():
    returnData={}
    returnData['status']='error'
    returnData['msg']='Invalid Request.'
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            if request.method == "POST":
                if request.form['action_id']:
                    statusChageData=models.Colors.query.filter_by(id=request.form['action_id']).first_or_404()
                    if statusChageData!=None and statusChageData.status!='D': 
                        statusChageData.status='D'
                        #statusChageData.updated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                        returnData['msg']="Record status has been deleted successfully."
                        returnData['status']='success'
                        db.session.commit()
        else:
            returnData['msg']='!Oops your are not a valid member.'
    else:
        returnData['msg']='!Oops your login sessions has been expire.'
    return jsonify(returnData)
#====================================================================================
################ Color Section [End] ###############################
#----------------------------::::::::::::::------------------------------------
#------------------------------------------------------------------------------
################ Size Section [Start] ###############################
#====================================================================================
@app.route('/admin/size/list', methods=['GET'])
def adminSizeList():
    sizeList=None
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            sizeList=models.Sizes.query.filter(models.Colors.status!='D').all()
    pageMetaTitle="Manage Size"
    activeMenu="ManageSizes"
    pageTitle="Size List"
    return render_template('Admin/size/list.html', user=current_user, sizeList=sizeList,pageMetaTitle=pageMetaTitle,activeMenu=activeMenu,pageTitle=pageTitle)
#====================================================================================
@app.route('/admin/size/add', methods=['GET','POST'])
def adminSizeAdd():
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            pageMetaTitle="Size Add"
            activeMenu="ManageSizes"
            pageTitle="Size Add"
            form = forms.AdminSize()
            if request.method == "POST":
                form = forms.AdminSize(request.form)
                if form.validate():
                    db.session.add(models.Sizes(size_name=form.size.data,status='A'))
                    db.session.commit()
                    flash("Record has been added successfully.", "success")
                    return redirect(url_for('adminSizeList'))
                else:
                    flash("Please fill all the input field", "danger")
            return render_template('Admin/size/add.html', user=current_user, form=form,pageMetaTitle=pageMetaTitle,activeMenu=activeMenu,pageTitle=pageTitle)
        else:
            return "!Oops invalid user."
    else:
        return "!Oops you are not a valid member."
#====================================================================================
@app.route('/admin/size/edit/<int:id>', methods=['GET','POST'])
def adminSizeEdit(id):
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            pageMetaTitle="Sizes Update"
            activeMenu="ManageSizes"
            pageTitle="Sizes Update"
            sizeData=models.Sizes.query.filter_by(id=id).first_or_404()
            if sizeData!=None:
                form = forms.AdminSize()
                if request.method == "POST":
                    form = forms.AdminSize(request.form)
                    if form.validate():
                        sizeData.size_name=form.size.data
                        db.session.commit()
                        flash("Record has been updated successfully.", "success")
                        return redirect(url_for('adminSizeList'))
                    else:
                        flash("Please fill all the input field", "danger")
                return render_template('Admin/size/edit.html', user=current_user, form=form,pageMetaTitle=pageMetaTitle,activeMenu=activeMenu,pageTitle=pageTitle,sizeData=sizeData)
            else:
               return "!Oops invalid request." 
        else:
            return "!Oops invalid user."
    else:
        return "!Oops you are not a valid member."
#====================================================================================
@app.route('/admin/size/change/status', methods=['POST'])   
def adminSizeChangeStatus():
    returnData={}
    returnData['status']='error'
    returnData['msg']='Invalid Request.'
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            if request.method == "POST":
                if request.form['action_id']:
                    statusChageData=models.Sizes.query.filter_by(id=request.form['action_id']).first()
                    if statusChageData!=None: 
                        if statusChageData.status=='A':
                            statusChageData.status=None
                            #statusChageData.updated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                            returnData['msg']="Record status has been changed in Dective."
                            returnData['status']='success'
                        else:
                            statusChageData.status='A'
                            #statusChageData.updated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                            returnData['msg']="Record status has been changed in Active."
                            returnData['status']='success'
                        db.session.commit()
        else:
            returnData['msg']='!Oops your are not a valid member.'
    else:
        returnData['msg']='!Oops your login sessions has been expire.'
    return jsonify(returnData)
#====================================================================================
@app.route('/admin/size/delete', methods=['POST'])   
def adminSizeDelete():
    returnData={}
    returnData['status']='error'
    returnData['msg']='Invalid Request.'
    if current_user.is_authenticated:
        if user_type()=='sadmin':
            if request.method == "POST":
                if request.form['action_id']:
                    statusChageData=models.Sizes.query.filter_by(id=request.form['action_id']).first_or_404()
                    if statusChageData!=None and statusChageData.status!='D': 
                        statusChageData.status='D'
                        #statusChageData.updated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                        returnData['msg']="Record status has been deleted successfully."
                        returnData['status']='success'
                        db.session.commit()
        else:
            returnData['msg']='!Oops your are not a valid member.'
    else:
        returnData['msg']='!Oops your login sessions has been expire.'
    return jsonify(returnData)
#====================================================================================
################ Size Section [End] ###############################
#----------------------------::::::::::::::------------------------------------
#------------------------------------------------------------------------------

# @app.route('/api/subcagegorylist/bycatid/<int:id>', methods=['GET'])
# @json_result
# def subcagegorylistBycatid(id):
#     returnData=None
#     # returnData['status']='error'
#     # returnData['msg']='Invalid Request.'
#     # returnData['subCategoryList']=None
#     if id!=None and id>0:
#         returnData=models.Categories.query.filter_by(parent_id=id).order_by(models.Categories.name.asc()).all()
#         # returnData['status']='success'
#         # returnData['msg']='subcategorylist'
#     return jsonify(returnData)
#====================================================================================
@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404
#====================================================================================
@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File Too Large, Max upload filesize: '+str(app.config['MAX_CONTENT_LENGTH'])+' MB', 413
#====================================================================================   
def get_unread_count():
    if current_user.is_authenticated:
        return 2
#====================================================================================   
def getCategoryList():
    return models.Categories.query.filter_by(status='A',parent_id=0).order_by(models.Categories.name.asc()).all()
#====================================================================================
def authenticate_user(form):
    u = models.Users.query.filter_by(username=form.username.data).first()
    if u!=None:
        return u if bcrypt.check_password_hash(u.password, form.password.data) else None
    else:
        return None
#====================================================================================
@login_required
def user_type():
    userType=None
    if current_user.is_authenticated:
        userTypeData = models.UserTypes.query.filter_by(id=current_user.get_user_type_id()).first()
        if userTypeData !=None:
            userType=userTypeData.type.lower()
    return userType
#====================================================================================      
@app.route('/api/test')
@json_result
def api_test():
    return {"message": "My hovercraft is full of eels"}
#====================================================================================
def allowed_image_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_IMAGE_EXTENSIONS']