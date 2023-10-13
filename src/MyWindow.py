
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QCursor
from PyQt5.QtCore import Qt
from pynput import mouse
import string
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import traceback
import pygetwindow as gw
from pywinauto import Application
import psutil
import os
from utils import *
from properties import *
from log_utils import *
from KeyboardListener import KeyboardListener



class MyWindow(QWidget):
    def __init__(self, app: QApplication):
        log_function_name_to_enter()

        super(MyWindow, self).__init__()

        self.app = app

        self.screen_size_config = {
            LEVEL_1: {
                KEY_CELL_WIDTH_COLUMN_SIZE: CELL_WIDTH_COLUMN_SIZE,
                KEY_CELL_HEIGHT_ROW_SIZE: CELL_HEIGHT_ROW_SIZE,
                KEY_FONT_SIZE: FONT_SIZE,
                KEY_IDENTIFIER_KEY_COUNT: IDENTIFIER_KEY_COUNT
            },
            LEVEL_2: {
                KEY_CELL_WIDTH_COLUMN_SIZE: CELL_WIDTH_COLUMN_SIZE_LEVEL2,
                KEY_CELL_HEIGHT_ROW_SIZE: CELL_HEIGHT_ROW_SIZE_LEVEL2,
                KEY_FONT_SIZE: FONT_SIZE_LEVEL2,
                KEY_SCREEN_WIDTH_COLUMN_SIZE: SCREEN_WIDTH_COLUMN_SIZE_LEVEL2,
                KEY_SCREEN_HEIGHT_ROW_SIZE: SCREEN_HEIGHT_ROW_SIZE_LEVEL2,
                KEY_IDENTIFIER_KEY_COUNT: IDENTIFIER_KEY_COUNT_LEVEL2
            }
        }
        logger.info('screen_size_config: {}'.format(self.screen_size_config))

        self.executor_pool = ThreadPoolExecutor(max_workers=THREAD_POOL_MAX_WORKERS)

        self.desktop = QDesktopWidget()

        self.screen_level = LEVEL_DEFAULT        

        self.x_start_of_current_screen = 0
        self.y_start_of_current_screen = 0
        self.x_start_in_current_screen = 0
        self.y_start_in_current_screen = 0

        self.keys = []

        self.record_current_mouse_position()

        self.update_current_screen()
    
        self.init_ui()

        # listen keyboard
        self.keyboard_listener = KeyboardListener(logger)
        self.keyboard_listener.key_pressed_signal.connect(self.handle_keyboard)
        self.keyboard_listener.quit_signal.connect(self.quit_app)        
        self.keyboard_listener.show_signal.connect(self.my_show_full_window)
        self.keyboard_listener.show_detail_signal.connect(self.my_show_detail_window)
        self.keyboard_listener.show_in_switched_screen_signal.connect(self.my_show_window_in_switched_screen)
        self.keyboard_listener.hide_signal.connect(self.my_hide) 
        self.keyboard_listener.simulate_mouse_click_left_signal.connect(self.my_simulate_mouse_click_left)       
        self.keyboard_listener.simulate_mouse_click_left_double_signal.connect(self.my_simulate_mouse_click_left_double)
        self.keyboard_listener.simulate_mouse_click_right_signal.connect(self.my_simulate_mouse_click_right)
        self.keyboard_listener.start()

        log_function_name_to_exit()


    def update_current_screen(self):
        cursor = QCursor()
        current_screen = self.app.screenAt(cursor.pos())

        self.x_start_of_current_screen = current_screen.geometry().left()
        self.y_start_of_current_screen = current_screen.geometry().top()
        self.width_of_current_screen = current_screen.geometry().width()
        self.height_of_current_screen = current_screen.geometry().height()

        logger.info('cursor position: ({}, {}); current screen geometry: ({}, {}, {}, {})'.format(
            cursor.pos().x(), cursor.pos().y(), 
            self.x_start_of_current_screen, self.y_start_of_current_screen,
            self.width_of_current_screen, self.height_of_current_screen))

        screens = self.app.screens() 
        screen_index = screens.index(current_screen)
        is_primary_screen = current_screen == self.app.primaryScreen()
        logger.info('screen count: {}; current screen index: {}; current screen is primary screen: {}'.format(len(screens), screen_index, is_primary_screen))


    def init_ui(self):
        log_function_name_to_enter()

        # 幕布透明度
        self.setWindowOpacity(TRANSPARENCY / 100)
        # 隐藏边框，顶层显示
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 隐藏窗口在任务栏的展示
        self.setWindowFlags(Qt.Tool)
        self.window_tile = APP_TITLE
        self.setWindowTitle(self.window_tile)

        p = self.palette()
        bg_color = QColor(*BACKGROUND_COLOR)
        p.setColor(self.backgroundRole(), bg_color)
        self.setPalette(p) 

        self.showFullScreen()
        self.post_show_window()

        log_function_name_to_exit()
     
        
    def paintEvent(self, event):
        log_function_name_to_enter()

        try:
            current_font_size = self.get_current_font_size()
            current_cell_width_column_size = self.get_current_cell_width_column_size()
            current_cell_height_row_size = self.get_current_cell_height_row_size()

            # always full screen
            self.setGeometry(self.x_start_of_current_screen, self.y_start_of_current_screen, 
                             self.width_of_current_screen, self.height_of_current_screen)

            if self.screen_level == LEVEL_1:
                current_screen_width_column_size = self.get_current_screen_width_column_size()
                current_screen_height_row_size = self.get_current_screen_height_row_size()
                self.x_start_in_current_screen = 0
                self.y_start_in_current_screen = 0
            else:
                x, y = mouse.Controller().position
                current_screen_width_column_size = self.get_current_screen_size_config()[KEY_SCREEN_WIDTH_COLUMN_SIZE]
                current_screen_height_row_size = self.get_current_screen_size_config()[KEY_SCREEN_HEIGHT_ROW_SIZE]
                self.x_start_in_current_screen = max(0, x - current_screen_width_column_size // 2 - self.x_start_of_current_screen)
                self.y_start_in_current_screen = max(0, y - current_screen_height_row_size // 2 - self.y_start_of_current_screen)

            logger.debug('screenGeometry: {}, {}'.format(current_screen_width_column_size, current_screen_height_row_size))

            logger.debug('screen_level: {}; cell_width: {}; cell_height: {}; font_size: {}; x_start: {}; y_start: {}; window width: {}; window height: {}'.format(
                self.screen_level, 
                current_cell_width_column_size,
                current_cell_height_row_size,
                current_font_size,
                self.x_start_in_current_screen,
                self.y_start_in_current_screen,
                self.width(),
                self.height()
            ))

            painter = QPainter()
            painter.begin(self)
            painter.setFont(QFont('Arial', current_font_size))
            painter.setPen(QColor(*IDENTIFIER_FONT_COLOR))
            
            identifier_count = 0            
            for width_column_idx in range(0, current_screen_width_column_size, current_cell_width_column_size):
                for height_row_idx in range(0, current_screen_height_row_size, current_cell_height_row_size):
                    painter.drawText(current_cell_width_column_size // 2 + width_column_idx + self.x_start_in_current_screen, 
                                     current_cell_height_row_size // 2 + height_row_idx + self.y_start_in_current_screen, 
                                     str(self.get_cell_identifier(width_column_idx, height_row_idx)))
                    identifier_count += 1
            logger.debug("identifier count: {}".format(identifier_count))
            
            painter.end()

            mouse.Controller().position = (self.x_old, self.y_old)
        except Exception as e:
            logger.error('paintEvent Exception: {}'.format(e.with_traceback))
            traceback.print_exc()
        
        log_function_name_to_exit()


    def get_current_screen_size_config(self):
        return self.screen_size_config[self.screen_level]
    

    def get_current_screen_width_column_size(self):
        if self.screen_level == LEVEL_1:
            return self.desktop.screenGeometry().width()
        else:
            return self.get_current_screen_size_config()[KEY_SCREEN_WIDTH_COLUMN_SIZE]


    def get_current_screen_height_row_size(self):
        if self.screen_level == LEVEL_1:
            return self.desktop.screenGeometry().height()
        else:
            return self.get_current_screen_size_config()[KEY_SCREEN_HEIGHT_ROW_SIZE]       


    def get_current_font_size(self):
        return self.get_current_screen_size_config()[KEY_FONT_SIZE]


    def get_current_cell_width_column_size(self):
        return self.get_current_screen_size_config()[KEY_CELL_WIDTH_COLUMN_SIZE]


    def get_current_cell_height_row_size(self):
        return self.get_current_screen_size_config()[KEY_CELL_HEIGHT_ROW_SIZE]


    def get_current_identifier_key_count(self):
        return self.get_current_screen_size_config()[KEY_IDENTIFIER_KEY_COUNT]


    def quit_app(self):
        log_function_name_to_enter()

        logger.info('quit sys')
        self.hide()
        sys.exit(0)

    
    def handle_keyboard(self, e):
        log_function_name_to_enter()        

        identifier_key_count = self.get_current_identifier_key_count()
        # len - x = count - 1
        for _ in range(0, len(self.keys) - identifier_key_count + 1):
            self.keys.pop(0)
        self.keys.append(str(e.name).upper())
        if len(self.keys) == identifier_key_count and self.isVisible():
            self.move_mouse()

        log_function_name_to_exit()

    
    def get_cell_identifier(self, column_width, row_height):
        if self.screen_level == LEVEL_1:
            return string.ascii_uppercase[row_height // self.get_current_cell_height_row_size() % len(string.ascii_uppercase)] +\
                string.ascii_uppercase[column_width // self.get_current_cell_width_column_size() % len(string.ascii_uppercase)]
        elif self.screen_level == LEVEL_2:
            idx = (row_height // self.get_current_cell_height_row_size()) * CELL_COUNT_PER_WIDTH_PER_HEIGHT_LEVEL2 + \
                  (column_width // self.get_current_cell_width_column_size())
            return string.ascii_uppercase[idx % len(string.ascii_uppercase)]
    

    def get_target_mouse_position(self):
        x_position_in_current_screen = 0
        y_position_in_current_screen = 0
        current_cell_height_row_size = self.get_current_cell_height_row_size()
        current_cell_width_column_size = self.get_current_cell_width_column_size()
        if self.screen_level == LEVEL_1:
            height_row_key = str(self.keys[0]).upper()
            width_column_key = str(self.keys[1]).upper()        
            x_position_in_current_screen = string.ascii_uppercase.index(width_column_key) * current_cell_width_column_size + \
                current_cell_width_column_size // 2 + self.x_start_in_current_screen
            y_position_in_current_screen = string.ascii_uppercase.index(height_row_key) * current_cell_height_row_size + \
                current_cell_height_row_size // 2 + self.y_start_in_current_screen
        elif self.screen_level == LEVEL_2:
            key_idx = string.ascii_uppercase.index(str(self.keys[0]).upper())
            x_position_in_current_screen = (key_idx % CELL_COUNT_PER_WIDTH_PER_HEIGHT_LEVEL2) * current_cell_width_column_size + \
                current_cell_width_column_size // 2 + self.x_start_in_current_screen
            y_position_in_current_screen = (key_idx // CELL_COUNT_PER_WIDTH_PER_HEIGHT_LEVEL2) * current_cell_height_row_size + \
                current_cell_height_row_size // 2 + self.y_start_in_current_screen
        return x_position_in_current_screen + self.x_start_of_current_screen, y_position_in_current_screen + self.y_start_of_current_screen


    def is_match_hotkey(self, expect_key, actual_key):
        return len(expect_key.symmetric_difference(actual_key)) == 0


    def move_mouse(self):
        log_function_name_to_enter()

        if len(self.keys) != self.get_current_identifier_key_count():
            logger.info('exit {}: not valid key count'.format(get_current_function_name()))
            return
        
        if not self.isVisible():
            logger.info('exit {}: window is not visible'.format(get_current_function_name()))
            return
        
        logger.debug('pressed keys: {}'.format(self.keys))

        for key in self.keys:
            if not is_valid_single_alpha(key):
                logger.info('exit {}: not valid alpha key'.format(get_current_function_name()))
                return
     
        x_position, y_position = self.get_target_mouse_position()
        logger.debug(f"width column position: {x_position}; hight row position: {y_position}.")

        with mouse.Controller() as controller:
            controller.position = (x_position, y_position)
            logger.info('pressed keys: {}'.format(self.keys))
            logger.info('move mouse to ({}, {})'.format(x_position, y_position))   
        
        self.record_current_mouse_position()

        # after mouse position changed
        self.keys.clear()
        self.my_hide()
        
        log_function_name_to_exit()


    def my_hide(self):
        log_function_name_to_enter()

        # 屏幕恢复默认级别
        self.screen_level = LEVEL_DEFAULT
        self.hide()
        
        log_function_name_to_exit()
    

    def my_delayed_hide_task(self):
        log_function_name_to_enter()

        current = get_timestamp_ms()
        if current - self.latest_show_timestamp >= DELAY_HIDE_TIME * 1000:
            self.my_hide()
        else:
            logger.debug("Cancel delayed hide task.")

        log_function_name_to_exit()


    def my_delayed_hide(self):
        log_function_name_to_enter()

        timer = threading.Timer(DELAY_HIDE_TIME, self.my_delayed_hide_task)
        timer.start()
        self.executor_pool.submit(timer)

        log_function_name_to_exit()


    def set_show_latest_time(self):
        self.latest_show_timestamp = get_timestamp_ms()


    def post_show_window(self):
        self.set_show_latest_time()
        self.my_delayed_hide()


    def record_current_mouse_position(self):
        self.x_old, self.y_old = mouse.Controller().position


    def my_show_window_common(self):
        self.record_current_mouse_position()
        self.show_top_application()
        self.hide()
        self.update_current_screen()
        self.showFullScreen()
        self.handle_window_on_top()
        self.post_show_window()


    def my_show_full_window(self):
        log_function_name_to_enter()

        self.screen_level = LEVEL_1
        self.my_show_window_common()
        
        log_function_name_to_exit()

    
    def my_show_detail_window(self):
        log_function_name_to_enter()

        self.screen_level = LEVEL_2
        self.my_show_window_common()
        
        log_function_name_to_exit()


    def switch_screen(self):
        log_function_name_to_enter()

        cursor = QCursor()
        cursor_screen = self.app.screenAt(cursor.pos())
        screens = self.app.screens() 
        x_position = 0
        y_position = 0
        for screen in screens:
            if screen != cursor_screen:
                x_position = screen.geometry().left() + screen.geometry().width() // 2
                y_position = screen.geometry().top() + screen.geometry().height() // 2
                mouse.Controller().position = (x_position, y_position)
                break
        logger.info("switch screen and cursor now in ({}, {})".format(x_position, y_position))

        log_function_name_to_exit()
        

    def my_show_window_in_switched_screen(self):
        log_function_name_to_enter()

        self.screen_level = LEVEL_1
        self.switch_screen()
        self.my_show_window_common()
        
        log_function_name_to_exit()


    def my_simulate_mouse_click_left(self):
        log_function_name_to_enter()
        logger.info('left single click')
        self.my_simulate_mouse_click_common_task(mouse.Button.left, 1)
        log_function_name_to_exit()


    def my_simulate_mouse_click_left_double(self):
        log_function_name_to_enter()
        logger.info('left double click')
        self.my_simulate_mouse_click_common_task(mouse.Button.left, 2)
        log_function_name_to_exit()


    def my_simulate_mouse_click_right(self):
        log_function_name_to_enter()
        logger.info('right click')
        self.my_simulate_mouse_click_common_task(mouse.Button.right, 1)
        log_function_name_to_exit()


    def my_simulate_mouse_click_common_task(self, button, click_times):
        log_function_name_to_enter()

        if self.isVisible():
            with mouse.Controller() as controller:
                x_position, y_position = controller.position
                logger.info("save mouse position")

            self.hide()
            QApplication.processEvents()

            with mouse.Controller() as controller:
                logger.info("is visible: {}".format(self.isVisible()))
                controller.position = (x_position, y_position)
                self.keys.clear()
                controller.click(button)
                for _ in range(1, click_times):
                    time.sleep(0.2)
                    controller.click(button)

            if mouse.Button.right != button:
                self.my_show_detail_window()

            with mouse.Controller() as controller:
                controller.position = (x_position, y_position)
                logger.info("restore mouse position")
        else:
            logger.info("The mouse click operation is invalid, cause window is not visible.")

        log_function_name_to_exit()


    def handle_window_on_top(self):
        log_function_name_to_enter()
        # set top
        try:
            window_item = gw.getWindowsWithTitle(self.window_tile)[0]
            win_app = Application().connect(handle=window_item._hWnd)
            win_app.top_window().set_focus()
            logger.info('window app: {}'.format(window_item))
        except Exception as e:
            logger.error('handle_window_on_top Exception: {}'.format(e.with_traceback))
            traceback.print_exc()

        log_function_name_to_exit()


    def show_top_application(self):
        log_function_name_to_enter()

        active_window = gw.getActiveWindow()
        if active_window == None:
            logger.info('no activate window')
            log_function_name_to_exit()
            return
        top_app = Application().connect(handle=active_window._hWnd)
        pid = top_app.process
        p = psutil.Process(pid)
        exe_path = p.exe()
        exe_name = exe_path.split(os.path.sep)[-1].removesuffix('.exe').removesuffix('64')
        if "idea" == exe_name:
            logger.info('The top-level software is IntelliJ IDEA.')
        else:
            logger.info('The top-level software is {}'.format(exe_name))

        log_function_name_to_exit()
