import sublime, sublime_plugin

class CloseTagOnSlashCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, self.view.sel()[0].begin(), '/')
		before = self.view.substr(sublime.Region(0, self.view.sel()[0].begin()))
		if '<' == before[-2]:
			before = self.removeComments(before[0:-2])
			tag = None
			while (tag is None) and (before is not None):
				before, after = self.splitOnNearestClosedTag(before)
				tag = self.nearestUnclosedTag(after)
			if tag is not None:
				self.view.insert(edit, self.view.sel()[0].begin(), tag + '>')

	def removeComments(self, string):
		commentStart = string.find('<!--')
		while -1 != commentStart:
			commentEnd = string.find('-->', commentStart + 4)
			if -1 == commentEnd:
				return string
			string = string[0:commentStart] + string[commentEnd + 3:]
			commentStart = string.find('<!--')
		return string

	def splitOnNearestClosedTag(self, after):
		before = None
		closeStart = after.rfind('</')
		if -1 != closeStart:
			closeEnd = after.find('>', closeStart + 2)
			if -1 != closeEnd:
				tag = after[closeStart + 2:closeEnd]
				before = after[0:closeStart]
				openStart = before.rfind('<' + tag + '>')
				if -1 != openStart:
					openEnd = openStart + len(tag) + 1
				else:
					openStart = before.rfind('<' + tag + ' ')
					if -1 != openStart:
						openEnd = before.find('>', openStart + len(tag) + 1)
				if -1 != openStart and -1 != openEnd:
					extraClose = before.find('</' + tag + '>', openEnd, closeStart)
					if -1 != extraClose:
						return self.splitOnNearestClosedTag(after[0:openStart] + after[extraClose + len(tag) + 3:])
					else:
						before = before[0:openStart]
				after = after[closeEnd + 1:]
		return before, after

	def nearestUnclosedTag( self, string ) :
		openStart = string.rfind('<')
		if -1 != openStart:
			openEnd = string.find('>', openStart + 1)
			if '/' == string[openEnd - 1]:
				if 0 == openStart:
					return None
				else:
					return self.nearestUnclosedTag(string[0:openStart - 1])
			else:
				space = string.find(' ', openStart + 1)
				if -1 != space:
					openEnd = space
				return string[openStart + 1:openEnd]
