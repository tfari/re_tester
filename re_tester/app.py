""" Root widget """
import re
from tkinter import Tk, INSERT
from tkinter.font import Font

from re_tester.settings import SETTINGS
from re_tester.frames import TopBarFrame, TestBoxFrame, ResultsTreeFrame, DebugFrame


class App(Tk):
    """ ROOT Widget """
    def __init__(self):
        super().__init__()
        self.title("re_tester")
        self.attributes("-topmost", SETTINGS.topmost)

        # Instantiate Font
        SETTINGS.font = Font(
            family=SETTINGS.font_family_name,
            size=SETTINGS.font_size
        )
        self.top_bar_frame = TopBarFrame()
        self.test_box_frame = TestBoxFrame()
        self.result_tree_frame = ResultsTreeFrame()
        self.debug_frame = DebugFrame()

        self.top_bar_frame.grid(column=0, row=1, sticky='nsew')
        self.test_box_frame.grid(column=0, row=2, sticky='nsew')
        self.result_tree_frame.grid(column=0, row=3, sticky='nsew')
        self.debug_frame.grid(column=0, row=4, sticky='nsew')

        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=3)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Set bindings
        self.set_bindings()
        # Focus regex text box
        self.top_bar_frame.regex_text_box.focus_set()

    def set_bindings(self) -> None:
        """ Set bindings """
        self.top_bar_frame.regex_text_box.bind("<<TextModified>>", lambda x: self.on_text_mod())
        self.test_box_frame.test_textbox.bind("<<TextModified>>", lambda x: self.on_text_mod())
        self.test_box_frame.test_textbox.bind("<KP_Enter>", lambda x: self.test_box_frame.test_textbox.insert(
            INSERT, '\n'))
        self.top_bar_frame.regex_string.trace_add("write", lambda x, y, z: self.on_text_mod())  # Ugly!

    def on_text_mod(self) -> None:
        """ When text is modified in either textbox. """
        self.test_box_frame.text_was_modified()
        self.debug_frame.clear()
        self.result_tree_frame.clear()
        pattern = self.top_bar_frame.get_regex_pattern()
        if pattern:
            try:
                self.re_get(pattern, self.test_box_frame.get_test_textbox_contents())
            except re.error as e:
                self.debug_frame.show_error(e)

    def re_get(self, patt: str, matcher_text: list[str]) -> None:
        """ Attempt the regex match and highlight/add to the tree accordingly. """
        for index, line in enumerate(matcher_text, start=1):
            match = re.search(re.compile(patt), line)
            if match:
                s_tree = self.result_tree_frame.add_parent_line_match(index, match.group())
                self.test_box_frame.add_tag_full_match(index, match)

                named_groups = {k: (match.start(k), match.end(k)) for k in match.groupdict()}
                for g_index, group_match_str in enumerate(match.groups(), start=1):
                    if match.start(g_index) != -1:  # -1 are non-matches
                        # Get group name
                        name = ' - (anonymous)'
                        ks = []
                        for k in named_groups:
                            if named_groups[k] == (match.start(g_index), match.end(g_index)):
                                name = f' - ({k})'
                                ks.append(k)
                                break  # Take first on perfectly overlapping named groups. Ex: (?P<a>(?P<b>test))
                        [named_groups.pop(k) for k in ks]  # Update named_groups

                        self.test_box_frame.add_tag_group(index, g_index, match)
                        self.result_tree_frame.add_sub_line_match(s_tree, g_index, name, group_match_str)


root = App()
root.mainloop()
