import sublime, sublime_plugin

class CloseTagOnSlashCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		closeTags = False;
		for region in self.view.sel():
			cursorPosition = region.begin()
			previousCharacter = self.view.substr(sublime.Region(cursorPosition - 1, cursorPosition))
			if '<' == previousCharacter:
				self.view.erase(edit, sublime.Region(cursorPosition - 1, cursorPosition))
				closeTags = True;
			else:
				self.view.insert(edit, cursorPosition, '/');
		if closeTags:
			self.view.run_command('close_tag');