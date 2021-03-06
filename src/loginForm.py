# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms import validators
from models import User

from config import CONFIG
config = CONFIG

from logger import CustomLogger
cust_logger = CustomLogger(config.web_server.logger_name)


class RegistrationForm(Form):
	"""
	Class for a form used to register a user. Fields can be with non uniform case, methods must deal
	with lowering the fields if needed
	"""
	username = TextField('Username', [validators.Length(min=4, max=25)])
	email = TextField('Email', [validators.Length(min=6, max=35)])
	password = PasswordField('New password', [
		validators.Required(),
		validators.EqualTo('confirm', message='Passwords must match')
	])
	confirm = PasswordField('Confirm passeword')

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	
	def validate(self):
		"""
		Validaion of the form, checking user unicity
		:return: True if form is correct and if a user with the same email or username does not 
		already exist, False otherwise
		"""
		cust_logger.info("Trying to register new user {}".format(self.username.data))

		rv = Form.validate(self)
		if not rv:
			return False

		user = User.objects(username=self.username.data.lower()).first()
		if user is not None:
			cust_logger.info("Username already used")
			self.username.errors.append('Username already used')
			return False

		user = User.objects(email=self.email.data.lower()).first()
		if user is not None:
			cust_logger.info("Email already used".format())
			self.email.errors.append('Email already used')
			return False
		return True


class LoginForm(Form):
	"""
	Class for a form to log a user. Fields can be with non-uniform case. Handle password validation
	"""
	username = TextField('Username', [validators.Required()])
	password = PasswordField('Password', [validators.Required()])

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.user = None

	def validate(self):
		"""
		Validaion of the form, checking user password hash with stored one.
		:return: True if the form is correct and the user as given correct credentials, 
		False otherwise
		"""
		cust_logger.info("Trying to validate form")

		rv = Form.validate(self)
		if not rv:
			return False

		user = User.objects(username=self.username.data.lower()).first()
		if user is None:
			cust_logger.info("Invalid username entered")
			self.password.errors.append('Unknown username or password')
			return False

		if not user.check_password(self.password.data):
			cust_logger.info("Invalid password entered")
			self.password.errors.append('Unknown username or password')
			return False

		self.user = user
		return True