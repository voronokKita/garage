/*  fall 2020 CS50 Lab 1: Population Growth
 *
 *  Ask the user for the start & the threshold of (llamas) population,
 *  calculate years to the population to reach the threshold.
 */

#include <stdio.h>
#include <cs50.h>

const int BIRTH_RATE = 3;
const int DEATH_RATE = 4;

int growth(int, int);

int main(void)
{
    int pop_start;
    do
    {
        pop_start = get_int("Start size: ");
    }
    while (pop_start < 9);

    int pop_end;
    do
    {
        pop_end = get_int("End size: ");
    }
    while (pop_end < pop_start);

    int years = growth(pop_start, pop_end);

    printf("Years: %i\n", years);
    
    return 0;
}

int growth(int population, int threshold)
{
    int years, n;
    for (years = 0; population < threshold; years++)
    {
        n = population;
        population = (n + (n / BIRTH_RATE - n / DEATH_RATE));
    }
    return years;
}
