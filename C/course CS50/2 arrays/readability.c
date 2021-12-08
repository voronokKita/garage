/*  fall 2020 CS50 PSet 2: Readability
 *
 *  Asks the user for some text and then rates the text difficulty.
 */

#include <stdio.h>
#include <cs50.h>
#include <iso646.h>
#include <ctype.h>
#include <math.h>

// Entities in the counters[i]:
#define WORDS 0
#define LETTERS 1
#define SENTENCES 2

void counter(char*, int []);
int readability(int []);

int main(void)
{
    char* lalala = get_string("Text: ");

    // Count entities;
    int counters[] = {0, 0, 0};
    counter(lalala, counters);

    // The Coleman-Liau index;
    int index = readability(counters);

    if (index < 1)
        printf("Before Grade 1\n");
    else if (index > 16)
        printf("Grade 16+\n");
    else
        printf("Grade %i\n", index);

    return 0;
}

void counter(char* line, int counters[])
{
    char c = '\0';
    bool in_word = false;
    for (int i = 0; line[i] != '\0'; i++)
    {
        c = line[i];

        // Check word:
        if (c == ' ' or c == '\t' or c == '\n')
        {
            in_word = false;
            continue;
        }
        else if (in_word == false)
        {
            in_word = true;
            counters[WORDS]++;
        }

        // Check symbols:
        if (c == '.' or c == '!' or c == '?')
        {
            counters[SENTENCES]++;
        }
        else if (isalpha(c))
        {
            counters[LETTERS]++;
        }
    }
}

int readability(int counters[])
{
    /* index = 0.0588 * L - 0.296 * S - 15.8 */

    // L is the average number of letters per 100 words
    float L = ((float) counters[LETTERS] / counters[WORDS]) * 100.0;

    // S is the average number of sentences per 100 words
    float S = ((float) counters[SENTENCES] / counters[WORDS]) * 100.0;

    return roundf(0.0588 * L - 0.296 * S - 15.8);
}
