#include <Wire.h>
#include <MPU6050.h>
#include <TinyGPS.h>
#include <LiquidCrystal.h>
#include <SoftwareSerial.h>
SoftwareSerial mySerial(10,11);  // RX, TX    GSM

LiquidCrystal lcd(7, 6, 5, 4, 3 , 2);

MPU6050 mpu;

int16_t ax, ay, az;
int16_t gx, gy, gz;

long X, Y, Z;
  
String stringVal = "";     //data on buff is copied to this string
String stringVal1 = "";     //data on buff is copied to this string

String lat1 = " 111";     //data on buff is copied to this string
String lat2 = "222";     //data on buff is copied to this string
String lat3 = "222";     //data on buff is copied to this string
String lat4 = "222";     //data on buff is copied to this string
 
String lon1 = "11";     //data on buff is copied to this string
String lon2 = "11";     //data on buff is copied to this string
String lon3 = "11";     //data on buff is copied to this string
String lon4 = "11";     //data on buff is copied to this string
 
float flat, flon;
unsigned long age;
char getData,dest=0;
char charVal[6];               //temporarily holds data from vals 
char SelectSMS[100]="  ";

#define motor_Pin  9
#define led_RPin  A1
      
int buz = 8;

char Mob1[20]="+923066211079";

boolean flag1 = false;
TinyGPS gps;
bool newData = false;

void setup()
{
  Serial.begin(9600);
  mySerial.begin(9600);
  mpu.initialize();
  lcd.begin(16, 2);
  
  lcd.clear();lcd.setCursor(0,0);
  lcd.print("  WELL COME ");
  delay(2000);
  lcd.clear();lcd.setCursor(0,0);  
  
  lcd.print("  Project Adviser: ");
  delay(2000);
  lcd.clear();lcd.setCursor(0,0);
  
  lcd.print("Ma'am Zahra Ali ");
  delay(2000);
  lcd.clear();lcd.setCursor(0,0);
  
  lcd.print("UMT Sialkot ");
  delay(2000);
  lcd.clear();lcd.setCursor(0,0);
  
  lcd.print("PROJECT TITLE");
  delay(2000);
  lcd.clear();
  lcd.setCursor(0,0);
  
  lcd.print("  Accident Life Rescue  ");
  lcd.setCursor(0,1);
  lcd.print("System Using ML ");
  delay(2000);
  
  lcd.clear();
  
  pinMode(motor_Pin, OUTPUT);  
  pinMode(led_RPin, OUTPUT); 
  pinMode(buz, OUTPUT);
  
  digitalWrite(led_RPin, HIGH);
  digitalWrite(buz, LOW);
  delay(1000);
  digitalWrite(buz, HIGH);

  lcd.clear();lcd.setCursor(0,0);
  lcd.print("Configured ...");
  delay(2000); 
  lcd.clear();
  

}



void loop()
{
  get_gps();
  delay(300);                               

 mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
 X = map(ax, -17000, 17000, 0, 999);
 Y = map(ay, -17000, 17000, 0, 999);
 Z = map(az, -17000, 17000, 0, 90);

// Serial.print("X="); Serial.println(X);
// Serial.print("Y="); Serial.println(Y); 
 
  chk(); //delay(100);
  
  lcd.setCursor(0,0);
  lcd.print("X:");
  lcd.print(X);
  lcd.print("  Y:");
  lcd.print(Y);  

 delay(100);

}

void chk()
{ 

if(Y<400 || Y>700 || X<250 || X>750)
{

 digitalWrite(motor_Pin, LOW);
 digitalWrite(buz, LOW);  
 
 lcd.clear();
 lcd.print("ACCIDENT OCCURED ");
 Serial.print ("ACCIDENT OCCURED");
 
 delay(1000);
 digitalWrite(buz, HIGH);
 sms1(flat,flon);
 delay(5000);
 lcd.clear();
//digitalWrite(buz, HIGH);
digitalWrite(led_RPin, HIGH);
digitalWrite(buz, HIGH);
}

 if(Y>450 && Y<700 && X>300 && X<650)
 {
  digitalWrite(buz, HIGH);
  digitalWrite(motor_Pin, HIGH); 

} 
}


void sms1(float a,float b)
{
 mySerial.println("AT");   delay(1000);
  mySerial.write("AT+CMGF=1\r\n");           //set GSM to text mode
  delay(500);

   mySerial.print("AT+CMGS=\"");
   mySerial.print(Mob1);
   mySerial.print("\"\r");
  // Serial.println("Send Message");
  delay(1500);
  mySerial.println("EMERGENCY ALERT");
  mySerial.println("ACCIDENT OCCURED");
  mySerial.println("Need for Rescue at ");
  mySerial.print(a, 4);
   mySerial.print(",");
  
   mySerial.print(b, 4);
   delay(2000); 
   mySerial.write(0x1A);           // sends ctrl+z end of message 
   delay(1500);
    
  lcd.print("sms sent ");
  Serial.println("SMS Sent");
  delay(2000); 
  lcd.clear();
}


void get_gps(){
  // For one second we parse GPS data and report some key values
  for (unsigned long start = millis(); millis() - start < 1000;)
  {
    while (Serial.available())
    {
      char c = Serial.read();
      if (gps.encode(c)) // Did a new valid sentence come in?
        newData = true;
    }
  }

  if (newData)
  {
    gps.f_get_position(&flat, &flon, &age);
    Serial.print("LAT=");
    Serial.print(flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flat, 3);
    Serial.print(" LON=");
    Serial.print(flon == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flon, 6);
    Serial.print(" SAT=");
    Serial.print(gps.satellites() == TinyGPS::GPS_INVALID_SATELLITES ? 0 : gps.satellites());
    Serial.print(" PREC=");
    Serial.print(gps.hdop() == TinyGPS::GPS_INVALID_HDOP ? 0 : gps.hdop());
    lcd.setCursor(0,0);
    lcd.print("LAT= ");
    lcd.setCursor(5,0);     lcd.print(flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flat, 4);
    lcd.setCursor(0,1);
    lcd.print("LON= ");
    lcd.setCursor(5,1);     lcd.print(flon == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flon, 4);


   stringVal="";
   stringVal1="";

 dtostrf(flon, 4, 3, charVal);  //4 is mininum width, 3 is precision; float value is copied onto buff 
 for(int i=0;i<sizeof(charVal);i++)
  {
 // lcd.print(charVal[i]);
  }
  for(int i=0;i<sizeof(charVal);i++)
  {
    stringVal1+=charVal[i];
  }
  }

}