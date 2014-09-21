import sys
import time
import traceback

from browser import document
from javascript import JSObject, console

class Editor:
  def __init__(self, tab_container='tt'):
      self._editors={}
      self._tabcount=0
      self._tab_container='\#%s' % tab_container
      self._jquery=JSObject(jQuery)

      self._jquery(self._tab_container).tabs()

  def add_editor(self, filename=None, content=""):
      if filename is None:
         filename = "Untitled-%s" % self._tabcount
         self._tabcount+=1

      #_content='<pre id="%s" class="editclass">%s</pre>'
      _content='<pre id="%s" class="editclass" style="width:100%%;height:100%%">%s</pre>'
      self._jquery(self._tab_container).tabs('add',
        {'title': filename,
         'content': _content % (filename, content), 
         'closable': True
        })

      #add ace editor to filename pre tag
      _editor=JSObject(ace).edit(filename)
      _session=_editor.getSession()
      _session.setMode("ace/mode/python")
      _editor.setTheme("ace/theme/crimson_editor")
      _session.setMode("ace/mode/python")
      #_session.setUseWrapMode(true)
      _session.setTabSize(4)

      _editor.focus()

      self._editors[filename]=_editor

      #set resize
      document[filename].bind('resize', lambda x: self._editors[filename].resize(True))

  def _currentTabName(self):
      _tab=self._jquery(self._tab_container).tabs('getSelected')
      return _tab.panel('options').title
      #_tab=_tab.panel('options').tab
      #console.log(_tab[0])
      #_title=_tab[0].innerText

      #return _title

  def getCurrentText(self):
      _title=self._currentTabName()
      return self._editors[_title].getValue()

  # load a Python script
  def load_filename(self, filename):
      #need to load file from google drive..
      self._add_editor(filename, "this is the contents for %s" % filename)

  def clearCurrentText(self):
      _title=self._currentTabName()

      return self._editors[_title].setValue('')

def write(data):
    document["myconsole"].value += '%s' % data

sys.stdout.write = write
sys.stderr.write = write
