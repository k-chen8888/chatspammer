import sys

# Pyside imports
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import QDeclarativeView

# Spammer imports
import quip_db as qdb

# Hotkey tool
import pyhk


'''
Main window
Put everything else in tabs
'''
class MainWindow(QDeclarativeView):
	
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)
		self.setWindowTitle("Chat Spammer")
		
		# Set window size
		self.resize(1000, 750)
		
		# Library
		self.lib = None
		
		# Make the tab area
		self.tab = Tab(self)
		
		tempw = QWidget()
		templ = QGridLayout()
		print templ.rowCount()
		print templ.columnCount()
		tempw.setLayout(templ)
		templ.addWidget(QLineEdit())
		self.tab.addTab(tempw, "Main")
		
		# Display when done loading
		self.tab.show()
	
	# Switches between selected apps
	# Starts up the library if there was no previously selected app
	def select_app(self, starting_app):
		if self.lib == None:
			self.lib = qdb.Library(starting_app, pyhk.pyhk())
		else:
			self.lib.app_switch(starting_app, self.lib.hk)
'''
End of MainWindow definition
'''


'''
Containers for all tabs
Single tab for each category
'''
class Tab(QTabWidget):
	
	def __init__(self, parent = None):
		super(Tab, self).__init__(parent)
		
		# Arrange things in a grid
		self.content = QGridLayout(self)
		
		self.resize(900, 700)
'''
End of Tab definition
'''


'''
Dialog boxes for tab contents

Existing quips: Contains a textbox for the text and a textbox for keystrokes
	Make a new one for each quip found in the database
New quip: Contains a single empty textbox for text input and a single empty textbox for keystroke input
	Make one of these after all quips are loaded
'''
class TabContent(QRect):
	
	def __init__(self, parent = None):
		super(TabContent, self).__init__(parent)
		
		# Set dimensions
		self.setWidth(200)
		self.setHeight(200)
'''
End of Tab Content definition
'''


'''
Run as main for testing only
'''
if __name__ == '__main__':
	# Create Qt application and the QDeclarative view
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	
	# Initialize library (not ready for testing)
	#window.select_app("MOBA")
	
	# Enter Qt main loop
	sys.exit(app.exec_())
'''
End testing area
'''