from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

# Datatypes and functions that will actually show up in the database
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Text

# Check to see if key combinations are already being used
from sqlalchemy.sql import exists

# Hotkey tool
import pyhk

# Windows tool to copy to clipboard
import pyperclip


'''
Make a database in the cwd if it doesn't already exist
'''
engine = create_engine('sqlite:///C:\\Users\\ScionOfTheVoid\\Documents\\chat_spammer\\quips.db', echo = True)
Base = declarative_base()

# Many-to-many associative table for Apps/Categories
app_cat_table = Table('app_cat_table', Base.metadata,
	Column('id', Integer, primary_key = True),
	Column('app_id', Integer, ForeignKey('apps.id')),
	Column('cat_id', Integer, ForeignKey('categories.id'))
)

# Table to store all quips
# Bind categories to these (one-to-many)
class Quips(Base):
	
	__tablename__ = "quips"
	
	id = Column(Integer, primary_key = True)
	quip_text = Column(String)
	keybinding = Column(String)
	
	# Relational structure for categories
	quip_category = Column(Integer, ForeignKey('categories.id'))
	
	# param'text' is the quip itself
	# param'key' must be a list; take it and make a string with spaces separating each element
	def __init__(self, text, key):
		self.quip_text = text
		self.keybinding = " ".join(key)
	
	def __repr__(self):
		return '<Quip(%r) bound to [%r]>' % (self.quip_text, self.keybinding)

# Table listing all categories
# Bind quips to these (one-to-many)
# Bind applications to these (many-to-many)
class Categories(Base):
	
	__tablename__ = "categories"
	
	id = Column(Integer, primary_key = True)
	cat_name = Column(String)
	
	# Relational structure for quips; this is the parent
	contains_quips = relationship("Quips")
	
	# Relational structure for apps not needed because this is the child
	
	def __init__(self, name):
		self.cat_name = name
	
	def __repr__(self):
		return '<Category %r>' % self.cat_name

# Table listing all applications
# Bind categories to these (many-to-many)
class Apps(Base):
	
	__tablename__ = "apps"
	
	id = Column(Integer, primary_key = True)
	app_name = Column(String)
	app_description = Column(Text)
	
	# Relational structure for categories
	useable_cat = relationship('Categories', secondary = lambda: app_cat_table)
	
	def __init__(self, name):
		self.app_name = name
	
	def __repr__(self):
		return '<App %r>' % self.app_name

# Table listing hotkeys for global utilities
class Utility(Base):
	
	__tablename__ = "utility"
	
	id = Column(Integer, primary_key = True)
	description = Column(String)
	keybinding = Column(String)
	
	# param'text' is a description of what this keybinding will do
	# param'key' must be a list; take it and make a string with spaces separating each element
	def __init__(self, text, key):
		self.description = text
		self.keybinding = " ".join(key)
	
	def __repr__(self):
		return '<Utility(%r) bound to [%r]>' % (self.description, self.keybinding)

# Initial commit to write tables
# Fails if tables already created
Base.metadata.create_all(engine)
'''
End of database definition
'''


