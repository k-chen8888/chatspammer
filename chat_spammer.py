# Import for library
import spammer_gui as gui

# Import for database and library
import quip_db as qdb


'''
Main part of app
Performs setup operations
Makes a chat spammer that listens for keystrokes, then digs into library to find correct quip to put into Windows clipboard
'''
# Initialize library
spammer = qdb.Library("MOBA", pyhk.pyhk())
'''
End of setup section
'''

'''
Start spamming comments! Use hotkeys to place text into Windows' clipboard
'''
spammer.go()