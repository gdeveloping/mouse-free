from PyQt5.QtCore import QThread, pyqtSignal
import keyboard
from utils import *
from properties import *
from log_utils import *


class KeyboardListener(QThread):
    show_signal = pyqtSignal()
    show_detail_signal = pyqtSignal()
    show_in_switched_screen_signal = pyqtSignal();
    hide_signal = pyqtSignal()
    quit_signal = pyqtSignal()
    key_pressed_signal = pyqtSignal(object)
    simulate_mouse_click_left_signal = pyqtSignal()
    simulate_mouse_click_left_double_signal = pyqtSignal()
    simulate_mouse_click_right_signal = pyqtSignal()

    def __init__(self, logger):
        super(KeyboardListener, self).__init__()
        self.logger = logger

        self.signal_hotkey_map = {
            self.show_signal: KEYBOARD_SHOW_HOTKEY,
            self.show_detail_signal: KEYBOARD_SHOW_DETAIL_HOTKEY,
            self.show_in_switched_screen_signal: KEYBOARD_SHOW_IN_SWITCHED_SCREEN_HOTKEY,
            self.hide_signal: KEYBOARD_HIDE_HOTKEY,
            self.quit_signal: KEYBOARD_QUIT_HOTKEY,
            self.simulate_mouse_click_left_signal: KEYBOARD_MOUSE_CLICK_LEFT_HOTKEY,
            self.simulate_mouse_click_left_double_signal: KEYBOARD_MOUSE_CLICK_LEFT_DOUBLE_HOTKEY,
            self.simulate_mouse_click_right_signal: KEYBOARD_MOUSE_CLICK_RIGHT_HOTKEY            
        }
        
        keyboard.on_press(self.async_key_press)
        keyboard.add_hotkey(KEYBOARD_SHOW_HOTKEY, self.async_show_window)
        keyboard.add_hotkey(KEYBOARD_SHOW_DETAIL_HOTKEY, self.async_show_detail_window)
        keyboard.add_hotkey(KEYBOARD_SHOW_IN_SWITCHED_SCREEN_HOTKEY, self.async_show_window_in_switched_screen)
        keyboard.add_hotkey(KEYBOARD_HIDE_HOTKEY, self.async_hide_window)
        keyboard.add_hotkey(KEYBOARD_QUIT_HOTKEY, self.async_quit)
        keyboard.add_hotkey(KEYBOARD_MOUSE_CLICK_LEFT_HOTKEY, self.async_simulate_mouse_click_left)
        keyboard.add_hotkey(KEYBOARD_MOUSE_CLICK_LEFT_DOUBLE_HOTKEY, self.async_simulate_mouse_click_left_double)
        keyboard.add_hotkey(KEYBOARD_MOUSE_CLICK_RIGHT_HOTKEY, self.async_simulate_mouse_click_right)
     

    def async_show_window(self):
        log_function_name_to_enter()

        keyboard.release(self.signal_hotkey_map[self.show_signal])
        self.show_signal.emit()

        log_function_name_to_exit()


    def async_hide_window(self):
        log_function_name_to_enter()

        keyboard.release(self.signal_hotkey_map[self.hide_signal])
        self.hide_signal.emit()

        log_function_name_to_exit()


    def async_show_detail_window(self):
        log_function_name_to_enter()

        keyboard.release(self.signal_hotkey_map[self.show_detail_signal])
        self.show_detail_signal.emit()

        log_function_name_to_exit()
    
    
    def async_show_window_in_switched_screen(self):
        log_function_name_to_enter()

        keyboard.release(self.signal_hotkey_map[self.show_in_switched_screen_signal])
        self.show_in_switched_screen_signal.emit()

        log_function_name_to_exit()

    
    def async_quit(self):
        log_function_name_to_enter()

        keyboard.release(self.signal_hotkey_map[self.quit_signal])
        self.quit_signal.emit()

        log_function_name_to_exit()


    def async_key_press(self, event):
        log_function_name_to_enter()
        logger.debug('enter async_key_press: {}'.format(event.name))

        self.key_pressed_signal.emit(event)

        log_function_name_to_exit()

    
    def async_simulate_mouse_click_left(self):
        log_function_name_to_enter()

        keyboard.release(self.signal_hotkey_map[self.simulate_mouse_click_left_signal])
        self.simulate_mouse_click_left_signal.emit()

        log_function_name_to_exit()


    def async_simulate_mouse_click_left_double(self):
        log_function_name_to_enter()

        keyboard.release(self.signal_hotkey_map[self.simulate_mouse_click_left_double_signal])
        self.simulate_mouse_click_left_double_signal.emit()

        log_function_name_to_exit()

    
    def async_simulate_mouse_click_right(self):
        log_function_name_to_enter()

        keyboard.release(self.signal_hotkey_map[self.simulate_mouse_click_right_signal])
        self.simulate_mouse_click_right_signal.emit()

        log_function_name_to_exit()


    def run(self):
        log_function_name_to_enter()
        
        logger.info('Thread is running...')

        log_function_name_to_exit()         

