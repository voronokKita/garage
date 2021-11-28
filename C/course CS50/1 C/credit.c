/*  CS50 PSet1: Credit
 *
 *  Validate some credit cards numbers of
 *  American Express, Master Card and Visa.
 */

#include <stdio.h>
#include <cs50.h>
#include <iso646.h>

// Firsts numbers of cards brands, 0 is the end of list:
const int AMEX_HEADERS[] = {34, 37, 0};
const int MACA_HEADERS[] = {51, 52, 53, 54, 55, 22, 0};
const int VISA_HEADERS[] = {4, 0};

bool in_list(int num, const int arr[])
{
    /* Check is the number in lists of headers? */

    int i;
    for (i = 0; arr[i] != num and arr[i] != 0; i++);

    return arr[i] == num ? true : false;
}

int validation(long long);
bool luhn(long long);

int main(void)
{
    long long number;
    do
    {
        number = get_long("Number: ");
    }
    while (number <= 0);

    // Check number length and leading digits;
    int brand = -1;
    brand = validation(number);

    // Run Luhn's test if card is probably valid;
    bool luhn_result = false;
    if (brand > 0)
    {
        luhn_result = luhn(number);
    }

    // Output results:
    if (brand <= 0 or luhn_result != true)
    {
        printf("INVALID\n");
    }
    else if (in_list(brand, AMEX_HEADERS) == true)
    {
        printf("AMEX\n");
    }
    else if (in_list(brand, MACA_HEADERS) == true)
    {
        printf("MASTERCARD\n");
    }
    else if (in_list(brand, VISA_HEADERS) == true)
    {
        printf("VISA\n");
    }

    return 0;
}

int validation(long long number)
{
    const int shift = 10;

    // Count ranks of a number;
    int num_ranks = 0;
    for (long long x = number; x > 0; num_ranks++)
    {
        x /= shift;
    }

    // Shift to first two digits;
    for (int r = 0; r < (num_ranks - 2); r++)
    {
        number /= shift;
    }

    // Check AMEX and MACA;
    if (in_list(number, AMEX_HEADERS) == true)
    {
        return number;
    }
    else if (in_list(number, MACA_HEADERS) == true)
    {
        return number;
    }
    else
    {
        // Shift to first digit and check Visa;
        number /= shift;
        if (in_list(number, VISA_HEADERS) == true)
        {
            return number;
        }
    }

    // Invalid.
    return -1;
}

bool luhn(long long number)
{
    /*  Luhn’s Algorithm
     *  1) Multiply every second digit by 2, starting with the number’s second-to-last digit,
     *      and then add those products’ digits together.
     *  2) Add the sum to the sum of the digits that weren’t multiplied by 2.
     *  3) If the total’s last digit is 0
     *      (or, put more formally, if the total modulo 10 is congruent to 0),
     *      the number is valid!
     */
    int tmp = 0;
    bool flag = 1;
    int firsts = 0;
    int seconds = 0;    
    const int shift = 10;

    while (number > 0)
    {
        // 1 - first
        if (flag == 1)
        {
            firsts += number % 10;

            number /= shift;
            flag = 0;
        }
        
        // 0 - second
        else
        {
            tmp = ((number % 10) * 2);
            // if single digit
            if (tmp < 10) 
            {
                seconds += tmp;
                tmp = 0;
            }
            // if two-digit
            else 
            {
                seconds += tmp % 10;
                tmp /= shift;
                seconds += tmp % 10;
                tmp = 0;
            }

            number /= shift;
            flag = 1;
        }
    }

    // Apply formula and return result.
    bool result = ((firsts + seconds) % 10 == 0) ? true : false;
    return result;
}
