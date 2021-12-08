/*  fall 2020 CS50 Lab 5: Inheritance
 *
 *  Simulate genetic inheritance of blood type.
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Each person has two parents and two alleles
typedef struct person
{
    struct person *parents[2];
    char alleles[2];
}
person;

const int GENERATIONS = 3;
const int INDENT_LENGTH = 4;

person *create_family(int);
char random_allele(void);
void print_family(person *, int);
void free_family(person *);

int main(void)
{
    srand(time(0));

    person *p = create_family(GENERATIONS);
    print_family(p, 0);
    free_family(p);

    return 0;
}

person *create_family(int generations)
{
    /* Create a new individual with generations. */

    // Allocate memory for a new person
    person *p = malloc(sizeof(person));
    if (p == NULL)
    {
        printf("Dynamic Memory Allocation Fail.\n");
        exit(1);  // ?
    }
    person *parent = NULL;

    // Generation with parents data:
    if (generations > 1)
    {
        // 1) Recursively create parents
        p->parents[0] = create_family(generations - 1);
        p->parents[1] = create_family(generations - 1);

        // 2) Assign child alleles based on parents
        parent = p->parents[0];
        p->alleles[0] = (rand() % 2) ? parent->alleles[0] : parent->alleles[1];
        parent = p->parents[1];
        p->alleles[1] = (rand() % 2) ? parent->alleles[0] : parent->alleles[1];
    }

    // Generation without parents data:
    else // if (generations == 1)
    {
        // 1) Set parents pointers to NULL
        p->parents[0] = NULL;
        p->parents[1] = NULL;

        // 2) Randomly assign alleles
        p->alleles[0] = random_allele();
        p->alleles[1] = random_allele();
    }

    // Return the newly created person.
    return p;
}

char random_allele()
{
    /* Randomly chooses a blood type allele. */

    int allele = rand() % 3;

    if (allele == 0)
        return 'A';
    else if (allele == 1)
        return 'B';
    else
        return 'O';
}

void print_family(person *p, int generation)
{
    /* Print each family member and their alleles. */

    // Handle base case
    if (p == NULL)
        return;

    // Print indentation;
    int indentation = generation * INDENT_LENGTH;
    for (int i = 0; i < indentation; i++)
        putchar(' ');

    // Print the person;
    printf("Generation %i, blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);

    // Print his parents.
    print_family(p->parents[0], generation + 1);
    print_family(p->parents[1], generation + 1);
}

void free_family(person *p)
{
    /* Free a person and all his ancestors. */

    if (p == NULL)
        return;

    free_family(p->parents[0]);
    free_family(p->parents[1]);

    free(p);
}
