# pi_display_webthing
A web connected LCD display module 

This project provides a [webthing API](https://iot.mozilla.org/wot/) to an I2C LCD module such as a [HD44780 1602 LCD Module](https://www.amazon.de/dp/B01N3B8JMN/ref=cm_sw_em_r_mt_dp_Mh6NFbGT9V02Z) on the Raspberry Pi. 
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

A RaspberryPi/LCD hardware setup and wiring may look like [HD44780 1602 LCD module](docs/layout.png). By default, 
Raspberry Pi OS disables I2C. Please refer [Configure I2C](docs/configure_i2c.md) to activate I2C as and to 
detect the address of the LCD module.

To install pi_display_webthing you may use [PIP](https://realpython.com/what-is-pip/) package manager such as shown below
```
sudo pip install pi_display_webthing
```

After this installation you may start the webthing http endpoint inside your python code or via command line using
```
sudo display --command listen --hostname 192.168.0.23 --port 8070 --expander PCF8574 --address 0x27 --num_lines 2 --num_chars 16
```
Here, the webthing API will be bind to hostname 192.168.0.23 on the local port 8070 using a 2/16 display layout on address 0x27. 
Further more the port I²C port expander name has to be set. The expander name should be written on the microchip. 
Supported port expanders are *PCF8574*, *MCP23008* and *MCP23017*

Alternatively to the *listen* command, you can use the *register* command to register and start the webthing service as systemd unit. 
By doing this the webthing service will be started automatically on boot. Starting the server manually using the *listen* command is no longer necessary. 
```
sudo display --command register --hostname 192.168.0.23 --port 8070 --expander PCF8574 --address 0x27 --num_lines 2 --num_chars 16
```  
