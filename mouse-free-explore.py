
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
from pynput import mouse
import keyboard
import string
import sys
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
import time


TRANSPARENCY = 50  # 透明度
CELL_WIDTH_COLUMN_SIZE = 75  # Cell Width
CELL_HEIGHT_ROW_SIZE = 45  # Cell Height
DELAY_HIDE_TIME = 5
FONT_SIZE = 12  # 字体大小
SHOW_INTERVAL = 5 * 1000  # 定时器间隔（毫秒 = 秒 * 1000）
BACKGROUND_COLOR = (173, 216, 230)  # 背景：浅蓝色
KEYBOARD_SHOW_HOTKEY = 'ctrl + alt + space'
KEYBOARD_SHOW_DETAIL_HOTKEY = 'ctrl + alt + shift'
KEYBOARD_HIDE_HOTKEY = 'esc'
KEYBOARD_MOUSE_CLICK_LEFT_HOTKEY = 'ctrl + alt + enter'
KEYBOARD_QUIT_HOTKEY = 'ctrl + alt + q'
TOGGLE_SHOW_HOTKEY = {"CTRL", "ALT"}
LOG_FILE_PATH = 'mouse-free.log'
THREAD_POOL_MAX_WORKERS = 5


def get_timestamp_ms():
    return time.time() * 1000


def get_current_function_name():
    return sys._getframe(1).f_code.co_name


def log_function_name_to_enter():
    logger.debug('enter function: {}'.format(sys._getframe(1).f_code.co_name))


def log_function_name_to_exit():
    logger.debug('exit function: {}'.format(sys._getframe(1).f_code.co_name))


def is_valid_single_alpha(key):
    return len(str(key)) == 1 and str(key).isalpha()

def config_logger():
    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    # Create a console handler and a file handler
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(LOG_FILE_PATH)

    # Create a formatter and attach it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Attach the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Create a logger
logger = config_logger()


