#include <math.h>
#define pinADC 26
int analogValue=0;
float Vref=3100;// Voltaje de referencia para el ADC
float Vout=0;
float Plinea=57.6,Vpk=0;;// Valor entre 1 y 500 kW, las unidades son kW
int VminPot=1;//con esto quiere decir que potencia es la máxima
bool serialData=0;//Un valor de 1 indica que se debe ingresar por monitor
float VoutRef=1;
int numSamples=20;
int total=0;
void setup() {
  Serial.begin(115200);
  
  analogSetAttenuation(ADC_11db);
  if(serialData){
  Serial.println("Ingrese la potencia en la linea:");
  while (!Serial.available()); // Wait for input
  String potLinChar = Serial.readStringUntil('\n');
  Plinea=atof(potLinChar.c_str());
  }
  Vpk=sqrt(10*Plinea)/5;
  VoutRef=ecuacionLineal(Vpk);
  Serial.print("Voltaje de salida de referencia: ");
  Serial.print(VoutRef);
  Serial.print("Voltaje pkpk:"); Serial.print(" "); Serial.println(Vpk);

}

void loop() {
  total=0;
  //analogValue = analogRead(pinADC);
  for (int i = 0; i < numSamples; i++) {
    total += analogRead(pinADC);
    delay(1);
  }
  int averageValue = total / numSamples;
  Vout = 0.8291*averageValue+90.27;//Ajuste realizado para el ADC
  Serial.println(Vout);
}
float ecuacionLineal(float PdBm){
  float m=-0.02451,b=1.048;
  return Vout=m*PdBm+b;
}
