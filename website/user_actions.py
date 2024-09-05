from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user


import base64
import imghdr
import random
from datetime import datetime, timedelta
import datetime as dt

from . import DateToolKit as dtk
from .db import db
from .db import dbORM
from . import encrypt
from . import ScreenGoRoute
from . import function_pool
from . import id_generator

user_actions = Blueprint('user_actions', __name__)
ua = user_actions

@ua.route("/api/fspace-backend/login", method=['POST'])
def validateLogin():
	# Collecting the posted data
	email_reg_username = request.form['email_reg_username']
	password = request.form['password']

	# Checking what the user is using to authenticate, email, reg_number, or username?
	if "@" in email_reg_username and ".com" in email_reg_username:
		ERU = "email"

	elif ("2019" in email_reg_username and len(email_reg_username) == 11) or ("2020" in email_reg_username and len(email_reg_username) == 11) or ("2021" in email_reg_username and len(email_reg_username) == 11) or ("2022" in email_reg_username and len(email_reg_username) == 11) or ("2023" in email_reg_username and len(email_reg_username) == 11) or ("2024" in email_reg_username and len(email_reg_username) == 11):
		ERU = "reg_number"
	else:
		ERU = "username"

	# Validating the User
	try:	
		User = dbORM.get_all("UserSICT")[f'{dbORM.find_one("UserSICT", ERU, email_reg_username)}']
		if check_password_hash(User['password'], password):
			return function_pool.returnJSONData("success", User)
		else:
			pass
		
	except:
		return function_pool.returnJSONData("failed", "Email, Username, Reg Number or password incorrect")
	
	
@ua.route("/api/fspace-backend/signup", method=['POST'])
def registerUser():
	# Collecting the posted data
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	reg_number= request.form['reg_number']
	dob = request.form['dob']
	department = request.form['department']
	faculty = request.form['faculty']
	email = request.form['email']
	password = request.form['password']

	user_with_email = dbORM.find_one("UserSICT", "email", email)
	user_with_reg_number = dbORM.find_one("UserSICT", "reg_number", reg_number)

	if user_with_email:
		return function_pool.returnJSONData("failed", "Email is already taken")
	elif user_with_reg_number:
		return function_pool.returnJSONData("failed", "Reg number has already been registered")
	elif len(first_name) < 2 or len(last_name) < 2:
		return function_pool.returnJSONData("failed", "Name must be at least 2 characters long.")
	elif len(email) < 4:
		return function_pool.returnJSONData("failed", "Email must be at least 4 characters long.")
	elif len(reg_number) < 11:
		return function_pool.returnJSONData("failed", "Reg Number must be at least 11 characters long.")
	
	else:
		new_user = {
			"first_name": first_name,
			"last_name": last_name,
			"reg_number": reg_number,
			"dob": dob,
			"department": department,
			"faculty": faculty,
			"email": email,
			"password": password
		}
		dbORM.add_entry("UserSICT", encrypt.encrypter(str(new_user)))
		
		User = dbORM.get_all("UserSICT")[f'{dbORM.find_one("UserSICT", "email", email)}']
		return function_pool.returnJSONData("success", User)

	

	

	
	
	
	