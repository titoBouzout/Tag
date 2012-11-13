import sublime, sublime_plugin
from time import time, sleep
import threading, thread
from Tag import Tag
import re

Tag = Tag()

s = sublime.load_settings('Tag Package.sublime-settings')

class Pref:
	def load(self):
		Pref.view              				              = False
		Pref.modified          				              = False
		Pref.elapsed_time      				              = 0.4
		Pref.time	      							              = time()
		Pref.wait_time	      				              = 0.8
		Pref.running           				              = False
		Pref.enable_live_tag_linting 	              = s.get('enable_live_tag_linting', True)
		Pref.hard_highlight						              = ['', 'html', 'htm', 'php', 'tpl', 'md', 'txt']
		Pref.enable_live_tag_linting_document_types	= [item.lower() for item in s.get('enable_live_tag_linting_document_types', '')]
		Pref.statuses									              = 0
		Pref.message_line							              = -1
		Pref.selection_last_line			              = -1
		Pref.message							                  = ''
		Pref.view_size							                = 0

Pref = Pref();
Pref.load()
s.add_on_change('reload', lambda:Pref.load())

class TagLint(sublime_plugin.EventListener):

	def on_activated(self, view):
		if not view.settings().get('is_widget') and not view.is_scratch():
			Pref.view = view
			Pref.selection_last_line = -1

	def on_load(self, view):
		if not view.settings().get('is_widget') and not view.is_scratch():
			Pref.modified = True
			Pref.view = view
			sublime.set_timeout(lambda:self.run(True), 0)

	def on_modified(self, view):
		if not view.settings().get('is_widget') and not view.is_scratch():
			Pref.modified = True
			Pref.time = time()

	def on_selection_modified(self, view):
		if Pref.enable_live_tag_linting:
			sel = view.sel()
			if sel and Pref.message_line != -1 and Pref.message != '':
				line = view.rowcol(sel[0].end())[0]
				if Pref.selection_last_line != line:
					Pref.selection_last_line = line
					if line == Pref.message_line:
						view.set_status('TagLint', Pref.message)
					else:
						Pref.statuses += 1
						sublime.set_timeout(lambda:self.clear_status(view, False), 7000);
						#view.erase_status('TagLint')
			# else:
			# 	view.erase_status('TagLint')

	def on_close(self, view):
		Pref.view = False
		Pref.modified = True

	def guess_view(self):
		if sublime.active_window() and sublime.active_window().active_view():
			Pref.view = sublime.active_window().active_view()

	def run(self, asap = False, from_command = False):
		now = time()
		if asap == False and (now - Pref.time < Pref.wait_time):
			return
		if (Pref.enable_live_tag_linting or from_command) and Pref.modified and not Pref.running:
			Pref.modified = False
			if from_command:
				Pref.view = sublime.active_window().active_view()
			if Pref.view:
				view = Pref.view
				Pref.view_size = view.size()
				if Pref.view_size > 10485760:
					return
				if Pref.view.settings().get('is_widget') or Pref.view.is_scratch():
					return
				file_ext = ('name.'+(view.file_name() or '')).split('.')
				file_ext.reverse()
				file_ext = file_ext.pop(0).lower()
				if not from_command and file_ext not in Pref.enable_live_tag_linting_document_types:
					return
				Pref.running = True
				is_xml = Tag.view_is_xml(view)
				if from_command:
					if view.sel():
						region = view.sel()[0]
						if region.empty():
							region = sublime.Region(0, view.size())
					else:
						region = sublime.Region(0, view.size())
				else:
					region = sublime.Region(0, view.size())
				original_position = region.begin()
				content = view.substr(region)
				TagLintThread(view, content, original_position, is_xml, from_command).start()
			else:
				self.guess_view()

	def display(self, view, message, invalid_tag_located_at, from_command):
		if view is not None:
			view.erase_regions("TagLint")
			if invalid_tag_located_at > -1:
				invalid_tag_located_at_start = invalid_tag_located_at
				invalid_tag_located_at_end   = invalid_tag_located_at+1
				size = view.size()
				while invalid_tag_located_at_end < size:
					end = view.substr(sublime.Region(invalid_tag_located_at_end, invalid_tag_located_at_end+1))
					if end == '>':
						invalid_tag_located_at_end += 1
						break
					elif end == '<':
						break;
					invalid_tag_located_at_end += 1
					if invalid_tag_located_at_start - invalid_tag_located_at_end > 100:
						break
				region = sublime.Region(invalid_tag_located_at_start, invalid_tag_located_at_end)
				line, col = view.rowcol(region.a);
				view.add_regions("TagLint", [region], 'variable.parameter', 'dot', sublime.PERSISTENT | sublime.DRAW_EMPTY_AS_OVERWRITE | sublime.DRAW_OUTLINED)
				Pref.message_line = line
				Pref.message = message
				view.set_status('TagLint', Pref.message+' in Line '+str(Pref.message_line+1)+' ')
				Pref.statuses += 1
				sublime.set_timeout(lambda:self.clear_status(view, from_command), 7000);
				if from_command:
					view.show_at_center(region)
			else:
				Pref.message_line = -1
				Pref.message = ''
				if from_command:
					view.set_status('TagLint', 'No errors found')
					Pref.statuses += 1
					sublime.set_timeout(lambda:self.clear_status(view, from_command), 7000);
				else:
					view.erase_status('TagLint')
		else:
			Pref.message_line = -1
			Pref.message = ''
		Pref.running = False

	def clear_status(self, view, from_command):
		Pref.statuses -= 1
		if view is not None and Pref.statuses == 0:
			view.erase_status('TagLint')
			if from_command and Pref.enable_live_tag_linting == False:
				view.erase_regions("TagLint")

