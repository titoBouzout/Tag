import sublime, sublime_plugin, time
from Tag import Tag

Tag = Tag()

class TagLintCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		view = self.view

		begin = time.time()

		data = view.substr(sublime.Region(0, view.size()))

		# remove unparseable content

		# unparseable = re.findall('(<!--(.*)-->)', data, re.I | re.S)
		# for item in unparseable:
		# 	#print item
		# 	data = data.replace('<!--'+item[1]+'-->', '....'+('.'*(len(item)-1))+'...');

		# unparseable = re.findall('(<script(.*)</script>)', data, re.I | re.S)
		# for item in unparseable:
		# 	#print item
		# 	data = data.replace('<script'+item[1]+'</script>', '<script>'+('.'*(len(item)-1))+'</script>');

		# unparseable = re.findall('(<style(.*)</style>)', data, re.I | re.S)
		# for item in unparseable:
		# 	print item
		# 	data = data.replace('<style'+item[1]+'</style>', '<style>'+('.'*(len(item)-1))+'</style>');

		data = data.split('<')

		position = len(data.pop(0))
		invalid_tag_located_at = -1

		i = 0
		lenght = len(data)
		first = True
		opening = 0
		while i < lenght:
			tag = Tag.name(data[i], False)
			if tag:
				# print tag
				# if opening tag, check if closing tag exists
				if not Tag.is_closing(data[i]):
					opening += 1
					# print tag+' is opening '+str(opening)
					first = False
					a = i+1
					skip = 0
					while a < lenght:
						# print data[a]
						inner_tag_name    = Tag.name(data[a], False)
						inner_tag_closing = Tag.is_closing(data[a])
						if inner_tag_name:
							# print 'ACA0'+inner_tag_name
							if inner_tag_name == tag:
								if inner_tag_closing:
									if skip == 0:
										break
									else:
										skip = skip-1
								else:
									skip = skip+1
							if inner_tag_closing:
								#print 'closing '+inner_tag_name
								opening -= 1
							else:
								#print 'opening '+inner_tag_name
								opening += 1
						a = a+1
					if a >= lenght:
						message = '"'+tag+'" tag is not closing'
						invalid_tag_located_at = position
						break
				elif not first:
					# print tag+' is closing '+str(opening)
					# print i
					# print lenght-1
					if opening == 0 and i <= lenght-1:
						message = 'A tag "'+tag+'" is closing but was not opened'
					 	invalid_tag_located_at = position
					 	break
					opening -= 1

			position += len(data[i])+1
			i = i+1

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
			region = sublime.Region(invalid_tag_located_at_start, invalid_tag_located_at_end)
			line, col = view.rowcol(region.a);
			view.add_regions("TagLint", [region], 'invalid', sublime.PERSISTENT)
			view.set_status('TagLint', message+' in Line '+str(line+1))
			view.show_at_center(region)
		else:
			view.set_status('TagLint', 'No errors found')
		# print 'Benchmark: '+str(time.time() - begin)
		sublime.set_timeout(lambda:self.clear_status(view), 4000);

	def clear_status(self, view):
		if view:
			view.erase_status('TagLint')

