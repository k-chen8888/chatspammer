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
	
	def __init__(self, starting_app = None, parent = None):
		super(MainWindow, self).__init__(parent)
		self.setWindowTitle("Chat Spammer")
		
		# Initialize library (not ready for testing)
		#self.lib = qdb.Library(starting_app, pyhk.pyhk())
		
		# Make the tab area
		self.tab = Tab(self)
		self.tab.addTab(QWidget(), "Main")
		self.tab.addTab(QWidget(), "Main2")
		self.tab.show()
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
class TabContent():
	pass
'''
End of Tab Content definition
'''


'''
Run as main for testing only
'''
if __name__ == '__main__':
	# Create Qt application and the QDeclarative view
	app = QApplication(sys.argv)
	window = MainWindow("MOBA")
	window.show()
	
	# Enter Qt main loop
	sys.exit(app.exec_())
'''
End testing area
'''