tag_lint = TagLint();

class TagLintThread(threading.Thread):

	def __init__(self, view, content, original_position, is_xml, from_command):
		threading.Thread.__init__(self)
		self.view              = view
		self.content           = content
		self.original_position = original_position
		self.is_xml            = is_xml
		self.message           = ''
		self.invalid_tag_located_at = -1
		self.from_command 		 = from_command

	def run(self):

		begin = time()

		content           = self.content
		original_position = self.original_position
		is_xml            = self.is_xml

		# remove unparseable content

		content = Tag.clean_html(content)

		# linting: opening tags

		data = content.split('<')

		position = original_position+len(data.pop(0))

		invalid_tag_located_at = -1

		i = 0
		lenght = len(data)
		first_at = 0
		while i < lenght:
			tag = Tag.name(data[i], False, is_xml)
			if tag and tag != 'html' and tag != 'body' and tag != 'head':
				# if opening tag, then check if closing tag exists
				if not Tag.is_closing(data[i]):
					# print tag+' is opening '
					if first_at == 0:
						first_at = position
					a = i+1
					skip = 0
					while a < lenght:
						inner_tag_name    = Tag.name(data[a], False, is_xml)
						# check if same tag was found
						if inner_tag_name and inner_tag_name == tag:
							# check if tag is closing
							if Tag.is_closing(data[a]):
								if skip == 0:
									break
								else:
									skip = skip-1
							else:
								skip = skip+1
						a = a+1
					if a >= lenght:
						self.message = '"'+tag+'" tag is not closing'
						invalid_tag_located_at = position
						break
			position += len(data[i])+1
			i = i+1

		# linting: closing tags

		if invalid_tag_located_at == -1:

			position = original_position+len(content);

			data = content.split('<')
			data.reverse()

			i = 0
			lenght = len(data)-1
			while i < lenght:
				tag = Tag.name(data[i], False, is_xml)
				if tag and tag != 'html' and tag != 'body' and tag != 'head':
					# if closing tag, check if opening tag exists
					if Tag.is_closing(data[i]):
						# print tag+' is closing '
						a = i+1
						skip = 0
						while a < lenght:
							inner_tag_name    = Tag.name(data[a], False, is_xml)
							if inner_tag_name and inner_tag_name == tag:
								# check if tag is opening
								if not Tag.is_closing(data[a]):
									if skip == 0:
										break
									else:
										skip = skip-1
								else:
									skip = skip+1
							a = a+1
						if a >= lenght:
							self.message = '"'+tag+'" tag is not opening'
							invalid_tag_located_at = position-(len(data[i])+1)
							if invalid_tag_located_at < first_at:
								invalid_tag_located_at = -1
							break
				position -= len(data[i])+1
				i = i+1

		elapsed_time = time() - begin;

		# print 'Benchmark: '+str(elapsed_time)

		self.invalid_tag_located_at = invalid_tag_located_at

		sublime.set_timeout(lambda:tag_lint.display(self.view, self.message, self.invalid_tag_located_at, self.from_command), 0)


tag_lint_run = tag_lint.run
def tag_lint_loop():
	while True:
		# sleep time is adaptive, if takes more than 0.4 to calculate the word count
		# sleep_time becomes elapsed_time*3
		if Pref.running == False:
			sublime.set_timeout(lambda:tag_lint_run(), 0)
		sleep((Pref.elapsed_time*3 if Pref.elapsed_time > 0.4 else 0.4))

if not 'running_tag_lint_loop' in globals():
	running_tag_lint_loop = True
	thread.start_new_thread(tag_lint_loop, ())


class TagLintCommand(sublime_plugin.WindowCommand):
	def run(self):
		Pref.modified = True
		Pref.running = False
		tag_lint_run(True, True);