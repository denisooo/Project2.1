#define BAUD 9600
#include <util/setbaud.h>
#include <avr/eeprom.h>

void ports(void){
  DDRC &= ~_BV(DDC0); // Analog pin 0 input Temprature
  DDRC &= ~_BV(DDC1); // Analog pin 1 input Light
  DDRC |= _BV(DDC3); // Pin 3 output (trigger)
  DDRD &= ~_BV(DDC4); // Pin 4 input (echo )
  DDRD &= ~_BV(DDC5); // Pin 5 Input ROLLIN
  DDRD &= ~_BV(DDC6); // Pin 6 Input stop
  DDRD &= ~_BV(DDC7); // Pin 7 input stop
  DDRB |= _BV(DDB0); // Pin 8 motor
  DDRB |= _BV(DDB1); // Pin 9 motor
  DDRB |= _BV(DDB2); // Pin 10 motor
  DDRB |= _BV(DDB6); // Pin 13 motor
  DDRB |= _BV(DDB4); // Pin 11 output Red led
  DDRB |= _BV(DDB5); // Pin 12 output Yellow led
  DDRB |= _BV(DDB6); // Pin 13 output Green led
}
void rollin(){
  int run;
  char i;
  for (run = 0; run < 20; run++){
    for i = 0; i <= 3; i++{
      case 0:
        PORTD |= _BV(PB0);
        PORTD |= _BV(PB1);
        PORTD &= ~_BV(PB2);
        PORTB &= ~_BV(PB6);
      break;
      case 1:
        PORTD &= ~_BV(PB0);
        PORTD |= _BV(PB1);
        PORTD |= _BV(PB2);
        PORTB &= ~_BV(PB6);
      break;
      case 2:
        PORTD &= ~_BV(PB0);
        PORTD &= ~_BV(PB1);
        PORTD |= _BV(PB2);
        PORTB |= _BV(PB6);
      break;
      case 3:
        PORTD |= _BV(PB0);
        PORTD &= ~_BV(PB1);
        PORTD &= ~_BV(PB2);
        PORTB |= _BV(PB6);
    }
    _delay_ms(50);
  }
}
void rollout(){
  int run;
  char i;
  for (run = 0; run < 20; run++){
    for i = 0; i <= 3; i++{
      case 0:
        PORTD |= _BV(PB0);
        PORTD |= _BV(PB1);
        PORTD &= ~_BV(PB2);
        PORTB &= ~_BV(PB6);
      break;
      case 1:
        PORTD &= ~_BV(PB0);
        PORTD |= _BV(PB1);
        PORTD |= _BV(PB2);
        PORTB &= ~_BV(PB6);
      break;
      case 2:
        PORTD &= ~_BV(PB0);
        PORTD &= ~_BV(PB1);
        PORTD |= _BV(PB2);
        PORTB |= _BV(PB6);
      break;
      case 3:
        PORTD |= _BV(PB0);
        PORTD &= ~_BV(PB1);
        PORTD &= ~_BV(PB2);
        PORTB |= _BV(PB6);
    }
    _delay_ms(50);
  }
}
