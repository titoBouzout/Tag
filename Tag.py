import re, sublime

class Tag():

	def __init__(self):

		Tag.regexp_is_valid								= re.compile("^[a-z0-9#\:\-_]+$", re.I);
		Tag.regexp_self_closing_optional 	= re.compile("^<?(\?xml|\!|area|base|br|col|frame|hr|img|input|link|meta|param|command|embed|source|/?li|/?p)[^a-z]", re.I);
		Tag.regexp_self_closing 					= re.compile("^<?(\?xml|\!|area|base|br|col|frame|hr|img|input|link|meta|param|command|embed|source)[^a-z]", re.I);
		Tag.regexp_self_closing_xml   		= re.compile("^<?(\?xml|\!)[^a-z]", re.I);
		Tag.regexp_is_closing 						= re.compile("^<?[^><]+/>", re.I);
		Tag.xml_files											= [item.lower() for item in ['xhtml', 'xml', 'rdf', 'xul', 'svg', 'xsd', 'xslt','tmTheme', 'tmPreferences', 'tmLanguage', 'sublime-snippet', 'opf', 'ncx']]

	def is_valid(self, content):
		return Tag.regexp_is_valid.match(content)

	def is_self_closing(self, content, return_optional_tags = True, is_xml= False):
		if return_optional_tags:
			if is_xml == False:
				return Tag.regexp_self_closing.match(content) or Tag.regexp_is_closing.match(content)
			else:
				return Tag.regexp_is_closing.match(content) or Tag.regexp_self_closing_xml.match(content)
		else:
			if is_xml == False:
				return Tag.regexp_self_closing_optional.match(content) or Tag.regexp_is_closing.match(content)
			else:
				return Tag.regexp_is_closing.match(content) or Tag.regexp_self_closing_xml.match(content)

	def name(self, content, return_optional_tags = True, is_xml = False):
		if content[:1] == '/':
			tag_name = content.split('/')[1].split('>')[0];
		else:
			tag_name = content.split(' ')[0].split('>')[0];
		if self.is_valid(tag_name) and not self.is_self_closing(content, return_optional_tags, is_xml):
			return tag_name
		else:
			return ''

	def is_closing(self, content):
		if content[:1] == '/' or Tag.regexp_is_closing.match(content):
			return True
		else:
			return False

	def view_is_xml(self, view):
		if view.settings().get('is_xml'):
			return True
		else:
			name = view.file_name()
			if not name:
				is_xml = '<?xml' in view.substr(sublime.Region(0, 50))
			else:
				name = ('name.'+name).split('.')
				name.reverse()
				name = name.pop(0).lower()
				is_xml = name in Tag.xml_files or '<?xml' in view.substr(sublime.Region(0, 50))
			view.settings().set('is_xml', is_xml)
			return is_xml

	def clean_html(self, content):

		# normalize
		content = content.replace('\r', '\n').replace('\t', ' ')

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

		unparseable = content.split('/*')
		content = unparseable.pop(0)
		l = len(unparseable)
		i = 0
		while i < l:
			tmp = unparseable[i].split('*/')
			content += '..'
			content += len(tmp.pop(0))*'.'
			content += '..'
			content += "..".join(tmp)
			i += 1

		unparseable = re.split('(\s\/\/[^\n]+\n)', content)
		
		for comment in unparseable:
			if comment[:3] == '\n//' or comment[:3] == ' //':
				content = content.replace(comment, (len(comment))*'.')

		unparseable = re.split('(\s\#[^\n]+\n)', content)
		
		for comment in unparseable:
			if comment[:3] == '\n#' or comment[:3] == ' #':
				content = content.replace(comment, (len(comment))*'.')

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

		# style
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

		return content
