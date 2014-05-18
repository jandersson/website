#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2
import re

from google.appengine.ext import db

jinja_environment = jinja2.Environment(autoescape=True,
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

workout_form = """
<html>
	<head>
	</head>
	<body>
		<form action="/workout_submit">
			<label>
				Plank Time:
				<input name="plank">
			</label>

			<label>
				Leg Raises:
				<input name="leg raises">
			</label>

			<label>
				Pushups:
				<input name="pushups">
			</label>

			<input type="submit">
		</form>
	</body>
</html>
"""

workout_stats_form = """
<html>
	<head>
	</head>
	<body>
		<p>Plank: %(plank)s </p>
		<p>Leg Raises: %(leg_raises)s </p>
	</body>
</html>
"""

rot13_form="""
<html>
<head>
	<link type ="text/css" rel ="stylesheet" href="/stylesheets/main.css" />
</head>
<body>
<form method = "post">

ROT13 Generator:

<br>

Enter some text below

<br>

<textarea name = "text">
%(cyphertext)s
</textarea>

<br>

<input type = "submit">

</form>
<br>

<a href = '/'>Home</a>
</body>
</html>
"""

signup_form = """
<html>
	<head>
		<link type ="text/css" rel ="stylesheet" href="/stylesheets/main.css" />
	</head>
	<body>
		<form method = "post">

			Want to sign up?

			<br>
			<label>
			Username
			<input type = "text" name = "username" value="%(username)s">
			%(username_error)s
			</label>
			
			<br>
			<label>
			Password 
			<input type = "password" name = "password">
			%(password_error)s
			</label>
			
			<br>
			<label>
			Verify Password 
			<input type = "password" name = "verify">
			%(verify_error)s
			</label>

			<br>
			<label>
			Email (optional) 
			<input type = "text" name = "email", value="%(email)s">
			%(email_error)s
			</label>
			<br>

			<input type = "submit">
		</form>

		<br>

		<a href = '/'>Home</a>
	</body>
</html>
"""

class Handler(webapp2.RequestHandler):
	"""
	Functions taken from Udacity Web Development course
	"""
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_environment.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(webapp2.RequestHandler):
    def get(self):
    	template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render())

    def post(self):
    	self.response.out.write("Thanks! That's a totally valid day!")

class AsciiChandler(Handler):
	def render_front(self, title="", art="", error=""):
		self.render("asciichan.html", title=title, art=art, error=error)
	def get(self):
		self.render_front()
	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")

		if title and art:
			self.write("thanks!")
		else:
			error = "You need to fill out both fields"
			self.render_front(title=title, art=art, error=error)
class FizzBuzz(Handler):
	def get(self):
		n = self.request.get("n", 0)
		n = n and int(n)
		self.render("fizzbuzz.html", n = n)

class Workout(webapp2.RequestHandler):
	def get(self):
		self.response.out.write(workout_form)

class WorkoutStats(webapp2.RequestHandler):
	def get(self):
		plank = self.request.get("plank")
		leg_raises = self.request.get("leg raises")
		pushups = self.request.get("pushups")
		self.response.out.write(plank)

class ROT13(webapp2.RequestHandler):
	def write_form(self, cyphertext = ""):
		self.response.out.write(rot13_form % {'cyphertext':cyphertext})
	def get(self):
		self.write_form()
	def post(self):
		user_text = self.request.get("text")
		cyphertext = make_rot13(user_text)
		cyphertext = escape_html(cyphertext)
		self.write_form(cyphertext)

class TestPage(Handler):
	def get(self):
		self.render("shopping_list.html")

class Welcome(webapp2.RequestHandler):
	def get(self):
		username = self.request.get("username")
		self.response.out.write("Welcome " + username)

class Signup(webapp2.RequestHandler):
	def write_form(self, form, username_error = "", password_error = "", email_error = "",
	verify_error = "", username = "", email = ""):
		self.response.out.write(form % {'username_error':username_error,
										'password_error':password_error,
										'email_error':email_error,
										'verify_error':verify_error,
										'email':email,
										'username':username})

	def validate_username(self, username):
		user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		return user_re.match(username)

	def validate_email(self, email):
		email_re = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
		return email_re.match(email)

	def validate_password(self, password):
		password_re = re.compile(r"^.{3,20}$")
		return password_re.match(password)

	def validate_verify(self, password, verify):
		if password == verify:
			return True
		else:
			return None

	def get(self):
		self.write_form(signup_form)
	def post(self):
		user_username = self.request.get("username")
		user_password = self.request.get("password")
		user_verify = self.request.get("verify")
		user_email = self.request.get("email")

		valid_username = self.validate_username(user_username)
		username_error = ""
		if user_email:
			valid_email = self.validate_email(user_email)
		else:
			valid_email = True
		email_error = ""
		valid_password = self.validate_password(user_password)
		password_error = ""
		valid_verify = self.validate_verify(user_password,user_verify)
		verify_error = ""

		errors = False
		if not valid_username:
			username_error = "Thats not a valid username"
			errors = True
		if not valid_email:
			email_error = "Never seen an email like that before"
			errors = True
		if not valid_password:
			password_error = "You'll have to do better than that"
			errors = True
		if not valid_verify:
			verify_error = "Your passwords don't match"
			errors = True
		if not errors:
			self.redirect('/welcome?' + "username=" + user_username)
		else:
			self.write_form(signup_form, username_error, password_error, email_error, verify_error, username = user_username, email = user_email)



def make_rot13(s):
	cypher = ''
	alphabet = {'a': 'n',
				'b': 'o',
				'c': 'p',
				'd': 'q',
				'e': 'r',
				'f': 's',
				'g': 't',
				'h': 'u',
				'i': 'v',
				'j': 'w',
				'k': 'x',
				'l': 'y',
				'm': 'z',
				'n': 'a',
				'o': 'b',
				'p': 'c',
				'q': 'd',
				'r': 'e',
				's': 'f',
				't': 'g',
				'u': 'h',
				'v': 'i',
				'w': 'j',
				'x': 'k',
				'y': 'l',
				'z': 'm'}
	for letter in s:
		if letter in alphabet:
			cypher = cypher + alphabet[letter]
		elif letter.lower() in alphabet:
			cypher = cypher + alphabet[letter.lower()].upper()
		else:
			cypher = cypher + letter
	return cypher

def escape_html(s):
    escapes = [["&","&amp;"],
    		   ["<","&lt;"],
    		   [">","&gt;"],
    		   ['"',"&quot;"]]
    for char in escapes:
        s = s.replace(char[0], char[1])
    return s

class ShoppingListHandler(Handler):
	def get(self):
		items = self.request.get_all("food")
		self.render("shopping_list.html", items = items)
		
class About(webapp2.RequestHandler):
    def get(self):
    	template = jinja_environment.get_template('about.html')
        self.response.out.write(template.render())
		
app = webapp2.WSGIApplication([('/', MainPage), 
							   ('/ROT13', ROT13),
							   ('/Signup', Signup),
							   ('/About', About),
							   ('/workout', Workout),
							   ('/workout_submit', WorkoutStats),
							   ('/welcome', Welcome),
							   ('/testpage',TestPage),
							   ('/fizzbuzz',FizzBuzz),
							   ('/shoppinglist',ShoppingListHandler),
							   ('/asciichan', AsciiChandler)]
							   , debug=True)




