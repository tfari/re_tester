""" Application's frames """
from re import Match
from tkinter import ttk, Frame, Label, Scrollbar, FLAT, LEFT, RIGHT, Y, BOTH, END, NONE
from re_tester.widgets import CustomText, LeftLineNumbersBar
from re_tester.settings import SETTINGS


class TopBarFrame(Frame):
    """ Top bar frame """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(background=SETTINGS.default_background)

        self.regex_label = Label(self, text='re: ',
                                 font=SETTINGS.font,
                                 background=SETTINGS.topbar_frame_background_color,
                                 foreground=SETTINGS.default_foreground)
        self.regex_text_box = CustomText(self)
        self.regex_text_box.config(
            height=1,
            undo=True,
            relief=FLAT,
            font=SETTINGS.font,
            foreground=SETTINGS.topbar_frame_foreground_color,
            insertbackground=SETTINGS.topbar_frame_cursor_color,
            background=SETTINGS.topbar_frame_background_color,
            highlightcolor=SETTINGS.topbar_frame_background_color,
            highlightbackground=SETTINGS.topbar_frame_background_color,
        )
        self.regex_label.pack(side=LEFT, fill=Y)
        self.regex_text_box.pack(side=LEFT, fill=BOTH, expand=True)

    def get_regex_pattern(self) -> str:
        """ Get the regex pattern in self.regex_text_box """
        return self.regex_text_box.get_all_lines()[0]


class TestBoxFrame(Frame):
    """ Test box frame """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(background=SETTINGS.default_background)
        self.test_textbox_line_numbers = LeftLineNumbersBar(self)
        self.test_textbox = CustomText(self)
        self.test_textbox.config(
            undo=True,
            relief=FLAT,
            font=SETTINGS.font,
            foreground=SETTINGS.test_box_frame_test_box_foreground_color,
            insertbackground=SETTINGS.test_box_frame_textbox_cursor_color,
            background=SETTINGS.test_box_frame_test_box_background_color,
            highlightcolor=SETTINGS.test_box_frame_test_box_background_color,
            highlightbackground=SETTINGS.test_box_frame_test_box_background_color,
        )
        self.test_textbox_line_numbers.draw_line_numbers(self.test_textbox)

        self.test_textbox_scrollbar = Scrollbar(self, command=self.test_textbox.yview,
                                                bd=1,
                                                background=SETTINGS.default_background,
                                                highlightcolor=SETTINGS.default_background,
                                                highlightbackground=SETTINGS.default_background,
                                                activebackground=SETTINGS.default_background,
                                                troughcolor=SETTINGS.default_background,
                                                relief=FLAT
                                                )
        self.test_textbox.config(yscrollcommand=self.test_textbox_scrollbar.set)

        self.test_textbox_line_numbers.pack(side=LEFT, fill=Y)
        self.test_textbox.pack(side=LEFT, fill=BOTH, expand=True)
        self.test_textbox_scrollbar.pack(side=RIGHT, fill=Y)

        self._init_tags()

    def _init_tags(self):
        self.test_textbox.tag_config('full_match', background=SETTINGS.full_match_color)
        self.test_textbox.tag_config('no_more_groups', background=SETTINGS.no_more_groups_match_background,
                                     foreground=SETTINGS.no_more_groups_match_foreground)
        for group_index, group_color in enumerate(SETTINGS.group_match_colors, start=1):
            self.test_textbox.tag_config(f'group_{group_index}', background=group_color)

    def add_tag_full_match(self, index: int, match: Match):
        """ Tag a full match """
        pos = '{}+{}c'.format(f'{index}.{match.start()}', match.end() - match.start())
        self.test_textbox.tag_add('full_match', f'{index}.{match.start()}', pos)

    def add_tag_group(self, index: int, group_index: int, match: Match):
        """ Tag a group """
        tag_name = f'group_{group_index}' if f'group_{group_index}' in self.test_textbox.tag_names() else \
            'no_more_groups'
        pos = '{}+{}c'.format(f'{index}.{match.start(group_index)}', match.end(group_index) - match.start(group_index))
        self.test_textbox.tag_add(tag_name, f'{index}.{match.start(group_index)}', pos)

    def get_test_textbox_contents(self) -> list[str]:
        """ Returns contents of test_textbox """
        return self.test_textbox.get_all_lines()

    def text_was_modified(self):
        """ Draw line numbers and remove all tags from test_textbox """
        self.test_textbox_line_numbers.draw_line_numbers(self.test_textbox)
        self.test_textbox.remove_all_tags()
        self._init_tags()  # Recreate tags.


