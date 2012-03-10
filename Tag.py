import re

class Tag():

	def __init__(self):

		Tag.regexp_is_valid								= re.compile("^[a-z0-9\:\-_]+$", re.I);
		Tag.regexp_self_closing_optional 	= re.compile("^<?(\?xml|\!|area|base|br|col|frame|hr|img|input|link|meta|param|command|embed|source|/?li|/?p)[^a-z]", re.I);
		Tag.regexp_self_closing 					= re.compile("^<?(\?xml|\!|area|base|br|col|frame|hr|img|input|link|meta|param|command|embed|source)[^a-z]", re.I);
		Tag.regexp_self_closing_xml   		= re.compile("^<?(\?xml|\!)[^a-z]", re.I);
		Tag.regexp_is_closing 						= re.compile("^<?[^><]+/>", re.I);
		Tag.xml_files											= ['xhtml', 'xml', 'rdf', 'xul', 'svg', 'xsd', 'xslt','tmTheme', 'tmPreferences', 'tmLanguage', 'sublime-snippet']

	def is_valid(self, content):
		return Tag.regexp_is_valid.match(content)

	def is_self_closing(self, content, ignore_optional = True, is_xml= False):
		if ignore_optional:
			return Tag.regexp_self_closing.match(content)
		else:
			if is_xml == False:
				return Tag.regexp_self_closing_optional.match(content) or Tag.regexp_is_closing.match(content)
			else:
				return Tag.regexp_is_closing.match(content) or Tag.regexp_self_closing_xml.match(content)

	def name(self, content, ignore_optional = True, is_xml = False):
		if content[:1] == '/':
			tag_name = content.split('/')[1].split('>')[0];
		else:
			tag_name = content.split(' ')[0].split('>')[0];
		if self.is_valid(tag_name) and not self.is_self_closing(content, ignore_optional, is_xml):
			return tag_name
		else:
			return ''

	def is_closing(self, content):
		if content[:1] == '/' or Tag.regexp_is_closing.match(content):
			return True
		else:
			return False