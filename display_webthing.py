import sys
from typing import List
from webthing import (SingleThing, Property, Thing, Value, WebThingServer)
from RPLCD.i2c import CharLCD, BaseCharLCD
from smbus2 import SMBus
from display import Display
import tornado.ioloop
import logging


class DisplayWebThing(Thing):
    # regarding capabilities refer https://iot.mozilla.org/schemas
    # there is also another schema registry http://iotschema.org/docs/full.html not used by webthing

    def __init__(self, name: str, lcd: BaseCharLCD):
        Thing.__init__(
            self,
            'urn:dev:ops:lcddisplay-1',
            'Display ' + name,
            ['Display'],
            'display of' + name
        )

        self.display = Display(lcd, self.__update_text)

        self.display_text = Value("")
        self.add_property(
            Property(self,
                     'displayed_text',
                     self.display_text,
                     metadata={
                         'title': 'Displayed text',
                         'type': 'string',
                         'description': 'Displayed text',
                         'readOnly': True,
                     }))

        self.upper_layer_text = Value("", self.display.panel(Display.LAYER_UPPER).update_text)
        self.add_property(
            Property(self,
                     'upper_layer_text',
                     self.upper_layer_text,
                     metadata={
                         'title': 'Upper layer text',
                         'type': 'string',
                         'description': 'The text of the upper layer',
                         'readOnly': False,
                     }))

        self.upper_layer_text_ttl = Value(-1, self.display.panel(Display.LAYER_UPPER).update_ttl)
        self.add_property(
            Property(self,
                     'upper_layer_text_ttl',
                     self.upper_layer_text_ttl,
                     metadata={
                         'title': 'Upper layer text (time-to-live)',
                         'type': 'integer',
                         'description': 'The time-to-live of the upper layer. Value -1 deactivates ttl',
                         'readOnly': False,
                     }))

        self.middle_layer_text = Value("", self.display.panel(Display.LAYER_MIDDLE).update_text)
        self.add_property(
            Property(self,
                     'middle_layer_text',
                     self.middle_layer_text,
                     metadata={
                         'title': 'Middle layer text',
                         'type': 'string',
                         'description': 'The text of the middle layer',
                         'readOnly': False,
                     }))

        self.middle_layer_text_ttl = Value(-1, self.display.panel(Display.LAYER_MIDDLE).update_ttl)
        self.add_property(
            Property(self,
                     'middle_layer_text_ttl',
                     self.middle_layer_text_ttl,
                     metadata={
                         'title': 'Middle layer text (time-to-live)',
                         'type': 'integer',
                         'description': 'The time-to-live of the middle layer. Value -1 deactivates ttl',
                         'readOnly': False,
                     }))

        self.lower_layer_text = Value("", self.display.panel(Display.LAYER_LOWER).update_text)
        self.add_property(
            Property(self,
                     'lower_layer_text',
                     self.lower_layer_text,
                     metadata={
                         'title': 'Lower layer text',
                         'type': 'string',
                         'description': 'The text of the lower layer',
                         'readOnly': False,
                     }))

        self.lower_layer_text_ttl = Value(-1, self.display.panel(Display.LAYER_LOWER).update_ttl)
        self.add_property(
            Property(self,
                     'lower_layer_text_ttl',
                     self.lower_layer_text_ttl,
                     metadata={
                         'title': 'Lower layer text (time-to-live)',
                         'type': 'integer',
                         'description': 'The time-to-live of the lower layer. Value -1 deactivates ttl',
                         'readOnly': False,
                     }))

        self.ioloop = tornado.ioloop.IOLoop.current()


    def __update_text(self):
        self.ioloop.add_callback(self.__update_text_props)

    def __update_text_props(self):
        self.display_text.notify_of_external_update(self.display.text)
        self.upper_layer_text.notify_of_external_update(self.display.panel(Display.LAYER_UPPER).text)
        self.upper_layer_text_ttl.notify_of_external_update(self.display.panel(Display.LAYER_UPPER).ttl)
        self.middle_layer_text.notify_of_external_update(self.display.panel(Display.LAYER_MIDDLE).text)
        self.middle_layer_text_ttl.notify_of_external_update(self.display.panel(Display.LAYER_MIDDLE).ttl)
        self.lower_layer_text.notify_of_external_update(self.display.panel(Display.LAYER_LOWER).text)
        self.lower_layer_text_ttl.notify_of_external_update(self.display.panel(Display.LAYER_LOWER).ttl)



def scan_device_names(bus: int) -> List[str]:
    devices = []
    try:
        bus = SMBus(bus)
        for device in range(128):
            try:
                bus.read_byte(device)
                devices.append(hex(device))
            except:
                pass
    except FileNotFoundError as e:
        print("WARNING: I2C seems not to be activated")
    return devices


def create_lcd(i2c_expander: str, i2c_address_hex: int) -> BaseCharLCD:
    try:
        logging.info("binding driver to address " + hex(i2c_address_hex) + " using port expander " + i2c_expander)
        return CharLCD(i2c_expander, i2c_address_hex)
    except Exception as e:
        logging.error("binding driver failed " + str(e))
        logging.info("available devices on /dev/i2c-1", ", ".join(scan_device_names(1)))  # 1 indicates /dev/i2c-1
        raise e


def run_server(port: int, name:str, i2c_expander: str, i2c_address_hex: int):
    display_webthing = DisplayWebThing(name, create_lcd(i2c_expander, i2c_address_hex))
    server = WebThingServer(SingleThing(display_webthing), port=port, disable_host_validation=True)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('done')

def string_to_hex(hexString: str) -> int:
    if hexString.startswith("0x"):
        return int(hexString, 16)
    else:
        return int(hexString)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(name)-20s: %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger('tornado.access').setLevel(logging.ERROR)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
    run_server(port=int(sys.argv[1]), name=sys.argv[2], i2c_expander=sys.argv[3], i2c_address_hex=string_to_hex(sys.argv[4]))
