from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

_lcd = Adafruit_CharLCDPlate()

def message(message):
	_lcd.clear()
	_lcd.message(message)