'''
Helper class
Accesses a database of phrases by keyword
Performs insert into/delete from database operations

Library always starts in access mode

WARNING: NEVER MAKE TWO LIBRARY OBJECTS SIMULTANEOUSLY!!
'''
class Library(object):
	
	# Initialize the library by supplying 1 argument; the other should always be default
	def __init__(self, starting_app, hotkey_tool = None):
		# Use a temporary dictionary to store quips
		# Load a new dictionary every time you switch apps or modes
		# Reload hotkeys every time you switch categories
		# First entry in dictionary is the name of the app; default is "Edit" for edit mode
		self.lib = {}
		self.lib['current_app'] = starting_app
		# Keep track of the category using "pages"
		self.page = 0
		
		# Hotkey object from pyhk
		self.hk = hotkey_tool
		
		# Success flag for insert/delete
		self.success = False
		
		# Load a library of chat commands
		# Make sessions using self.Session() only when needed; close immediately after use
		self.Session = sessionmaker(bind = engine)
		
		if self.hk == None:
			print "Need a hotkey tool... load library manually after providing one"
		else:
			self.load_lib()
	
	# Load the library from the database
	# Accepts hotkey tool as input
	# Note that utilities are always loaded
	def load_lib(self):
		if self.hk == None or self.output == False:
			return "Failed to load library"
		
		self.hk.removeHotkey()
		session = self.Session()
		
		app = session.query(Apps).filter(Apps.app_name == self.lib['current_app']).first()
		self.lib["Categories"] = []
		for c in app.useable_cat:
			self.lib["Categories"].append([cat.cat_id, cat.cat_name, None])
		
		# Default is always the first category loaded
		# Make sub-dictionary
		self.lib["Categories"][self.page][2] = []
		
		# Numerical index
		count = 0
		
		# Get all quips that fall under the given category and add them to the dictionary
		# In addition, immediately bind hotkeys
		for q in session.query(Quips).filter(Quips.quip_category == cat_data[0]).all():
			self.lib["Categories"][self.page][2].append(q.quip_text)
			self.hk.addHotkey(q.keybinding.split(" "), pyperclip.copy(self.lib["Categories"][self.page][2][count]))
			
			# Increment count
			count += 1
		
		session.close()
		
		# Set a hotkey to end the program
		self.hk.setEndHotkey(['F12'])
		
		return "Dictionary loaded"
	
	# Helper function to check if a key combination is already being used
	# Key combinations can only be reused across different categories
	# Use private only
	def keys_in_use(self, session, keys, cat_id):
		key_string = " ".join(keys)
		
		# Check for utilities if no cat_name is given
		if cat_id == -1:
			return session.query(exists().where(Utility.keybinding == key_string)).scalar()
		else:
			return session.query(exists().where(Quips.keybinding == key_string, Quips.quip_category == cat_id)).scalar()
	
	# Helper function to check if quip already exists in the database
	# Use private only
	def quip_exists(self, session, quip_text):
		return session.query(exists().where(Quips.quip_text == quip_string)).scalar()
	
	# Helper function to check if category already exists in the database
	# Use private only
	def cat_exists(self, session, cat_name):
		return session.query(exists().where(Categories.cat_name == cat_name)).scalar()
	
	# Helper function to check if app is already registered in the database
	# Use private only
	def app_exists(self, session, app_name):
		return session.query(exists().where(Apps.app_name == app_name)).scalar()
	
	# Write a new line to the library
	# Only accepts keys as a list
	def add_quip(self, quip, keys, cat_name):
		msg = ""
		
		# Try to insert the quip
		if type(keys) == list:
			if len(keys) > 0:
				session = self.Session()
				
				try:
					
					cat = session.query(Categories).filter(Categories.cat_name == cat_name).first()
					
					# Failure if category does not yet exist or if key combination is in use
					if cat == None or self.keys_in_use(session, keys, cat.id) == True or self.quip_exists(session, quip) == True:
						self.success = False
						msg = "Impossible to insert this quip"
					else:
						new_quip = Quips(quip, keys)
						session.add(new_quip)
						
						# Add category relationship
						cat.contains_quips.append(quip)
						
						self.success = True
					
				except:
					
					session.rollback()
					self.success = False
					raise
				
				finally:
					
					if self.success == True:
						session.commit()
						self.success = False
						msg = "Added '%s' under '%s'" % (quip, cat_name)
					elif msg == "" and success == False:
						msg = "Failed to add '%s' under '%s'" % (quip, cat_name)
					else:
						pass
					
					# Close when done
					session.close()
					
			else:
				msg = "Must have key bindings; failed to add '%s' under '%s'" % (quip, cat_name)
		
		else:
			msg = "Keys must be in list format; failed to add '%s' under '%s'" % (quip, cat_name)
		
		# Report
		return msg
	
	# Add a new category
	def add_cat(self, cat_name):
		session = self.Session()
		msg = ""
		
		try:
			
			if self.cat_exists(session, cat_name) == True:
				msg = "This category is already in the database"
				self.success = False
			else:
				new_cat = Categories(cat_name)
				session.add(new_cat)
				self.success = True
			
		except:
			
			session.rollback()
			self.success = False
			raise
			
		finally:
			
			if self.success == True:
				session.commit()
				self.success = False
				msg = "Added a new category '%s'" % cat_name
			elif msg == "" and success == False:
				msg = "Failed to add the category '%s'" % cat_name
			else:
				pass
			
			# Close when done
			session.close()
			
			# Report
			return msg
	
	# Associate a new app with this program
	def add_app(self, app_name):
		session = self.Session()
		msg = ""
		
		try:
			
			if self.app_exists(session, app_name) == True:
				msg = "This app is already in the database"
				self.success = False
			else:
				new_app = Apps(app_name)
				session.add(new_app)
				self.success = True
			
		except:
			
			session.rollback()
			self.success = False
			raise
			
		finally:
			
			if self.success == True:
				session.commit()
				self.success = False
				msg = "Added a new app '%s'" % app_name
			elif msg == "" and success == False:
				msg = "Failed to add the app '%s'" % app_name
			else:
				pass
			
			# Close when done
			session.close()
			
			# Report
			return msg 
	
	# Associate a category with an app
	def add_cat_to_app(self, app_name, cat_name):
		session = self.Session()
		msg = ""
		
		try:
			
			# Can add app to category only if both already exist
			if self.app_exists(session, app_name) == True and self.cat_exists(session, cat_name) == True:
				cat = session.query(Categories).filter(Categories.cat_name == cat_name).first()
				app = session.query(Apps).filter(Apps.app_name == app_name).first()
				
				app.useable_cat.append(cat)
				
				self.success = True
			else:
				self.success = False
			
		except:
			
			session.rollback()
			self.success = False
			raise
			
		finally:
			
			if self.success == True:
				session.commit()
				self.success = False
				msg = "Associated '%s' with '%s'" % (app_name, cat_name)
			else:
				msg = "Failed to associate '%s' with '%s'" % (app_name, cat_name)
			
			# Close when done
			session.close()
			
			# Report
			return msg
	
	# Change the key bindings on anything
	def change_key(self, old_binding, new_binding):
		session = self.Session()
		msg = ""
		quip = None
		
		try:
			# Need the name of the current category to perform keys_in_use() check
			if session.query(exists().where(Quips.keybinding == old_string)).scalar():
				quip = session.query(Quips).filter(Quips.keybinding == old_string).first()
			
			# Can change keys only if they were being used in the first place and new key combination is unused
			if self.keys_in_use(session, old_binding, quip.quip_category) == True and self.keys_in_use(session, new_binding, quip.quip_category) == False:
				old_string = " ".join(old_binding)
				new_string = " ".join(new_binding)
				
				if quip == None:
					session.query(Utility).filter(Utility.keybinding == old_string).update({'keybinding': new_string})
				else:
					session.query(Quips).filter(Quips.keybinding == old_string).update({'keybinding': new_string})
				
				self.success = True
			else:
				msg = "Either the old key combination provided is not in use or the new key combination provided is already in use"
				self.success = False
				
		except:
			
			session.rollback()
			self.success = False
			raise
			
		finally:
			
			if self.success == True:
				session.commit()
				self.success = False
				msg = "Keybinding change successful"
			elif msg == "" and self.success == False:
				msg = "Keybinding change failed"
			else:
				pass
			
			# Close when done
			session.close()
			
			# Report
			return msg
	
	# Switch between apps
	def app_switch(self, starting_app, hotkey_tool = None):
		if hotkey_tool == None:
			return "Need a hotkey tool to switch between apps or out of edit mode"
		
		self.lib = {}
		self.lib['current_app'] = starting_app
		
		# Reload
		self.load_lib(hotkey_tool)
		
		return "Now using '%s'" % starting_app
	
	# Switch active category
	def cat_switch(self, cat_name, inc_page):
		self.page += inc_page
		
		# Reset hotkey tool
		self.hk.removeHotkey()
		session = self.Session()
		
		# Follow the same load procedure as in load_lib
		self.lib["Categories"][self.page][2] = []
		
		# Numerical index
		count = 0
		
		# Get all quips that fall under the given category and add them to the dictionary
		# In addition, immediately bind hotkeys
		for q in session.query(Quips).filter(Quips.quip_category == cat_data[0]).all():
			self.lib["Categories"][self.page][2].append(q.quip_text)
			self.hk.addHotkey(q.keybinding.split(" "), pyperclip.copy(self.lib["Categories"][self.page][2][count]))
			
			# Increment count
			count += 1
		
		session.close()
		
		# Set a hotkey to end the program
		self.hk.setEndHotkey(['F12'])
		
		return "Now using Category(%s)" % self.lib["Categories"][self.page][1]
	
	# Start spamming!
	def go(self):
		self.hk.start()
		return "Engine started. Press keys and start spamming!"
'''
End of helper class definition
'''