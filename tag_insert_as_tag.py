import sublime
import sublime_plugin
import re


class TagInsertAsTagCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    view = self.view
    self_closing = ["area", "base", "br", "col", "command", "embed", "hr", "img", "input", "keygen", "link", "meta", "param", "source", "track", "wbr"]
    self_closing_empty = ["br", "hr", "wbr"]

    for region in view.sel():
      if view.score_selector(region.a, 'text.html, text.xml') > 0:
        word_reg = view.word(region)
        word = view.substr(word_reg)
        if re.search("\s\Z", word) or word == "":
          view.run_command("insert_snippet", {"name": "Packages/Tag/Insert As Tag/default-tag.sublime-snippet"})
        else:
          view.sel().clear()
          if word in self_closing:
            if word in self_closing_empty:
              tags = "<%s>" % (word)
            else:
              tags = "<%s >" % (word)
          else:
            tags = "<%s></%s>" % (word, word)
          view.replace(edit, word_reg, tags)
          view.sel().add(sublime.Region(word_reg.b + 2))
