import sublime, sublime_plugin
import re

def TagRemoveAll(data, view):
	return re.sub(r'<[^>]*>', '', data);

def TagRemoveSelected(data, tags, view):
	tags = tags.replace(',', ' ').replace(';', ' ').replace('|', ' ')+' '
	for tag in tags.split(' '):
		if tag:
			regexp = re.compile('<'+re.escape(tag)+'(| [^>]*)>', re.IGNORECASE)
		 	data = regexp.sub('', data);
			regexp = re.compile('</'+re.escape(tag)+'>', re.IGNORECASE)
		 	data = regexp.sub('', data);
	return data;

class TagRemoveAllInSelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if region.empty():
				continue
			dataRegion = sublime.Region(region.begin(), region.end())
			data = TagRemoveAll(self.view.substr(dataRegion), self.view)
			self.view.replace(edit, dataRegion, data);

class TagRemoveAllInDocumentCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		dataRegion = sublime.Region(0, self.view.size())
		data = TagRemoveAll(self.view.substr(dataRegion), self.view)
		self.view.replace(edit, dataRegion, data);

class TagRemovePickedInSelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit, tags = False):
		if not tags:
			import functools
			self.view.window().run_command('hide_panel');
			self.view.window().show_input_panel("Remove the following tags:", '', functools.partial(self.on_done, edit), None, None)
		else:
			self.on_done(edit, tags);

	def on_done(self, edit, tags):
		for region in self.view.sel():
			if region.empty():
				continue
			dataRegion = sublime.Region(region.begin(), region.end())
			data = TagRemoveSelected(self.view.substr(dataRegion), tags, self.view)
			self.view.replace(edit, dataRegion, data);

class TagRemovePickedInDocumentCommand(sublime_plugin.TextCommand):
	def run(self, edit, tags = False):
		if not tags:
			import functools
			self.view.window().run_command('hide_panel');
			self.view.window().show_input_panel("Remove the following tags:", '', functools.partial(self.on_done, edit), None, None)
		else:
			self.on_done(edit, tags);

	def on_done(self, edit, tags):
		dataRegion = sublime.Region(0, self.view.size())
		data = TagRemoveSelected(self.view.substr(dataRegion), tags, self.view)
		self.view.replace(edit, dataRegion, data);