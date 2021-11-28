/*  CS50 PSet 2: Caesar
 *
 *  Uses a int-argument as an encryption key;
 *  ask the user for enter text
 *  and then print encrypted result of that text.
 */

#include <stdio.h>
#include <cs50.h>
#include <iso646.h>
#include <ctype.h>
#include <stdlib.h>
#include <limits.h>

bool check_key(char*);
void caesar(char*, int);

int main(int argc, char* argv[])
{
    // Is the key correct?
    if (argc != 2 or check_key(argv[1]) == false)
    {
        printf("USAGE: %s positive-integer-key\n", argv[0]);
        return 1;
    }

    // Input;
    char* line = get_string("plaintext: ");

    // Cript;
    caesar(line, atoi(argv[1]));

    // Output.
    printf("Ciphertext: %s\n", line);

    return 0;
}

bool check_key(char* key)
{
    // It is digit?
    for (int integer_ranks = 9, r = 0; key[r] != '\0'; r++)
    {
        if (!isdigit(key[r]) or r > integer_ranks)
        {
            return false;
        }
    }

    // Is boundary value correct?
    long num = atol(key);
    if (num <= 0 or num > INT_MAX)
    {
        return false;
    }

    // The key is correct.
    return true;
}

void caesar(char* line, int key)
{
    char tmp;
    for (int c = 0; line[c] != '\0'; c++)
    {
        if (isalpha(line[c]))
        {
            tmp = line[c];

            // upper or lower?
            tmp -= isupper(line[c]) ? 65 : 97;

            // key-shift % within alphabetic borders
            tmp = (tmp + key) % 26;

            // restore
            tmp += isupper(line[c]) ? 65 : 97;

            line[c] = tmp;
        }
    }
}
