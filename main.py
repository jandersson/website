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

class Art(db.Model):
	title = db.StringProperty(required = True)
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class AsciiChandler(Handler):
	def render_front(self, title="", art="", error=""):
		arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
		self.render("asciichan.html", title=title, art=art, error=error, arts=arts)
		
	def get(self):
		self.render_front()

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")

		if title and art:
			a = Art(title = title, art = art)
			a.put()
			self.redirect("/asciichan")
		else:
			error = "You need to fill out both fields"
			self.render_front(title=title, art=art, error=error)

class FizzBuzz(Handler):
	def get(self):
		n = self.request.get("n", 0)
		n = n and int(n)
		self.render("fizzbuzz.html", n = n)

class Workout(Handler):
	def get(self):
		self.render("workout.html")
	def post(self):
		plank = self.request.get("plank")
		leg_raises = self.request.get("leg raises")
		pushups = self.request.get("pushups")
		self.response.out.write(plank)		

class ROT13(Handler):

	def get(self):
		self.render("rot13.html")

	def post(self):
		user_text = self.request.get("text")
		cyphertext = self.make_rot13(user_text)
		#cyphertext = self.escape_html(cyphertext)
		self.render("rot13.html", cyphertext=cyphertext)
	
	def escape_html(self, s):
	    escapes = [["&","&amp;"],
	    		   ["<","&lt;"],
	    		   [">","&gt;"],
	    		   ['"',"&quot;"]]
	    for char in escapes:
	        s = s.replace(char[0], char[1])
	    return s

	def make_rot13(self, s):
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

class Post(db.Model):
	title = db.StringProperty(required = True)
	entry = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class BlogPostHandler(Handler):
	def render_front(self, title="", entry="", title_error="", entry_error=""):
		self.render("newpost.html", title=title, entry=entry, title_error=title_error, entry_error=entry_error)

	def get(self):
		self.render_front()

	def post(self):
		title = self.request.get("title")
		entry = self.request.get("entry")
		errors = False
		title_error=""
		entry_error=""
		if not title:
			errors = True
			title_error = "You need a title."

		if not entry:
			errors = True
			entry_error = "Cant be postin' without some content"

		if title and entry:
			new_post = Post(title=title, entry=entry)
			new_post.put()
			self.redirect("/blog")
		else:
			self.render_front(title=title, entry=entry, title_error=title_error, entry_error=entry_error)

class BlogHandler(Handler):
	def render_front(self, title="", entry="", title_error="", entry_error=""):
		posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
		self.render("blog.html", title=title, entry=entry, title_error=title_error, posts=posts, entry_error=entry_error)
	
	def get(self):
		self.render_front()

	def post(self):
		pass


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
							   ('/welcome', Welcome),
							   ('/testpage',TestPage),
							   ('/fizzbuzz',FizzBuzz),
							   ('/shoppinglist',ShoppingListHandler),
							   ('/asciichan', AsciiChandler),
							   ('/blog', BlogHandler),
							   ('/blog/newpost', BlogPostHandler)
							   ], debug=True)




