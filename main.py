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

jinja_environment = jinja2.Environment(autoescape=True,
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

about_form ="""
<html>
	<head>
		<link type ="text/css" rel ="stylesheet" href="/stylesheets/main.css" />	
	</head>
<body>
<nav>
<ul>
<li><a href = '/'>Home</a></li>
<li><a href = '/About'>About</a></li>
<li><a href = '/'>Contact</a></li>
</ul>
</nav>
<article>
<br>
<br>
<a href='/ROT13'>ROT13 Generator</a>
<br>
<a href='/Signup'>Signup Page</a>
</article>
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

Username <input type = "text" name = "username">

<br>

Password <input type = "password" name = "password">

<br>

Verify Password <input type = "password" name = "verify">

<br>

Email (optional) <input type = "text" name = "email">

<br>

<input type = "submit">
</form>

<br>

<a href = '/'>Home</a>
</body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
    	template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render())

    def post(self):
    	self.response.out.write("Thanks! That's a totally valid day!")

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

class Signup(webapp2.RequestHandler):
	def get(self):
		self.response.out.write(signup_form)
	def post(self):
		self.response.out.write("Thanks for the totally valid input")

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

def valid_username(username):
	return True
		
class About(webapp2.RequestHandler):
    def get(self):
        self.response.write(about_form)	
		

app = webapp2.WSGIApplication([('/', MainPage), 
							   ('/ROT13', ROT13),
							   ('/Signup', Signup),
							   ('/About', About)]
							   , debug=True)




