#define pinADC 15
int analogValue=0;
//int IPP=;
float Vout=0;
int VminPot=1;//con esto quiere decir que potencias
float Vref=3.3;// Voltaje de referencia 
void setup() {
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  analogValue = analogRead(pinADC);
  Vout = analogValue * Vref / 4095;
  Serial.print(Vout);
  Serial.print(" ");
 Serial.println(VminPot);

}
