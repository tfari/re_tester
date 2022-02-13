""" TODO: Document """
import json
import os.path
import sys
import dataclasses
from tkinter.font import Font


@dataclasses.dataclass
class Settings:
    """ TODO: Document """
    topmost: bool = True
    font_family_name: str = 'Monospace'
    font_size: int = 10
    default_background: str = "#29251c"
    default_foreground: str = "#e8c25d"

    topbar_frame_background_color: str = "#29251c"
    topbar_frame_foreground_color: str = "#cfcbc2"
    topbar_frame_cursor_color: str = "#c9c7c1"

    test_box_frame_test_box_background_color: str = "#26231b"
    test_box_frame_test_box_foreground_color: str = "#cfcbc2"
    test_box_frame_textbox_cursor_color: str = "#c9c7c1"
    test_box_frame_line_numbers_background_color: str = "#29251c"
    test_box_frame_line_numbers_foreground_color: str = "#cfcbc2"

    results_tree_frame_background_color: str = "#29251c"
    results_tree_frame_foreground_color: str = "#cfcbc2"

    debug_frame_background_color: str = "#332f25"
    debug_frame_foreground_color: str = "#d92e04"

    full_match_color: str = "#3b6a6e"
    group_match_colors: tuple[str] = (
        "#694848",
        "#823535",
        "#9B0101",
        "#2C5A36",
        "#4E5A47",

        "#3D4E5A",
        "#302FF0",
        "#44448C",
        "#0707F0",
        "#585A09"
    )
    no_more_groups_match_background: str = '#8FF0A4'
    no_more_groups_match_foreground: str = '#29251c'

    def __post_init__(self):
        # Instantiate font object
        self.font: Font = None

    def to_json(self):
        """ Return ready for JSON """
        response = self.__dict__
        response.pop('font')  # Take out font
        return response

    @staticmethod
    def read_from_file():
        """ TODO: Document """
        path = sys.path[0] + '/resources'
        if os.path.exists(path):
            try:
                with open(f'{path}/settings.json', 'r', encoding='utf-8') as r_file:
                    s = Settings(**json.loads(r_file.read()))
            except FileNotFoundError:
                s = Settings()
                json.dump(s.to_json(), open(f'{path}/settings.json', 'w'), indent=4)
            except json.decoder.JSONDecodeError:
                print("[!] Warning, broken JSON, using default values.")
                s = Settings()
            finally:
                return s
        else:
            os.makedirs(path)
            s = Settings()
            json.dump(s.to_json(), open(f'{path}/settings.json', 'w'), indent=4)

        return s


SETTINGS: Settings = Settings.read_from_file()
