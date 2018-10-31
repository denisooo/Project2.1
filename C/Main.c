#define F_CPU 16000000UL

#include <avr/io.h>
#include <stdint.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include <stdbool.h>
int main (void)
{
  while(1) {
    _delay_ms(500);
  }
  return 0;
}
