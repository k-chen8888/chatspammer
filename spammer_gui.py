import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import QDeclarativeView

'''
Main window
Use sub-windows for separate tasks
'''
class MainWindow(QDeclarativeView):
	
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)
		self.setWindowTitle("Chat Spammer")
		
		# Render the .qml file for the view
		self.setSource(QUrl.fromLocalFile("spammer_view.qml"))
		
		# Resize QML window with outer window
		self.setResizeMode(QDeclarativeView.SizeRootObjectToView)
'''
End of MainWindow definition
'''

 
'''
Run as main for testing only
'''
if __name__ == '__main__':
	# Create Qt application and the QDeclarative view
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	
	# Enter Qt main loop
	sys.exit(app.exec_())
'''
End testing area
'''