#include <math.h>
#define pinADC 26
int analogValue=0;
float Vout=0;
float Plinea=62.5,Vpk=0;// Valor entre 1 y 500 kW, las unidades son kW
float Plcal=0,dif=0;
bool serialData=1;//Un valor de 1 indica que se debe ingresar por monitor serial
float VoutRef=1;
int numSamples=20;
int total=0;
int contador=0; 
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
  Serial.println(VoutRef);
}
void loop() {
  total=0;
  //analogValue = analogRead(pinADC);
  //Hacemos multisampling para asegurar el buen performance
  for (int i = 0; i < numSamples; i++) {
    total += analogRead(pinADC);
  }
  int averageValue = total / numSamples;
  Vout = 0.8291*averageValue+90.27;//Ajuste realizado para el ADC
  //Serial.println(Vout);
  Plcal=5*pow((Vout+101),2)/(2*175.19*175.19);//Calculamos la potencia en la línea
  dif=abs(Plinea-Plcal)*100/Plinea;//Hallamos la diferencia porcentual
  if(dif>10 && VoutRef>3000) Serial.println("Nivel anómalo de potencia");
  else if(VoutRef<3000){
    Serial.println("Potencia menor a la debida");
  }
}
float ecuacionLineal(float Vpk){
  float m=175.19,b=-101;
  return Vout=m*Vpk+b;
}
