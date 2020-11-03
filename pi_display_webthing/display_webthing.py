from webthing import (SingleThing, Property, Thing, Value, WebThingServer)
from pi_display_webthing.display import Display
from pi_display_webthing.lcd import Lcd
import tornado.ioloop
import logging


class DisplayWebThing(Thing):
    # regarding capabilities refer https://iot.mozilla.org/schemas
    # there is also another schema registry http://iotschema.org/docs/full.html not used by webthing

    def __init__(self, name: str, port_expander_name: str, address: str, num_lines: int, num_chars_per_line: int, description: str):
        Thing.__init__(
            self,
            'urn:dev:ops:display-1',
            (name + ' Display').strip(),
            ['Display'],
            description
        )

        self.display = Display(Lcd(port_expander_name, address, num_lines, num_chars_per_line), self.__update_text)

        self.text = Value("")
        self.add_property(
            Property(self,
                     'text',
                     self.text,
                     metadata={
                         'title': 'text',
                         'type': 'string',
                         'description': 'The displayed text',
                         'readOnly': True,
                     }))

        self.upper_layer_text = Value("", self.display.panel(Display.LAYER_UPPER).update_text)
        self.add_property(
            Property(self,
                     'upper_layer_text',
                     self.upper_layer_text,
                     metadata={
                         'title': 'upper layer text',
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
                         'title': 'upper layer text (time-to-live)',
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
                         'title': 'middle layer text',
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
                         'title': 'middle layer text (time-to-live)',
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
                         'title': 'lower layer text',
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
                         'title': 'lower layer text (time-to-live)',
                         'type': 'integer',
                         'description': 'The time-to-live of the lower layer. Value -1 deactivates ttl',
                         'readOnly': False,
                     }))

        self.ioloop = tornado.ioloop.IOLoop.current()


    def __update_text(self):
        self.ioloop.add_callback(self.__update_text_props)

    def __update_text_props(self):
        self.text.notify_of_external_update(self.display.text)
        self.upper_layer_text.notify_of_external_update(self.display.panel(Display.LAYER_UPPER).text)
        self.upper_layer_text_ttl.notify_of_external_update(self.display.panel(Display.LAYER_UPPER).ttl)
        self.middle_layer_text.notify_of_external_update(self.display.panel(Display.LAYER_MIDDLE).text)
        self.middle_layer_text_ttl.notify_of_external_update(self.display.panel(Display.LAYER_MIDDLE).ttl)
        self.lower_layer_text.notify_of_external_update(self.display.panel(Display.LAYER_LOWER).text)
        self.lower_layer_text_ttl.notify_of_external_update(self.display.panel(Display.LAYER_LOWER).ttl)


def run_server(hostname: str, port: int, name:str, port_expander_name: str, address: str, num_lines: int, num_chars_per_line: int, description: str):
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    display_webthing = DisplayWebThing(name, num_lines, port_expander_name, address, num_chars_per_line, description)
    server = WebThingServer(SingleThing(display_webthing), hostname=hostname, port=port)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('done')
