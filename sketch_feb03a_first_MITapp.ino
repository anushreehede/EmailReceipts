/* Arduino and HC-05 Bluetooth Module Tutorial
 * 
 * by Dejan Nedelkovski, www.HowToMechatronics.com
 * 
 */
 
#define ledPin 7
String state = " ";
void setup() 
{
 pinMode(ledPin, OUTPUT);
 digitalWrite(ledPin, LOW);
 Serial.begin(9600); // Default communication rate of the Bluetooth module
}
void loop() {
 if(Serial.available() > 0)
 { // Checks whether data is comming from the serial port
  state = Serial.readString(); // Reads the data from the serial port
 }
 if (state != " ") 
 {
  digitalWrite(ledPin, HIGH); // Turn LED ON
  Serial.println(state); // Send back, to the phone, the String "LED: ON"
  state = " ";
  delay(2000);
  digitalWrite(ledPin, LOW);
  
 } 
}
