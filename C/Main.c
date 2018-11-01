#define F_CPU 16000000UL

#include <avr/io.h>
#include <stdint.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include <stdbool.h>
#include <include/Functions.c>

// Globale variabelen
float MAXTEMP;
float MAXLIGHT;
float MAXROLLOUT;
float MINROLLOUT;
float CURRENTDISTANCE;
float ROLL_TO;
float ROLL_TO_MIN;
float ROLL_TO_MAX;

union Param{
  char chrs[4];
  float f;
} PROTO_PARAM;

int main (void)
{
  ports();
  while(1) {
    _delay_ms(500);
  }
  return 0;
}
