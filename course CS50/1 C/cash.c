/*  fall 2020 CS50 PSet1: Cash
 *
 *  Ask the user for the change owed,
 *  count minimum number of coins needed to pay.
 */

#include <stdio.h>
#include <cs50.h>
#include <math.h>

int cash(int);

int main(void)
{
    float answer;
    do
    {
        answer = get_float("Change owed: ");
    }
    while (answer <= 0);

    int change = round(answer * 100);
    int coins = cash(change);

    printf("%i\n", coins);

    return 0;
}

int cash(int change)
{
    int coins = 0;
    while (change > 0)
    {
        if (change / 25 >= 1)
        {
            change -= 25;
            coins++;
        }
        else if (change / 10 >= 1)
        {
            change -= 10;
            coins++;
        }
        else if (change / 5 >= 1)
        {
            change -= 5;
            coins++;
        }
        else
        {
            change -= 1;
            coins++;
        }
    }
    return coins;
}
