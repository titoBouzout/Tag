import sublime, sublime_plugin

class TagCloseTagOnSlashCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		closeTags = False;
		for region in self.view.sel():
			cursorPosition = region.begin()
			previousCharacter = self.view.substr(sublime.Region(cursorPosition - 1, cursorPosition))
			if '<' == previousCharacter and self.view.score_selector(cursorPosition, 'text.html | text.xml') > 0:
				self.view.erase(edit, sublime.Region(cursorPosition - 1, cursorPosition))
				closeTags = True;
			else:
				if region.empty():
					self.view.insert(edit, cursorPosition, '/');
				else:
					self.view.replace(edit, sublime.Region(region.begin(), region.end()), '/');
		if closeTags:
			self.view.run_command('close_tag');

			