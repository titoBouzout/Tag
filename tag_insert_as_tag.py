import sublime, sublime_plugin, re
from Tag import Tag

Tag = Tag()

class TagInsertAsTagCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		view = self.view
		new_selections = []
		for region in view.sel():
			source = view.substr(region)
			if not source.strip():
				region = view.word(region)
				source = view.substr(region)
			if not source.strip():
				new_selections.append(sublime.Region(region.a, region.b))
				pass
			else:
				if re.match("^\s", source):
					view.replace(edit, region, '<p>'+source+'</p>')
					new_selections.append(sublime.Region(region.end()+3, region.end()+3))
				elif Tag.is_self_closing(source):
					view.replace(edit, region, '<'+source+'/>')
					new_selections.append(sublime.Region(region.end()+3, region.end()+3))
				else:
					tag = source.split('\r')[0].split('\n')[0].split(' ')[0]
					if tag and Tag.is_valid(tag) and tag != '<' and tag != '</' and tag != '>':
						view.replace(edit, region, '<'+source+'></'+tag+'>')
						new_selections.append(sublime.Region(region.end()+2, region.end()+2))
					else:
						new_selections.append(sublime.Region(region.end(), region.end()))

		view.sel().clear()
		for sel in new_selections:
			view.sel().add(sel)