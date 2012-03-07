import sublime, sublime_plugin
import re

# to find on which indentation level we currently are
current_indentation_re = re.compile("^\s*")

# to leave additional new lines as is
aditional_new_lines_re = re.compile("^\s*\n+\s*\n+\s*$")

# no indentation
no_indent = re.compile("^</?(head|body)[>| ]", re.I)

# possible self closing tags:      XML------HTML------------------------------------------------HTML5----------------
self_closing_tags = re.compile("^<(\?|\!|area|base|br|col|frame|hr|img|input|link|meta|param|command|embed|source)", re.I)

skip_content_of_this_tags_re = re.compile("^<(script|style|pre|code)(>| )", re.I)

trim_outter_left  = "abbr|acronym|dfn|em|strong|b|i|u|font|del|ins|sub|sup".split('|')
trim_outter_right = "".split('|')

trim_inner_left   = "abbr|acronym|dfn|em|strong|b|i|u|font|del|ins|sub|sup|title".split('|')
trim_inner_right  = "abbr|acronym|dfn|em|strong|b|i|u|font|del|ins|sub|sup|title".split('|')

def TagIndentBlock(data, view):

		# User settings
		settings = sublime.load_settings('Tag Package.sublime-settings')

		preserve_additional_new_lines = bool(settings.get('preserve_additional_new_lines', True))
		num_chars_considered_little_content = str(int(settings.get('little_content_means_this_number_of_characters', 60)))

		# the indent character
		if view.settings().get('translate_tabs_to_spaces') :
			indent_character = ' '*int(view.settings().get('tab_size', 4))
		else:
			indent_character = '\t'

		# on which indentation level we currently are?
		indentation_level = (current_indentation_re.search(data).group(0)).split("\n")
		current_indentation = indentation_level.pop()
		if len(indentation_level) == 1:
			beauty = "\n"+indentation_level[0]
		elif len(indentation_level) > 1:
			beauty = "\n".join(indentation_level)
		else:
			beauty = ''

		# pre processing
		if preserve_additional_new_lines == False:
			#fix comments
			data = re.sub(r'(\n\s*<\!--)', '\n\t\n\\1', data)

		# first newline should be skipped
		starting = True

		# inspiration from http://jyro.blogspot.com/2009/08/makeshift-xml-beautifier-in-python.html
		level = 0
		tags = re.split('(<[^>]+>)',data)
		lenght = len(tags)
		i = 0
		while i < lenght:
			f = tags[i]
			no_indent_match  = no_indent.match(f[:20])

			if f.strip() == '':
				if preserve_additional_new_lines and aditional_new_lines_re.match(f):
					beauty += '\n'
			elif f[0]=='<' and f[1] != '/':
				#	beauty += '1'
				if starting == False:
					beauty += '\n'
				starting = False
				beauty += current_indentation
				if not no_indent_match:
					beauty += indent_character*level
				if skip_content_of_this_tags_re.match(f[:20]):
					tag_is = re.sub(r'<([^ ]+)(>| ).*', '\\1', f[:20], 1)
					tag_is = re.compile("/"+tag_is+">$", re.I)
					beauty += f
					i = i+1
					while i < lenght:
						f = tags[i]
						if not tag_is.search(f[-20:]):
							beauty += f
							i = i+1
						else:
							beauty += f
							break
				else:
					beauty += f.strip()
					if not no_indent_match:
						level = level + 1
				#self closing tag
				if f[-2:] == '/>' or self_closing_tags.match(f):
					#beauty += '2'
					beauty += current_indentation
					if not no_indent_match:
						level = level - 1
			elif f[:2]=='</':
				if not no_indent_match:
					level = level - 1
				#beauty += '3'
				if starting == False:
					beauty += '\n'
				starting = False
				beauty += current_indentation
				if not no_indent_match:
					beauty += indent_character*level
				beauty += f.strip()
			else:
				#beauty += '4'
				if starting == False:
					beauty += '\n'
				starting = False
				beauty += current_indentation
				if not no_indent_match:
					beauty += indent_character*level
				beauty += f.strip()
			i = i+1

		if bool(settings.get('empty_tags_close_on_same_line', True)):
			# put empty tags on same line
			beauty = re.sub(r'<([^/!][^>]*[^/])>\s+</', '<\\1></', beauty)
			# put empty tags on same line for tags with one character
			beauty = re.sub(r'<([^/!])>\s+</', '<\\1></', beauty)

		if bool(settings.get('tags_with_little_content_on_same_line', True)):
			# put tags with little content on same line
			beauty = re.sub(r'<([^/][^>]*[^/])>\s*([^<\t\n]{1,'+num_chars_considered_little_content+'})\s*</', '<\\1>\\2</', beauty)
			# put tags with little content on same line for tags with one character
			beauty = re.sub(r'<([^/])>\s*([^<\t\n]{1,'+num_chars_considered_little_content+'})\s*</', '<\\1>\\2</', beauty)

		for tag in trim_outter_left:
			beauty = re.sub(r'\s+<'+tag+'(>| )', ' <'+tag+'\\1', beauty, re.I)
		for tag in trim_outter_right:
			beauty = re.sub(r'</'+tag+'>\s+([^\s])', '</'+tag+'> \\1', beauty, re.I)

		for tag in trim_inner_left:
			beauty = re.sub(r'<'+tag+'(>| [^>]*>)\s+([^\s])', '<'+tag+'\\1\\2', beauty, re.I)
		for tag in trim_inner_right:
			beauty = re.sub(r'\s+</'+tag+'>', '</'+tag+'> ', beauty, re.I)

		return beauty

class TagIndentCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if region.empty():
				continue
			if self.view.score_selector(region.a, 'text.html | text.xml') <= 0:
				dataRegion = region
			else:
				dataRegion = sublime.Region(self.view.line(region.begin()).begin(), region.end())
			data = TagIndentBlock(self.view.substr(dataRegion), self.view)
			self.view.replace(edit, dataRegion, data);

	def is_visible(self):
		for region in self.view.sel():
			if not region.empty():
				return True

class TagIndentDocumentCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		dataRegion = sublime.Region(0, self.view.size())
		data = TagIndentBlock(self.view.substr(dataRegion).strip(), self.view)
		self.view.replace(edit, dataRegion, data);

	def is_visible(self):
		value = False
		for region in self.view.sel():
			if region.empty():
				continue
			if self.view.score_selector(region.a, 'text.html | text.xml') <= 0:
				return False
			else:
				value = True
		return value or self.view.score_selector(sublime.Region(0, 100).a, 'text.html | text.xml') > 0