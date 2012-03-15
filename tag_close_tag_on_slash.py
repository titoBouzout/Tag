import sublime, sublime_plugin
from Tag import Tag

Tag = Tag()

class TagCloseTagOnSlashCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		view = self.view
		is_xml = Tag.view_is_xml(view)

		closed_some_tag = False
		new_selections = []
		new_selections_insert = []

		for region in view.sel():
			cursorPosition = region.begin()
			previousCharacter = view.substr(sublime.Region(cursorPosition - 1, cursorPosition))

			if '<' == previousCharacter:
				tag = self.close_tag(view.substr(sublime.Region(0, cursorPosition)), is_xml)
				if region.empty():
					replace = False
					view.insert(edit, cursorPosition, tag);
				else:
					replace = True
					view.replace(edit, sublime.Region(region.begin(), region.end()), '');
					view.insert(edit, cursorPosition, tag);
				if tag != '/':
					closed_some_tag = True
					if replace:
						new_selections_insert.append(sublime.Region(region.begin()+len(tag), region.begin()+len(tag)))
					else:
						new_selections_insert.append(sublime.Region(region.end()+len(tag), region.end()+len(tag)))
				else:
					new_selections.append(sublime.Region(region.end()+len(tag), region.end()+len(tag)))
			else:
				if region.empty():
					view.insert(edit, cursorPosition, '/');
				else:
					view.replace(edit, sublime.Region(region.begin(), region.end()), '/');
				new_selections.append(sublime.Region(region.end(), region.end()))

		view.sel().clear()

		# we inserted the "</tagname" part.
		# running the command "insert" with parameter ">" to allow
		# to the application indent these tags correctly
		if closed_some_tag:
			view.run_command('hide_auto_complete')
			for sel in new_selections_insert:
				view.sel().add(sel)
			view.run_command('insert',  {"characters": ">"})

		for sel in new_selections:
			view.sel().add(sel)

	def close_tag(self, data, is_xml):

		data = data.split('<')
		data.reverse()
		data.pop(0);

		try:
			i = 0
			lenght = len(data)-1
			while i < lenght:
				tag = Tag.name(data[i], True, is_xml)
				# if opening tag, close the tag
				if tag and not Tag.is_closing(data[i]):
					return '/'+Tag.name(data[i], True, is_xml)+''
				# if closing tag, jump to opening tag
				else:
					if tag:
						i = i+1
						skip = 0
						while i < lenght:
							if Tag.name(data[i], True, is_xml) == tag:
								if not Tag.is_closing(data[i]):
									if skip == 0:
										break
									else:
										skip = skip-1
								else:
									skip = skip+1
							i = i+1
				i = i+1
			return '/'
		except:
			return '/';