import sublime, sublime_plugin
import re

class TagClassesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		data = ''
		classes = []
		for region in self.view.sel():
			if region.empty():
				continue
			data += self.view.substr(sublime.Region(region.begin(), region.end()))

		if not data:
			data += self.view.substr(sublime.Region(0, self.view.size()))

		if data:
			re_classes = (" ".join(re.compile('class="([^"]+)"').findall(data))).split()
			for item in re_classes:
				item = item.strip()
				if '.'+item+' {}' not in classes:
					classes.append('.'+item+' {}')
			if classes:
				s = sublime.load_settings('Tag Package.sublime-settings')
				if s.get('tag_classes_sort', False):
					classes.sort()
				sublime.set_clipboard("\n".join(classes))
				sublime.status_message("CSS Classes Copied to Clipboard")


