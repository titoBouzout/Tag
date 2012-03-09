import sublime, sublime_plugin, time
from Tag import Tag

Tag = Tag()

class TagLintCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		view = self.view

		begin = time.time()

		region = view.sel()[0]
		if region.empty():
			region = sublime.Region(0, view.size())

		is_xml = view.file_name()
		if not is_xml:
			is_xml = False
		else:
			is_xml = is_xml.split('.')
			is_xml.reverse()
			is_xml = is_xml.pop(0)
			is_xml = is_xml == 'xml' or is_xml == 'xul' or is_xml == 'xhtml'

		original_position = region.begin()

		content = view.substr(region)

		# remove unparseable content

		# comments
		unparseable = content.split('<!--')
		content = unparseable.pop(0)
		l = len(unparseable)
		i = 0
		while i < l:
			tmp = unparseable[i].split('-->')
			content += '....'
			content += len(tmp.pop(0))*'.'
			content += '...'
			content += "...".join(tmp)
			i += 1

		# script
		unparseable = content.split('<script')
		content = unparseable.pop(0)
		l = len(unparseable)
		i = 0
		while i < l:
			tmp = unparseable[i].split('</script>')
			content += '.......'
			content += len(tmp.pop(0))*'.'
			content += '.........'
			content += ".........".join(tmp)
			i += 1

		# script
		unparseable = content.split('<style')
		content = unparseable.pop(0)
		l = len(unparseable)
		i = 0
		while i < l:
			tmp = unparseable[i].split('</style>')
			content += '......'
			content += len(tmp.pop(0))*'.'
			content += '........'
			content += "........".join(tmp)
			i += 1

		# linting: opening tags

		data = content.split('<')

		position = original_position+len(data.pop(0))

		invalid_tag_located_at = -1

		i = 0
		lenght = len(data)
		first_at = 0
		while i < lenght:
			tag = Tag.name(data[i], False, is_xml)
			if tag:
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
						message = '"'+tag+'" tag is not closing'
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
				if tag:
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
							message = '"'+tag+'" tag is not opening'
							invalid_tag_located_at = position-(len(data[i])+1)
							if invalid_tag_located_at < first_at:
								invalid_tag_located_at = -1
							break
				position -= len(data[i])+1
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
			view.add_regions("TagLint", [region], 'invalid', sublime.PERSISTENT | sublime.DRAW_EMPTY_AS_OVERWRITE)
			view.set_status('TagLint', message+' in Line '+str(line+1)+' '+str(time.time() - begin))
			view.show_at_center(region)
		else:
			view.set_status('TagLint', 'No errors found')
		# print 'Benchmark: '+str(time.time() - begin)
		sublime.set_timeout(lambda:self.clear_status(view), 4000);

	def clear_status(self, view):
		if view:
			view.erase_status('TagLint')