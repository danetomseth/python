byte number = 0;
int inbyte;
unsigned long serialdata;

void setup(){
Serial.begin(9600);
}

void loop(){
//if (Serial.available()) {
//number = Serial.read();
//Serial.print("character recieved: ");
//Serial.println(number, DEC);
//}
getSerial();
  switch(serialdata)
  {
  case 1:
    {
      Serial.println("CASE 1");
      break;
    }
   case 2: 
   {
    Serial.println("CASE 2");
    break;
   }
   default: {
    Serial.println("DEFAULT");
   }
  }
}



long getSerial()
{
  serialdata = 0;
  while (inbyte != '/')
  {
    inbyte = Serial.read(); 
    if (inbyte > 0 && inbyte != '/')
    {
     
      serialdata = serialdata * 10 + inbyte - '0';
    }
  }
  inbyte = 0;
  return serialdata;
}
