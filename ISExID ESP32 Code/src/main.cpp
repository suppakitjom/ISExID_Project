#include <Arduino.h>

int BUTTON1 = 1;
int BUTTON2 = 2;
int BUTTON3 = 3;
int BUTTON4 = 4;

void setup() {
    // put your setup code here, to run once:
    pinMode(BUTTON1, INPUT_PULLDOWN);
    pinMode(BUTTON2, INPUT_PULLDOWN);
    pinMode(BUTTON3, INPUT_PULLDOWN);
    pinMode(BUTTON4, INPUT_PULLDOWN);
    Serial.begin(9600);
}

void loop() {
    // put your main code here, to run repeatedly:
    // if button is pressed, serial print number of button
    if (digitalRead(BUTTON1) == HIGH) {
        Serial.println("1");
    }
    if (digitalRead(BUTTON2) == HIGH) {
        Serial.println("2");
    }
    if (digitalRead(BUTTON3) == HIGH) {
        Serial.println("3");
    }
    if (digitalRead(BUTTON4) == HIGH) {
        Serial.println("4");
    }
}