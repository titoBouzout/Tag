Description
------------------

"Tag" plugin is a collection of packages about tags, mixed together in an effort to provide a single package with utilities to work with tags.

Currently provides: "Close tag on slash", "Tag indent or AutoFormat Tags",  "Tag Remove", "Insert as Tag", "Tag Remove Attributes", "Tag Close", "Tag Lint"

Improvements and more features about tags are welcome on this package. Please submit these.

Source / Installation
------------------

Convenient way to install this plugin is to use "Package Control" via http://wbond.net/sublime_packages/package_control

Upgrade
------------------

If you already installed "Close tag on slash" or "Tag indent", please remove these packages first and the associated settings. "Close tag on slash" already provides keymap for "/", then if you already installed that keymap you may want to remove it.

Close tag on slash
------------------

A command that is meant to be bound to the slash ("/") key in order to semi auto close open HTML tags (in part inspired by the discussion at http://www.sublimetext.com/forum/viewtopic.php?f=5&t=1358).
Requires build 2111 or later of Sublime Text 2.

*Usage*

Runs automatically when inserting an Slash "/" into an HTML document.

Tag Indent
------------------

Apply and/or add beauty indentation to HTML/XML/RDF/XUL tags found on selection(s).

*Aims*

Aims to add and/or apply correct indentation to little portions of HTML or XML, not to complete documents.

*Usage*

There is context menuitems called "Indent Tags on Selection", "Indent Tags on Document"

There is also Main menuitems: Edit -> Tag -> "Indent Tags on Selection", "Indent Tags on Document"

There is also commands "Indent Tags on Selection", "Indent Tags on Document"

*Information*

It takes the starting "indentation level" from the first line of each selection and sums tabs as needed.

On empty tags, and on tags with less than 60 characters, it writes the tag in one line.

Short-cut is "ctrl+alt+f"

Tag Remove
------------------

Provides the ability to remove all tags or some selected tags in a document or in selection(s).

*Usage*

The main menu "Edit" -> "Tag" provide access to the commands

Insert As Tag
------------------

Converts the current word to an html-tag. If there is no current word, a default tag is inserted.

*Usage*

The short-cut is "ctrl+shift+,"

Tag Remove Attributes
------------------

Allows to remove attributes from tags for selection or document.

*Usage*

The main menu "Edit" -> "Tag" provide access to the commands

Tag Close
------------------

Overwrite the built-in funtionallity by a custom one provided by this package which fix some bugs.

*Usage*

Windows, Linux : ALT+.
OSX : SUPER+ALT+.

Tag Lint
------------------

Experimental feature which aims to check correctness of opened and closed tags.

*Usage*

The main menu "Edit" -> "Tag" -> "Tag Lint"
