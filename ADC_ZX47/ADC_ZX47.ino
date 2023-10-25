#include <math.h>
#define pinADC 12
int analogValue=0;
float Vref=2.45;// Voltaje de referencia para el ADC
//int IPP=;
float Vout=0;
float Plinea=57.6;// Valor entre 1 y 500 kW, las unidades son kW
float PdBm=0;
int VminPot=1;//con esto quiere decir que potencias
bool serialData=0;
float VoutRef=1;
void setup() {
  Serial.begin(115200);
 // analogSetAttenuation(ADC_11db);
  if(serialData){
  Serial.println("Ingrese la potencia en la linea(en kW,debe ser int):");
  while (!Serial.available()); // Wait for input
  String potLinChar = Serial.readStringUntil('\n');
  Plinea=atof(potLinChar.c_str());
  }
  PdBm=10 *(log10(Plinea)-2);
  VoutRef=ecuacionLineal(PdBm);
  Serial.print("Voltaje de salida de referencia: ");
  Serial.println(VoutRef);
}

void loop() {
  // put your main code here, to run repeatedly:
  analogValue = analogRead(pinADC);
  Vout = analogValue * 3.458 / 4095;
  if(abs(Vout-VoutRef)>0.08 && Vout>1.9 ) {
    Serial.print(Vout);
  }

}
float ecuacionLineal(float PdBm){
  float m=-0.02451,b=1.048;
  return Vout=m*PdBm+b;
}
