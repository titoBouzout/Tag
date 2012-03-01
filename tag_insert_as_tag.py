import sublime
import sublime_plugin
import re

class TagInsertAsTagCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		view = self.view
		self_closing_tags = re.compile("^(area|base|br|col|frame|hr|img|input|link|meta|param|command|embed|source)", re.I)
		new_selections = []
		for region in view.sel():
			source = view.substr(region)
			if not source.strip():
				region = view.word(region)
				source = view.substr(region)
			if not source.strip():
				pass
			else:
				if re.match("^\s", source):
					view.replace(edit, region, '<p>'+source+'</p>')
					new_selections.append(sublime.Region(region.end()+3, region.end()+3))
				elif self_closing_tags.match(source):
					view.replace(edit, region, '<'+source+'/>')
					new_selections.append(sublime.Region(region.end()+3, region.end()+3))
				else:
					view.replace(edit, region, '<'+source+'></'+source.split(' ')[0]+'>')
					new_selections.append(sublime.Region(region.end()+2, region.end()+2))

		view.sel().clear()
		for sel in new_selections:
			view.sel().add(sel)