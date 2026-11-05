# Lab 6 study: Arduino Uno keypad and I2C LCD

**Gajendra | 2301ME18 | ME3202, IIT Patna**

The supplied Lab 6 manual uses a 4x4 keypad, a 16x2 I2C LCD and an Arduino Uno. This independently written sketch prints the pressed key to both the LCD and Serial Monitor. It is ready to compile with the `Keypad` and `LiquidCrystal_I2C` libraries, but has not been hardware-tested as part of this repository preparation.

The [illustrated project report](reports/arduino_keypad_lcd_study.pdf) explains the abstract, wiring, completed work and verification steps.

## Wiring

| Part | Arduino Uno pin |
| --- | --- |
| Keypad rows 1-4 | D2, D3, D4, D5 |
| Keypad columns 1-4 | D6, D7, D8, D9 |
| LCD SDA / SCL | A4 / A5 |
| LCD VCC / GND | 5V / GND |

Upload [`keypad_lcd.ino`](keypad_lcd.ino), open Serial Monitor at 9600 baud, and press each key. If the display is blank, verify power, I2C address, contrast and wiring. If the wrong key appears, check row/column order before changing the key map.
