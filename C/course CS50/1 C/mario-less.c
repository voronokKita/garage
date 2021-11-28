/*  CS50 PSet1: Mario less
 *
 *  Build stairs of #hashes.
 */

#include <stdio.h>
#include <cs50.h>
#include <iso646.h>

const int MIN = 1;
const int MAX = 8;

void pyramid(int);

int main(void)
{
    int pyramid_height;
    do
    {
        pyramid_height = get_int("Height: ");
    }
    while (pyramid_height < MIN or pyramid_height > MAX);

    pyramid(pyramid_height);

    return 0;
}

void pyramid(int layer)
{
    /*  Let's imagine the pyramid as an empty square,
     *  the volume of emptiness wherein decreases from top to bottom with every level,
     *  but the number of bricks increases:
     */
    int bricks, space, brickwork;
    for (bricks = 1; layer > 0; layer--, bricks++)
    {
        for (space = layer - 1; space > 0; space--)
        {
            putchar(' ');
        }
        for (brickwork = bricks; brickwork > 0; brickwork--)
        {
            putchar('#');
        }
        putchar('\n');
    }
}
