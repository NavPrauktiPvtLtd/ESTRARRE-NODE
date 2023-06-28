
//install Adafruit_MLX90614 library in arduino first

#include <Adafruit_MLX90614.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

void setup() {
  Serial.begin(9600);
  while (!Serial);
 
  if (!mlx.begin()) {
    Serial.println("Error connecting to MLX sensor. Check wiring.");
    while (1);
  };
}

void loop() {

  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    //Serial.print("You sent me: ");
     char read_data = data[0];
    if(read_data == 'a'){
      Serial.print(mlx.readObjectTempC()); Serial.println("*C");
    }
    //Serial.println(read_data);
    
  }

  delay(1000);
}