import sublime, sublime_plugin

class CloseTagOnSlashCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		cursorPosition = self.view.sel()[0].begin()
		previousCharacter = self.view.substr(sublime.Region(cursorPosition - 1, cursorPosition))
		if '<' == previousCharacter:
			self.view.erase(edit, sublime.Region(cursorPosition - 1, cursorPosition))
			self.view.run_command('close_tag')
			if self.view.sel()[0].begin() < cursorPosition:
				self.view.insert(edit, cursorPosition - 1, '</')
		else:
			self.view.insert(edit, cursorPosition, '/')
