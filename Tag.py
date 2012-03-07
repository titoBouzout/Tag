import re

class Tag():

	def __init__(self):

		Tag.regexp_is_valid								= re.compile("^[a-z0-9\:-_]+$", re.I);
		Tag.regexp_self_closing_optional 	= re.compile("^<?(\?xml|\!|area|base|br|col|frame|hr|img|input|link|meta|param|command|embed|source|/?li|/?p)[^a-z]", re.I);
		Tag.regexp_self_closing 					= re.compile("^<?(\?xml|\!|area|base|br|col|frame|hr|img|input|link|meta|param|command|embed|source)[^a-z]", re.I);
		Tag.regexp_is_closing 						= re.compile("^<?[^><]+/>", re.I);

	def is_valid(self, content):
		return Tag.regexp_is_valid.match(content)

	def is_self_closing(self, content, ignore_optional = True):
		if ignore_optional:
			return Tag.regexp_self_closing.match(content)
		else:
			return Tag.regexp_self_closing_optional.match(content) or Tag.regexp_is_closing.match(content)

	def name(self, content, ignore_optional = True):
		if content[:1] == '/':
			tag_name = content.split('/')[1].split('>')[0];
		else:
			tag_name = content.split(' ')[0].split('>')[0];
		if self.is_valid(tag_name) and not self.is_self_closing(content, ignore_optional):
			return tag_name
		else:
			return ''

	def is_closing(self, content):
		if content[:1] == '/' or Tag.regexp_is_closing.match(content):
			return True
		else:
			return False