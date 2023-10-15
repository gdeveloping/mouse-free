
from common_utils import *


APP_TITLE = 'Mouse-Free-Application'

CONFIG_FILE_NAME = 'mouse-free.properties'

properties = get_config_from_properties_file(CONFIG_FILE_NAME)


# hotkey
KEYBOARD_SHOW_HOTKEY = properties['KEYBOARD_SHOW_HOTKEY']
KEYBOARD_SHOW_DETAIL_HOTKEY = properties['KEYBOARD_SHOW_DETAIL_HOTKEY']
KEYBOARD_SHOW_IN_SWITCHED_SCREEN_HOTKEY = properties['KEYBOARD_SHOW_IN_SWITCHED_SCREEN_HOTKEY']
KEYBOARD_HIDE_HOTKEY = properties['KEYBOARD_HIDE_HOTKEY']
KEYBOARD_QUIT_HOTKEY = properties['KEYBOARD_QUIT_HOTKEY']
KEYBOARD_MOUSE_CLICK_LEFT_HOTKEY = properties['KEYBOARD_MOUSE_CLICK_LEFT_HOTKEY']
KEYBOARD_MOUSE_CLICK_LEFT_DOUBLE_HOTKEY = properties['KEYBOARD_MOUSE_CLICK_LEFT_DOUBLE_HOTKEY']
KEYBOARD_MOUSE_CLICK_RIGHT_HOTKEY = properties['KEYBOARD_MOUSE_CLICK_RIGHT_HOTKEY']
KEYBOARD_SHOW_HOTKEY_OF_TOP_APP = properties['KEYBOARD_SHOW_HOTKEY_OF_TOP_APP']


# log file path
LOG_FILE_PATH = properties['LOG_FILE_PATH']
# log level
LOG_LEVEL = str_to_log_level(str(properties['LOG_LEVEL']).strip().upper())


# screen common
MAX_CELL_LEVEL = 2 # max level， start from 1
TRANSPARENCY = int(properties['TRANSPARENCY']) 
DELAY_HIDE_TIME = int(properties['DELAY_HIDE_TIME']) 
BACKGROUND_COLOR = get_tuple_number_from_str(properties['BACKGROUND_COLOR'])
IDENTIFIER_FONT_COLOR = get_tuple_number_from_str(properties['IDENTIFIER_FONT_COLOR'])
THREAD_POOL_MAX_WORKERS = int(properties['THREAD_POOL_MAX_WORKERS']) 

# level 1
CELL_WIDTH_COLUMN_SIZE = int(properties['CELL_WIDTH_COLUMN_SIZE'])  # level 1 cell width
CELL_HEIGHT_ROW_SIZE = int(properties['CELL_HEIGHT_ROW_SIZE'])  # level 1 cell height
FONT_SIZE = int(properties['FONT_SIZE'])  # level 1 font size
IDENTIFIER_KEY_COUNT = 2

# level 2
CELL_WIDTH_COLUMN_SIZE_LEVEL2 = int(properties['CELL_WIDTH_COLUMN_SIZE_LEVEL2'])  # level 2 cell width
CELL_HEIGHT_ROW_SIZE_LEVEL2 = int(properties['CELL_HEIGHT_ROW_SIZE_LEVEL2'])  # level 2 cell height
FONT_SIZE_LEVEL2 = int(properties['FONT_SIZE_LEVEL2'])  # level 2 font size
IDENTIFIER_KEY_COUNT_LEVEL2 = 1
CELL_COUNT_PER_WIDTH_PER_HEIGHT_LEVEL2 = 5
SCREEN_WIDTH_COLUMN_SIZE_LEVEL2 = CELL_WIDTH_COLUMN_SIZE_LEVEL2 * CELL_COUNT_PER_WIDTH_PER_HEIGHT_LEVEL2
SCREEN_HEIGHT_ROW_SIZE_LEVEL2 = CELL_HEIGHT_ROW_SIZE_LEVEL2 * CELL_COUNT_PER_WIDTH_PER_HEIGHT_LEVEL2

# level 3
FONT_SIZE_LEVEL3 = 15

# constant
LEVEL_1 = "LEVEL_1"
LEVEL_2 = "LEVEL_2"
LEVEL_3 = "LEVEL_3"
LEVEL_DEFAULT = LEVEL_1

KEY_CELL_WIDTH_COLUMN_SIZE = "CELL_WIDTH_COLUMN_SIZE"
KEY_CELL_HEIGHT_ROW_SIZE = "CELL_HEIGHT_ROW_SIZE"
KEY_FONT_SIZE = "FONT_SIZE"
KEY_SCREEN_WIDTH_COLUMN_SIZE = "SCREEN_WIDTH_COLUMN_SIZE"
KEY_SCREEN_HEIGHT_ROW_SIZE = "SCREEN_HEIGHT_ROW_SIZE"
KEY_IDENTIFIER_KEY_COUNT = "IDENTIFIER_KEY_COUNT"


idea_shortcuts = {
    'Ctrl + N': 'Go to class',
    'Ctrl + Shift + N': 'Go to file',
    'Ctrl + Alt + L': 'Reformat code',
    'Alt + Enter': 'Show intention actions and quick-fixes',
    'Ctrl + Alt + O': 'Optimize imports',
    'Ctrl + E': 'Recent files popup',
    'Ctrl + Space': 'Basic code completion',
    'Ctrl + Shift + Space': 'Smart code completion',
    'Ctrl + /': 'Comment/uncomment with line comment',
    'Ctrl + Shift + /': 'Comment/uncomment with block comment',
    'Ctrl + B': 'Go to declaration',
    'Ctrl + Shift + I': 'Quick definition lookup',
    'Ctrl + Q': 'Quick documentation lookup',
    'Ctrl + P': 'Parameter info',
    'Ctrl + Shift + F7': 'Highlight usages in file',
    'Ctrl + F12': 'File structure popup',
    'Alt + 1': 'Project view',
    'Alt + 2': 'Favorites'
}