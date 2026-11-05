// Gajendra | 2301ME18 | ME3202 Lab 6 study reproduction
// Requires Keypad and LiquidCrystal_I2C libraries.

#include <Keypad.h>
#include <LiquidCrystal_I2C.h>

const byte ROWS = 4;
const byte COLS = 4;
char keys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};
byte rowPins[ROWS] = {2, 3, 4, 5};
byte colPins[COLS] = {6, 7, 8, 9};
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("ME3202 Keypad");
  lcd.setCursor(0, 1);
  lcd.print("Press a key");
}

void loop() {
  char key = keypad.getKey();
  if (key != NO_KEY) {
    Serial.print("Key pressed: ");
    Serial.println(key);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Key pressed:");
    lcd.setCursor(0, 1);
    lcd.print(key);
  }
}
