""" Custom widgets definition """
from tkinter import Text, Canvas, Widget
from re_tester.settings import SETTINGS


class CustomText(Text):
    """
    Reports on internal widget commands, provides interface for line-numbering, and other useful methods.
    Based on https://stackoverflow.com/a/16375233
    """
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result

    def remove_all_tags(self):
        """ Delete all tags """
        for tag in self.tag_names():
            self.tag_delete(tag)  # Easy way, but requires recreating them each time

    def get_total_line_n(self) -> int:
        """ Return the number of lines in the widget """
        return self.index_to_line_n(self.index('end')) - 1

    def get_all_lines(self) -> list:
        """ Return the contents of the Widget separated by line """
        return self.get('0.0', 'end').split('\n')[:-1]

    def get_all_dlines(self) -> list:
        """
        Return a list with every line number and their associated dlineinfo
        :return: list[tuple[int, int, int , int, int], int] (dlineinfo, line_index)
        """
        results = []

        line_index = self.index('@0,0')
        d_line = self.dlineinfo(line_index)
        while d_line:
            results.append((d_line, self.index_to_line_n(line_index)))
            line_index = self.index(f'{line_index}+1line')
            d_line = self.dlineinfo(line_index)

        return results

    @staticmethod
    def index_to_line_n(tkinter_index: str) -> int:
        """
        Get a line number from a tkinter_index
        """
        return int(tkinter_index.split(".")[0])


class LeftLineNumbersBar(Canvas):
    """
    Width-responsive line numbering.
    Modification on: https://stackoverflow.com/a/16375233
    """
    def __init__(self, master: Widget):
        super().__init__(master)
        self.config(width=0, borderwidth=0, highlightthickness=0,
                    bg=SETTINGS.test_box_frame_line_numbers_background_color)
        self._x_padding = 5

    def _clear(self) -> None:
        """ Clear contents """
        self.delete('all')

    def draw_line_numbers(self, textbox: CustomText) -> None:
        """
        Write TextBox line numbers
        :param textbox: TextBox object
        """
        self._clear()
        total_line_n = textbox.get_total_line_n()
        self.config(width=self._get_width(total_line_n, self._x_padding))

        for d_line, line_number in textbox.get_all_dlines():
            y_position = d_line[1]
            line_number_str = self._fmt_line_n(line_number, total_line_n)
            self._write_text(self._x_padding, y_position, line_number_str)

    def _write_text(self, x_position: int, y_position: int, text: str):
        """
        Create text on canvas
        """
        self.create_text(x_position, y_position, anchor='nw', text=text,
                         fill=SETTINGS.test_box_frame_line_numbers_foreground_color, font=SETTINGS.font)

    @staticmethod
    def _get_width(total_lines: int, x_padding: int) -> int:
        """
        Get the width the Canvas should have to fit the width of the largest line number with
        the specified font.
        :param total_lines: int, the total lines we are working with
        :param x_padding: int, the padding for the text, we add this * 2 to account for it
        """
        return SETTINGS.font.measure('0' * len(str(total_lines))) + (x_padding * 2)

    @staticmethod
    def _fmt_line_n(line_number: int, total_lines: int, offset: int = 0) -> str:
        """
        Format line number string for Canvas printing.
        :param line_number: int, number of the line
        :param total_lines: int, number of total lines
        :param offset: int, offset line number, defaults to zero, only used for testing
        """
        return f'{str(line_number + offset):>{len(str(total_lines))}}'
