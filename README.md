### Email Receipts
A simple software for creating retail invoices and sending them to a customer over mail. Requires an Arduino!

### Requirements
- Gmail account and [Gmail API project](https://developers.google.com/gmail/api/quickstart/python) and related files. Store in `client_secret.json`.
- Arduino Uno, HC-05 Bluetooth module, male-male and female-male jumper cables, LED, resistor.
- Arduino IDE. 
- Account on [MIT App Inventor](http://appinventor.mit.edu/explore/).
- Python requirements: `qrcode` , `pyserial` , and any others required by `mail.py`. 

### Set Up Procdedure
1. On terminal, run `git clone https://github.com/anushreehede/EmailReceipts.git` to clone this repository. 
2. Set up the Gmail API. Save the client secret files. On line 13 in `main.py`, place the same Gmail account ID. 
3. Import the file `BarCode_Scanner.aia` on your MIT App Inventor as a new project. Go to Build and save the `.apk` file onto your phone. 
4. Set up the Arduino, HC-05 Bluetooth module, LED, resistor and wires as shown [here](https://maker.pro/arduino/tutorial/bluetooth-basics-how-to-control-led-using-smartphone-arduino). Connect the Arduino cable to the serial port and accordingly change line 16 in `main.py` with the correct serial port name.
5. Upload the Arduino code `sketch_feb03a_first_MITapp.ino` to Arduino using the Arduino IDE. 

### Run 
1. Connect the Arduino cable to the correct serial port on your system. 
2. Open the app, turn on Bluetooth and connect your phone's Bluetooth to the HC-05.
3. Run `python main.py` and follow the instructions as shown. Add stock items and price, before you begin to create bills. 
4. Customer database stored in `Customers.txt`, items database stored in `Items.txt` and current receipt stored in `Receipts.txt`.
5. To add an item to the customer's bill, scan an item's QR code and click send. Wait for the LED to blink, and the item will be read by the application. 
6. Once the customer had been billed, he will receive an email with the invoice of his purchases.  

### TODO
- Create a proper database for item id, item name, price, QR code
- Create a GUI for this 
- Design the app 
- Design the email which is sent 
