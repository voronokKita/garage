/*  fall 2020 CS50 PSet1: Mario more
 *
 *  Build two symmetric stairs of #hashes with 2 spaces between.
 */

#include <stdio.h>
#include <cs50.h>
#include <iso646.h>

const int MIN = 1;
const int MAX = 8;

void pyramid(int, int);

int main(void)
{
    int pyramid_height;
    do
    {
        pyramid_height = get_int("Height: ");
    }
    while (pyramid_height < MIN or pyramid_height > MAX);

    pyramid(pyramid_height, pyramid_height);

    return 0;
}

void pyramid(int bricks, int layers)
{
    // Recursion border
    if (bricks == 0)
    {
        return;
    }

    // Recursion
    pyramid(bricks - 1, layers);

    // Emptiness
    for (int space = layers - bricks; space > 0; space--)
    {
        putchar(' ');
    }

    // Bricks
    int opening = bricks + 1;
    for (int brickwork = bricks * 2 + 1; brickwork > 0; brickwork--)
    {
        brickwork == opening ? printf("  ") : putchar('#');
    }

    putchar('\n');
}
