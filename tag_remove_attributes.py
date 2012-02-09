import sublime, sublime_plugin
import re

def TagRemoveAttributesClean(data):
	regexp = re.compile(r'(<([a-z0-9-]+)\s+>)');
	data = regexp.sub('<\\2>', data);
	return data

def TagRemoveAttributesAll(data, view):
	return TagRemoveAttributesClean(re.sub(r'(<([a-z0-9-]+)\s+[^>]+>)', '<\\2>', data));
	
def TagRemoveAttributesSelected(data, attributes, view):
	attributes = attributes.replace(',', ' ').replace(';', ' ').replace('|', ' ')+' '
	for attribute in attributes.split(' '):
		if attribute:
			regexp = re.compile(r'(<([a-z0-9-]+\s+)([^>]*)\s*'+re.escape(attribute)+'="[^"]+"\s*([^>]*)>)')
		 	data = regexp.sub('<\\2\\3\\4>', data);
		 	data = TagRemoveAttributesClean(data);
	return data;

class TagRemoveAllAttributesInSelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if region.empty():
				continue
			dataRegion = sublime.Region(region.begin(), region.end())
			data = TagRemoveAttributesAll(self.view.substr(dataRegion), self.view)
			self.view.replace(edit, dataRegion, data);

class TagRemoveAllAttributesInDocumentCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		dataRegion = sublime.Region(0, self.view.size())
		data = TagRemoveAttributesAll(self.view.substr(dataRegion), self.view)
		self.view.replace(edit, dataRegion, data);

class TagRemovePickedAttributesInSelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		import functools
		self.view.window().run_command('hide_panel');
		self.view.window().show_input_panel("Remove the following attributes:", '', functools.partial(self.on_done, edit), None, None)

	def on_done(self, edit, attributes):
		for region in self.view.sel():
			if region.empty():
				continue
			dataRegion = sublime.Region(region.begin(), region.end())
			data = TagRemoveAttributesSelected(self.view.substr(dataRegion), attributes, self.view)
			self.view.replace(edit, dataRegion, data);

class TagRemovePickedAttributesInDocumentCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		import functools
		self.view.window().run_command('hide_panel');
		self.view.window().show_input_panel("Remove the following attributes:", '', functools.partial(self.on_done, edit), None, None)

	def on_done(self, edit, attributes):
		dataRegion = sublime.Region(0, self.view.size())
		data = TagRemoveAttributesSelected(self.view.substr(dataRegion), attributes, self.view)
		self.view.replace(edit, dataRegion, data);