class MyWindow(QWidget):
    def __init__(self):
        log_function_name_to_enter()

        super(MyWindow, self).__init__()

        self.executor_pool = ThreadPoolExecutor(max_workers=THREAD_POOL_MAX_WORKERS)

        self.init_ui()

        self.keys = []

        # 监听键盘，独立线程
        self.keyboard_listener = KeyboardListener(logger)
        self.keyboard_listener.key_pressed_signal.connect(self.handle_keyboard)
        self.keyboard_listener.quit_signal.connect(self.quit_app)        
        self.keyboard_listener.show_signal.connect(self.my_show)
        self.keyboard_listener.show_detail_signal.connect(self.my_show_detail)
        self.keyboard_listener.hide_signal.connect(self.my_hide) 
        self.keyboard_listener.simulate_mouse_click_left_signal.connect(self.my_simulate_mouse_click_left)       
        self.keyboard_listener.start()

        log_function_name_to_exit()


    def init_ui(self):
        log_function_name_to_enter()

        self.setWindowOpacity(TRANSPARENCY / 100)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        p = self.palette()
        bg_color = QColor(*BACKGROUND_COLOR)
        p.setColor(self.backgroundRole(), bg_color)
        self.setPalette(p)
        self.showFullScreen()
        # 隐藏窗口在任务栏的展示
        self.setWindowFlags(Qt.Tool)
        self.set_show_latest_time()
        self.my_delayed_hide()

        log_function_name_to_exit()
     
        
    def paintEvent(self, event):
        log_function_name_to_enter()

        try:
            painter = QPainter()
            painter.begin(self)
            painter.setFont(QFont('Arial', FONT_SIZE))       

            identifier_count = 0
            for width_column_idx in range(0, self.width(), CELL_WIDTH_COLUMN_SIZE):
                for height_row_idx in range(0, self.height(), CELL_HEIGHT_ROW_SIZE):
                    painter.drawText(width_column_idx + CELL_WIDTH_COLUMN_SIZE // 2 + FONT_SIZE, 
                                     height_row_idx + CELL_HEIGHT_ROW_SIZE // 2 + FONT_SIZE, 
                                     str(self.get_cell_identifier(width_column_idx, height_row_idx)))
                    identifier_count += 1
            logger.info("identifier count: {}".format(identifier_count))
            
            painter.end()
        except Exception as e:
            logger.error('paintEvent Exception: {}'.format(e.with_traceback))
        
        log_function_name_to_exit()


    def quit_app(self):
        log_function_name_to_enter()

        QApplication.quit()

        log_function_name_to_exit()

    
    def handle_keyboard(self, e):
        log_function_name_to_enter()

        del self.keys[0:-1]
        self.keys.append(str(e.name).upper())
        if len(self.keys) == 2 and self.isVisible():
            self.move_mouse()

        log_function_name_to_exit()

    
    def get_cell_identifier(self, column_width, row_height):
        return string.ascii_uppercase[(row_height // CELL_HEIGHT_ROW_SIZE)] + string.ascii_uppercase[(column_width // CELL_WIDTH_COLUMN_SIZE)]
    

    def is_match_hotkey(self, expect_key, actual_key):
        return len(expect_key.symmetric_difference(actual_key)) == 0


    def move_mouse(self):
        log_function_name_to_enter()

        if len(self.keys) != 2:
            logger.info('exit {}: not valid key count'.format(get_current_function_name()))
            return
        
        height_row_key = str(self.keys[0]).upper()
        width_column_key = str(self.keys[1]).upper()
        logger.info('width_key {} is_valid_single_alpha(): {}'.format(width_column_key, is_valid_single_alpha(width_column_key)))
        logger.info('hight_key {} is_valid_single_alpha(): {}'.format(height_row_key, is_valid_single_alpha(height_row_key)))
        
        if (not is_valid_single_alpha(width_column_key)) or (not is_valid_single_alpha(height_row_key)):
            logger.info('exit {}: not valid alpha key'.format(get_current_function_name()))
            return
        
        logger.info(f'width column key: {width_column_key}; hight row key: {height_row_key}.')
        x_position = string.ascii_uppercase.index(width_column_key) * CELL_WIDTH_COLUMN_SIZE + CELL_WIDTH_COLUMN_SIZE // 2
        y_position = string.ascii_uppercase.index(height_row_key) * CELL_HEIGHT_ROW_SIZE + CELL_HEIGHT_ROW_SIZE // 2
        logger.info(f"width column position: {x_position}; hight row position: {y_position}.")
        with mouse.Controller() as controller:
            controller.position = (x_position, y_position)
            logger.info('move mouse to ({}, {})'.format(x_position, y_position))   
        self.keys.clear()

        self.my_hide()
        
        log_function_name_to_exit()


    def log_window_status(self, window):
        logger.debug('window isWindow: {}'.format(window.isWindow()))
        logger.debug('window isActiveWindow: {}'.format(window.isActiveWindow()))
        logger.debug('window isFullScreen: {}'.format(window.isFullScreen()))
        logger.debug('window isVisible: {}'.format(window.isVisible()))  


    def my_hide(self):
        log_function_name_to_enter()
        self.log_window_status(self)

        self.hide()
        
        log_function_name_to_exit()
    

    def my_delayed_hide_task(self):
        log_function_name_to_enter()

        current = get_timestamp_ms()
        if current - self.latest_show_timestamp >= DELAY_HIDE_TIME * 1000:
            self.my_hide()
        else:
            logger.info("Cancel delayed hide task.")

        log_function_name_to_exit()


    def my_delayed_hide(self):
        timer = threading.Timer(DELAY_HIDE_TIME, self.my_delayed_hide_task)
        timer.start()
        self.executor_pool.submit(timer)


    def set_show_latest_time(self):
        self.latest_show_timestamp = get_timestamp_ms()


    def my_show(self):
        log_function_name_to_enter()
        self.log_window_status(self)

        self.showFullScreen()
        self.set_show_latest_time()
        self.my_delayed_hide()
        
        log_function_name_to_exit()


    def my_simulate_mouse_click_left(self):
        log_function_name_to_enter()

        if self.isVisible():
            self.my_hide()
            mouse.Controller().click(mouse.Button.left)
        else:
            logger.info("The left mouse click operation is invalid, cause window is not visible.")

        log_function_name_to_exit()

    
    def my_show_detail(self):
        log_function_name_to_enter()
        self.log_window_status(self)

        x, y = mouse.Controller().position
        DETAIL_CELL_LENGTH = 300
        self.setGeometry(x - DETAIL_CELL_LENGTH // 2, y - DETAIL_CELL_LENGTH // 2, DETAIL_CELL_LENGTH, DETAIL_CELL_LENGTH)
        self.show()
        self.set_show_latest_time()
        self.my_delayed_hide()
        
        log_function_name_to_exit()


class KeyboardListener(QThread):
    show_signal = pyqtSignal()
    show_detail_signal = pyqtSignal()
    hide_signal = pyqtSignal()
    quit_signal = pyqtSignal()
    key_pressed_signal = pyqtSignal(object)
    simulate_mouse_click_left_signal = pyqtSignal()
    

    def __init__(self, logger):
        super(KeyboardListener, self).__init__()
        self.logger = logger
        
        keyboard.on_press(self.async_key_press)
        keyboard.add_hotkey(KEYBOARD_SHOW_HOTKEY, self.async_show_window)
        keyboard.add_hotkey(KEYBOARD_SHOW_DETAIL_HOTKEY, self.async_show_detail_window)
        keyboard.add_hotkey(KEYBOARD_HIDE_HOTKEY, self.async_hide_window)
        keyboard.add_hotkey(KEYBOARD_QUIT_HOTKEY, self.async_quit)
        keyboard.add_hotkey(KEYBOARD_MOUSE_CLICK_LEFT_HOTKEY, self.async_simulate_mouse_click_left)
        

    
    def async_show_window(self):
        log_function_name_to_enter()

        self.show_signal.emit()

        log_function_name_to_exit()


    def async_hide_window(self):
        log_function_name_to_enter()

        self.hide_signal.emit()

        log_function_name_to_exit()


    def async_show_detail_window(self):
        log_function_name_to_enter()

        self.show_detail_signal.emit()

        log_function_name_to_exit()

    
    def async_quit(self):
        log_function_name_to_enter()

        self.quit_signal.emit()

        log_function_name_to_exit()


    def async_key_press(self, event):
        log_function_name_to_enter()
        logger.debug('enter async_key_press: {}'.format(event.name))

        self.key_pressed_signal.emit(event)

        log_function_name_to_exit()

    
    def async_simulate_mouse_click_left(self):
        log_function_name_to_enter()

        self.simulate_mouse_click_left_signal.emit()

        log_function_name_to_exit()


    def run(self):
        log_function_name_to_enter()
        
        logger.info('Thread is running...')

        log_function_name_to_exit()         



if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyWindow()

    sys.exit(app.exec_())

