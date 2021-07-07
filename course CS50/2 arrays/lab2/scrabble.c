/*  CS50 Lab 2: Scrabble
 *
 *  Ask the user for two words,
 *  calculate the "value" of words and compare.
 */

#include <stdio.h>
#include <cs50.h>
#include <ctype.h>

const int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int scrabble(char *);

int main(void)
{
    char *word_one = get_string("Player 1: ");
    char *word_two = get_string("Player 2: ");

    int score_one = scrabble(word_one);
    int score_two = scrabble(word_two);

    if (score_one > score_two)
    {
        printf("Player 1 wins!\n");
    }
    else if (score_one < score_two)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }

    return 0;
}

int scrabble(char *word)
{
    int score = 0;
    int letter_index;
    for (int c = 0; word[c] != '\0'; c++)
    {
        if (isalpha(word[c]))
        {
            letter_index = word[c];
            letter_index -= islower(word[c]) ? 97 : 65;
            score += POINTS[letter_index];
        }
    }

    return score;
}
