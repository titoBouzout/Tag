import sublime, sublime_plugin, re

class TagCloseTagOnSlashCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		closeTags = False;
		view = self.view
		for region in view.sel():
			cursorPosition = region.begin()
			previousCharacter = view.substr(sublime.Region(cursorPosition - 1, cursorPosition))

			if '<' == previousCharacter and view.score_selector(cursorPosition, 'text.html | text.xml') > 0:
				syntax = view.syntax_name(region.begin())
				should_skip = re.match(".*string.quoted.double", syntax) or re.match(".*string.quoted.single", syntax)
				if not should_skip:
					view.erase(edit, sublime.Region(cursorPosition - 1, cursorPosition))
					closeTags = True;
				else:
					if region.empty():
						view.insert(edit, cursorPosition, '/');
					else:
						view.replace(edit, sublime.Region(region.begin(), region.end()), '/');
			else:
				if region.empty():
					view.insert(edit, cursorPosition, '/');
				else:
					view.replace(edit, sublime.Region(region.begin(), region.end()), '/');
		if closeTags:
			view.run_command('close_tag');
			if view.window():
				view.window().show_input_panel("boo!", '', '', None, None)
				view.window().run_command('hide_panel');