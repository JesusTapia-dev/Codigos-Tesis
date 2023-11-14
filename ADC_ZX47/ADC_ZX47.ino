#include <math.h>
#define pinADC 26
float find_maximun(float *p);
int analogValue=0;
float Vout=0;
float Plinea=62.5,Vpk=0;// Valor entre 1 y 500 kW, las unidades son kW
float Plcal=0,dif=0,difPlow=0;
bool serialData=1;//Un valor de 1 indica que se debe ingresar por monitor serial
float VoutRef=1,Pmax;
int numSamples=20;
int total=0;
int contador=0,SIZE=40; 
float *p, Parray[40];
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
  /*
  for (int i = 0; i < numSamples; i++) {
    total += analogRead(pinADC);
  }*/
  //int averageValue = total / numSamples;
  int averageValue=analogRead(pinADC);
  Vout = 0.8291*averageValue+90.27;//Ajuste realizado para el ADC
  //Serial.println(Vout);
  Plcal=5*pow((Vout+101),2)/(2*175.19*175.19);//Calculamos la potencia en la línea
  //dif=abs(Plinea-Plcal)*100/Plinea;//Hallamos la diferencia porcentual
  if (Plcal>3){//valores por debajo de este umbral serán leidos como tierra
    Parray[contador]=Plcal;
   contador =contador+1;
  }  
  //cuando llenamos los valores hacemos la 
  if (contador==SIZE){
    p=&Parray[0];
    Pmax=find_maximun(p);
    contador=0;
    dif=abs(Plinea-Pmax)*100/Plinea;
    difPlow=abs(Plinea-Pmax);
    if(dif>10 && difPlow>7) Serial.println(Pmax);  
  }


  /*
  if(dif>10 &&  Vout>120 ){
   Parray[contador]=Plcal;
   contador =contador+1;
    if(contador==SIZE){
      p=&Parray[0];
      Pmax=find_maximun(p);
      contador=0;
      difPlow=abs(Plinea-Pmax);
      if (difPlow>8) {
        Serial.print("Potencia anomala en el transmisor: "); 
        Serial.println(Pmax);  
      }
    }
  } */
}
float ecuacionLineal(float Vpk){
  float m=175.19,b=-101;
  return Vout=m*Vpk+b;
}
float find_maximun(float *p){
	float maxi=*p;
	float *q;
	q=p;
	for(int i=0;i<SIZE;i++){
		if(maxi<*(p+i)) {
			maxi=*(p+i);
		}
	}
	return maxi;
}