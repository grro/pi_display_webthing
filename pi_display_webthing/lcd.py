from RPLCD.i2c import CharLCD


class Lcd:

    def __init__(self, port_expander_name: str, address: str, num_lines: int, num_chars_per_line: int):
        self.char_lcd = CharLCD(port_expander_name, address)
        self.num_lines = num_lines
        self.num_chars_per_line = num_chars_per_line

    def write(self, text):
        self.char_lcd.clear()
        self.char_lcd.write_string(text)