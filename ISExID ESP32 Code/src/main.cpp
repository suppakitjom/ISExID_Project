#include <Arduino.h>
#include <MFRC522.h>
#include <SPI.h>

const int BUTTON1 = 32;
const int BUTTON2 = 33;
const int BUTTON3 = 25;
const int BUTTON4 = 26;

const int SS_PIN = 5;
const int RST_PIN = 27;
MFRC522 rfid(SS_PIN, RST_PIN);

String cardID;
String tempCardID;
String getCardID() {
    // if card detected return its id
    if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
        // convert UID to string
        String content = "";
        for (byte i = 0; i < rfid.uid.size; i++) {
            content.concat(String(rfid.uid.uidByte[i] < 0x10 ? " 0" : " "));
            content.concat(String(rfid.uid.uidByte[i], HEX));
        }
        content.toUpperCase();
        content.trim();

        while (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
            // do nothing
        }

        rfid.PICC_HaltA();
        rfid.PCD_StopCrypto1();
        return content;
    } else {
        return "";
    }
}

void setup() {
    // put your setup code here, to run once:
    pinMode(BUTTON1, INPUT_PULLDOWN);
    pinMode(BUTTON2, INPUT_PULLDOWN);
    pinMode(BUTTON3, INPUT_PULLDOWN);
    pinMode(BUTTON4, INPUT_PULLDOWN);
    Serial.begin(9600);
    SPI.begin();
    rfid.PCD_Init();
}
void loop() {
    tempCardID = getCardID();

    // checks if card id is not the same as the last one
    // if changes, check if it is registered then play corresponding track
    if (tempCardID != cardID) {
        cardID = tempCardID;
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
}