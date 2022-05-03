/*  fall 2020 CS50 PSet 3: Runoff
 *
 *  Runs a runoff election.
 *  May assume that no two candidates will have the same name.
 */

#include <stdio.h>
#include <cs50.h>
#include <iso646.h>
#include <string.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// Numbers of voters and candidates
int voter_count;
int candidate_count;

// Preferences[voter][candidate] is c'th preference for voter v
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct
{
    char* name;
    int votes;
    bool eliminated;
}
candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

bool vote(int, int, char*);
void tabulate(void);
bool print_winner(void);
int find_min(void);
bool is_tie(int);
void eliminate(int);

int main(int argc, char* argv[])
{
    if (argc < 2)
    {
        printf("USAGE: %s [candidate ...]\n", argv[0]);
        return 1;
    }

    // Populate array of candidates:
    candidate_count = argc - 1;
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }
    for (int person = 0; person < candidate_count; person++)
    {
        candidates[person].name = argv[person + 1];
        candidates[person].votes = 0;
        candidates[person].eliminated = false;
    }

    voter_count = get_int("Number of voters: ");
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // Keep querying for votes:
    for (int voter = 0; voter < voter_count; voter++)
    {
        // query for each rank
        for (int rank = 0; rank < candidate_count; rank++)
        {
            char* name = get_string("Rank %i: ", rank + 1);

            // Record vote, unless it's invalid
            if (vote(voter, rank, name) == false)
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }
        putchar('\n');
    }

    // Keep holding runoffs until winner exists:
    while (true)
    {
        // Calculate votes given remaining candidates
        tabulate();

        // Check if election has been won;
        bool won = print_winner();
        if (won)
        {
            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        bool tie = is_tie(min);

        // If tie, everyone wins;
        if (tie)
        {
            for (int cnd = 0; cnd < candidate_count; cnd++)
            {
                if (candidates[cnd].eliminated == false)
                {
                    printf("%s\n", candidates[cnd].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int cnd = 0; cnd < candidate_count; cnd++)
        {
            candidates[cnd].votes = 0;
        }
    }

    return 0;
}

bool vote(int voter, int rank, char* name)
{
    /* Record preference if vote is valid. */

    for (int person = 0; person < candidate_count; person++)
    {
        if (strcmp(name, candidates[person].name) == 0)
        {
            preferences[voter][rank] = person;
            return true;
        }
    }

    return false;
}

void tabulate(void)
{
    /* Tabulate votes for non-eliminated candidates. */

    for (int prefered = 0, voter = 0; voter < voter_count; voter++)
    {
        for (int person = 0; person < candidate_count; person++)
        {
            prefered = preferences[voter][person];
            if (candidates[prefered].eliminated == false)
            {
                candidates[prefered].votes++;
                break;
            }
        }
    }
}

bool print_winner(void)
{
    /* Print the winner of the election, if there is one. */

    // Find the best score:
    int score = 0;
    int pretender = 0;
    for (int cnd = 0; cnd < candidate_count; cnd++)
    {
        if (!candidates[cnd].eliminated and candidates[cnd].votes > score)
        {
            score = candidates[cnd].votes;
            pretender = cnd;
        }
    }

    // Is it more than 50%?
    if (score > voter_count / 2)
    {
        // Is it the strongest one?
        for (int cnd = 0; cnd < candidate_count; cnd++)
        {
            if (cnd != pretender and !candidates[cnd].eliminated and candidates[cnd].votes == score)
            {
                return false;
            }
        }

        // Hooray!
        printf("%s\n", candidates[pretender].name);
        return true;
    }

    return false;
}

int find_min(void)
{
    /* Return the minimum number of votes any remaining candidate has. */

    int min = voter_count;
    for (int cnd = 0; cnd < candidate_count; cnd++)
    {
        if (!candidates[cnd].eliminated and candidates[cnd].votes < min)
        {
            min = candidates[cnd].votes;
        }
    }

    return min;
}

bool is_tie(int min)
{
    /* Return true if the election is tied between all candidates, false otherwise. */

    for (int cnd = 0; cnd < candidate_count; cnd++)
    {
        if (!candidates[cnd].eliminated and candidates[cnd].votes != min)
        {
            return false;
        }
    }

    return true;
}

void eliminate(int min)
{
    /* Eliminate the candidate (or candidates) in last place. */

    for (int cnd = 0; cnd < candidate_count; cnd++)
    {
        if (!candidates[cnd].eliminated and candidates[cnd].votes == min)
        {
            candidates[cnd].eliminated = true;
        }
    }
}
