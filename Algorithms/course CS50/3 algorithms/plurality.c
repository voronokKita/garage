/*  fall 2020 CS50 PSet 3: Plurality
 *
 *  Runs a plurality election.
 *  May assume that no two candidates will have the same name.
 */

#include <stdio.h>
#include <cs50.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Number of candidates
int candidate_count;

// Candidates have name and vote count
typedef struct
{
    char* name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

bool vote(char* name);
void print_winner(void);

int main(int argc, char* argv[])
{
    if (argc < 2)
    {
        printf("USAGE: %s [candidate-1 ... candidate-9]\n", argv[0]);
        return 1;
    }

    // Populate array of candidates:
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int cnd = 0; cnd < candidate_count; cnd++)
    {
        candidates[cnd].name = argv[cnd + 1];
        candidates[cnd].votes = 0;
    }

    // Number of voters;
    int voter_count = get_int("Number of voters: ");

    // Loop over all voters:
    for (int voter = 0; voter < voter_count; voter++)
    {
        char* name = get_string("Vote: ");

        // Check for invalid vote
        if (vote(name) == false)
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of the election.
    print_winner();

    return 0;
}

bool vote(char* name)
{
    /* Update vote totals by given a new vote. */

    for (int cnd = 0; cnd < candidate_count; cnd++)
    {
        if (strcmp(name, candidates[cnd].name) == 0)
        {
            candidates[cnd].votes++;
            return true;
        }
    }

    return false;
}


void print_winner(void)
{
    /* Print the winner (or winners) of the election. */

    // insertion sort:
    int j, tmp_votes;
    char* tmp_name;
    for (int cnd = 0; cnd < candidate_count; cnd++)
    {
        j = candidate_count - 1 - cnd;
        while (j > 0 && candidates[j].votes > candidates[j - 1].votes)
        {
            tmp_name = candidates[j - 1].name;
            tmp_votes = candidates[j - 1].votes;
            candidates[j - 1].name = candidates[j].name;
            candidates[j - 1].votes = candidates[j].votes;
            candidates[j].name = tmp_name;
            candidates[j].votes = tmp_votes;
            j--;
        }
    }

    // Output:
    printf("%s\n", candidates[0].name);

    if (candidates[1].votes == candidates[0].votes)
    {
        for (int cnd = 1; cnd < candidate_count; cnd++)
        {
            if (candidates[cnd].votes == candidates[0].votes)
            {
                printf("%s\n", candidates[cnd].name);
            }
        }
    }
}