class ResultsTreeFrame(Frame):
    """ Test box frame """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(background=SETTINGS.default_background)
        self.result_tree_style = ttk.Style()
        self.result_tree_style.configure("Treeview",
                                         background=SETTINGS.results_tree_frame_background_color,
                                         foreground=SETTINGS.results_tree_frame_foreground_color,
                                         fieldbackground=SETTINGS.results_tree_frame_background_color,
                                         relief=FLAT,
                                         borderwidth=0
                                         )

        # Disable selected style
        self.result_tree_style.map("Treeview", background=[('selected', SETTINGS.default_background)],
                                   foreground=[('selected', SETTINGS.default_foreground)])
        self.result_tree = ttk.Treeview(self, height=10, style="Treeview", show="tree", selectmode=NONE)
        self.result_tree_scrollbar = Scrollbar(self, command=self.result_tree.yview,
                                               bd=1,
                                               background=SETTINGS.results_tree_frame_background_color,
                                               highlightcolor=SETTINGS.results_tree_frame_background_color,
                                               highlightbackground=SETTINGS.results_tree_frame_background_color,
                                               activebackground=SETTINGS.results_tree_frame_background_color,
                                               troughcolor=SETTINGS.results_tree_frame_background_color,
                                               relief=FLAT,
                                               )

        self.result_tree.config(yscrollcommand=self.result_tree_scrollbar.set)
        self.result_tree.pack(side=LEFT, fill=BOTH, expand=True)
        self.result_tree_scrollbar.pack(side=RIGHT, fill=Y)

        self._init_tags()

    def _init_tags(self):
        self.result_tree.tag_configure('full', foreground=SETTINGS.full_match_color)
        self.result_tree.tag_configure('no_more_groups', background=SETTINGS.no_more_groups_match_background,
                                       foreground=SETTINGS.no_more_groups_match_foreground)
        for group_index, group_color in enumerate(SETTINGS.group_match_colors, start=1):
            self.result_tree.tag_configure(f'group_{group_index}', foreground=group_color)

    def add_parent_line_match(self, index: int, match: str) -> str:
        """ Add a root item to tree """
        return self.result_tree.insert("", END, text=f'Line: {index} - Full match: "{match}"',
                                                 tags="full", open=True)

    def add_sub_line_match(self, parent_index: str, group_index: int, group_name: str, match: str):
        """ Add a children item to tree """
        tag_name = f'group_{group_index}' if self.result_tree.tag_configure(f'group_{group_index}')['foreground'] else \
            'no_more_groups'
        self.result_tree.insert(parent_index, END, text=f'Group: {group_index}{group_name}: "{match}"',
                                tags=tag_name)

    def clear(self):
        """ Delete all results on self.result_tree """
        for rt in self.result_tree.get_children(""):
            self.result_tree.delete(rt)


class DebugFrame(Frame):
    """ Test box frame """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(background=SETTINGS.default_background)
        self.debug_textbox = CustomText(self, height=3)
        self.debug_textbox.config(
                                  font=SETTINGS.font,
                                  background=SETTINGS.debug_frame_background_color,
                                  foreground=SETTINGS.debug_frame_foreground_color,
                                  highlightcolor=SETTINGS.debug_frame_background_color,
                                  highlightbackground=SETTINGS.debug_frame_background_color,
                                  relief=FLAT
                                  )
        self.debug_textbox.pack(side=LEFT, fill=BOTH, expand=True)

    def show_error(self, error: Exception):
        """ Insert error into self.debug_textbox """
        self.debug_textbox.insert('1.0', f'{error}')

    def clear(self):
        """ Delete all text on self.debug_textbox """
        self.debug_textbox.delete('1.0', END)
