/* Hello, CS50! */

#include <stdio.h>
#include <cs50.h>
#include <string.h>

int main(void)
{
    char *answer = get_string("What is your name? ");

    if (strlen(answer) > 1)
        printf("Hello, %s!\n", answer);
    else
        printf("Hello, World!\n");

    return 0;
}
