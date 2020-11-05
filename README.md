# pi_display_webthing
A web connected LCD display module 

This project provides a [webthing API](https://iot.mozilla.org/wot/) to an I2C LCD module such as a [HD44780 1602 LCD Module](https://amzn.to/2TffbbL) on the Raspberry Pi. 
As a webthing, the LCD can be discovered and controlled by *home automation systems* or custom solutions supporting the webthing API.  

The pi_display_webthing exposes an http webthing endpoint which supports controlling the display via http. E.g. 
```
# webthing has been started on host 192.168.0.23

curl http://192.168.0.23:8070/properties 

{
    "text": "NAS error!",
    "upper_layer_text": "NAS error!",
    "upper_layer_text_ttl": -1,
    "middle_layer_text": "uploaded: 41",
    "middle_layer_text_ttl": -1,
    "lower_layer_text": "",
    "lower_layer_text_ttl": -1
}
```
Here, the text *NAS error!* will be displayed. The text of the middle layer *uploaded: 41* will be covered by the upper layer. 
If the text of the upper layer will be cleaned, the displayed text is *uploaded: 41*. 
By setting the ttl of the layer, the text of the layer will be disappear after expiration of the ttl. Value -1 means that ttl is deactivated. 

A RaspberryPi/LCD hardware setup and wiring may look like [HD44780 1602 LCD module](docs/layout.png). By default, 
Raspberry Pi OS disables I2C. Please refer [Configure I2C](docs/configure_i2c.md) to activate I2C and to 
detect the address of the LCD module.

To install pi_display_webthing you may use [PIP](https://realpython.com/what-is-pip/) package manager such as shown below
```
sudo pip install pi_display_webthing
```

After this installation you may start the webthing http endpoint inside your python code or via command line using
```
sudo display --command listen --hostname 192.168.0.23 --port 8070 --i2c_expander PCF8574 --i2c_address 0x27 --num_lines 2 --num_chars 16
```
Here, the webthing API will be bind to hostname 192.168.0.23 on the local port 8070 using a 2/16 display layout on address 0x27. 
Further more the port I2C port expander name has to be set. The expander name should be written on the microchip. 
Supported port expanders are *PCF8574*, *MCP23008* and *MCP23017*

Alternatively to the *listen* command, you can use the *register* command to register and start the webthing service as systemd unit. 
By doing this the webthing service will be started automatically on boot. Starting the server manually using the *listen* command is no longer necessary. 
```
sudo display --command register --hostname 192.168.0.23 --port 8070 --i2c_expander PCF8574 --i2c_address 0x27 --num_lines 2 --num_chars 16
```  
