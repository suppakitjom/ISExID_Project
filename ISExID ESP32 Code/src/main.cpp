#include <Arduino.h>
#include <MFRC522.h>
#include <SPI.h>

const int BUTTON1 = 2;
const int BUTTON2 = 3;
const int BUTTON3 = 4;
const int BUTTON4 = 5;

const int SS_PIN = 10;
const int RST_PIN = 9;

bool isActive = false;

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
    pinMode(BUTTON1, INPUT_PULLUP);
    pinMode(BUTTON2, INPUT_PULLUP);
    pinMode(BUTTON3, INPUT_PULLUP);
    pinMode(BUTTON4, INPUT_PULLUP);
    Serial.begin(9600);
    SPI.begin();
    rfid.PCD_Init();
}

void loop() {
    // if (digitalRead(BUTTON1) == LOW) {
    //     Serial.println("1");
    // }
    // if (digitalRead(BUTTON2) == LOW) {
    //     Serial.println("2");
    // }
    // if (digitalRead(BUTTON3) == LOW) {
    //     Serial.println("3");
    // }
    // if (digitalRead(BUTTON4) == LOW) {
    //     Serial.println("4");
    // }
    tempCardID = getCardID();

    if (tempCardID != "") {
        if (!isActive) {
            Serial.println('6');
            isActive = true;
        }
        cardID = tempCardID;
        // Serial.println(cardID);

        if (digitalRead(BUTTON1) == LOW) {
            Serial.println("1");
            delay(750);
        } else if (digitalRead(BUTTON2) == LOW) {
            Serial.println("2");
            delay(750);
        } else if (digitalRead(BUTTON3) == LOW) {
            Serial.println("3");
            delay(750);
        } else if (digitalRead(BUTTON4) == LOW) {
            Serial.println("4");
            delay(750);
        }
    } else {
        if (isActive) {
            Serial.println('5');
            isActive = false;
        }
    }
}