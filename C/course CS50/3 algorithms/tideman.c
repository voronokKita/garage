/*  fall 2020 CS50 PSet 3: Tideman
 *
 *  Runs a Tideman election.
 *  May assume that no two candidates will have the same name.
 */

#include <stdio.h>
#include <cs50.h>
#include <iso646.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Array of candidates
char* candidates[MAX];
int candidate_count;

// preferences[x][y] is number of voters who prefer x over y
int preferences[MAX][MAX];

// locked[x][y] means x is locked in over y
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

pair pairs[MAX * (MAX - 1) / 2];
int pair_count;

bool vote(int, char*, int []);
void record_preferences(int []);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
bool cycle(int, int);
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
    for (int person = 0; person < candidate_count; person++)
    {
        candidates[person] = argv[person + 1];
    }

    // Clear graph of locked in pairs:
    for (int x = 0; x < candidate_count; x++)
    {
        for (int y = 0; y < candidate_count; y++)
        {
            locked[x][y] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes:
    for (int voter = 0; voter < voter_count; voter++)
    {
        // ranks[voter] is voter's i'th preference
        int ranks[candidate_count];

        // Query for each rank:
        for (int rank = 0; rank < candidate_count; rank++)
        {
            char* name = get_string("Rank %i: ", rank + 1);

            if (vote(rank, name, ranks) == false)
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

bool vote(int rank, char* name, int ranks[])
{
    /* Update ranks given a new vote. */

    for (int person = 0; person < candidate_count; person++)
    {
        if (strcmp(name, candidates[person]) == 0)
        {
            ranks[rank] = person;
            return true;
        }
    }
    return false;
}

void record_preferences(int ranks[])
{
    /*  Update preferences given one voter's ranks.
     *  preferences[x][y] is number of voters who prefer x over y.
     *  input like: cnd3 cnd1 cnd0 cnd2
     *  output:
     *  x3 0 + + +
     *  x2 0 0 0 0
     *  x1 + 0 + 0
     *  x0 0 0 + 0   
     */
    // List from where to strike candidates with each rank
    bool candidate_above[candidate_count];
    memset(candidate_above, false, candidate_count);

    int rank, x, y;
    for (rank = 0; rank < candidate_count; rank++)
    {
        // Take candidate from ranks
        x = ranks[rank];

        // Strike self-candidate from list
        candidate_above[x] = true;

        // Give candidate preferences before those who still in list;
        for (y = 0; y < candidate_count; y++)
        {
            if (candidate_above[y] == false)
            {
                preferences[x][y]++;
            }
        }
    }
}

void add_pairs(void)
{
    /*  Record pairs of candidates where one is preferred over the other.
     *  expected input like:
     *  x2 3 3 0
     *  x1 2 0 2
     *  x0 0 3 2
     *  output: A>B, C>A, C>B; pair_count == 3
     */
    int x, y, i;
    int max = MAX * (MAX - 1) / 2;
    // pair_count == 0

    for (x = 0; x < candidate_count; x++)
    {
        for (y = 0; y < candidate_count; y++)
        {
            if (preferences[x][y] > preferences[y][x] and pair_count < max)
            {
                i = pair_count;
                pairs[i].winner = x;
                pairs[i].loser = y;
                pair_count++;
            }
        }
    }
}

void sort_pairs(void)
{
    /*  Sort pairs in decreasing order by the strength of victory.
     *  expected input like: 3 pairs; A>B, C>A, C>B
     *  output: strength[0] = votes, strength[1] = votes, strength[2] = votes
     */
    // Get the strength of each victory:
    int strength[pair_count];
    int x, y, pair;
    for (pair = 0; pair < pair_count; pair++)
    {
        x = pairs[pair].winner;
        y = pairs[pair].loser;
        strength[pair] = preferences[x][y] - preferences[y][x];
    }

    // insertion sort
    int k, tmp_winner, tmp_loser, tmp_strength;
    for (pair = 0; pair < pair_count; pair++)
    {
        k = pair_count - 1 - pair;
        while (k > 0 and strength[k - 1] < strength[k])
        {
            tmp_winner = pairs[k - 1].winner;
            tmp_loser = pairs[k - 1].loser;
            tmp_strength = strength[k - 1];

            pairs[k - 1].winner = pairs[k].winner;
            pairs[k - 1].loser = pairs[k].loser;
            strength[k - 1] = strength[k];

            pairs[k].winner = tmp_winner;
            pairs[k].loser = tmp_loser;
            strength[k] = tmp_strength;

            k--;
        }
    }
}

void lock_pairs(void)
{
    /*  Lock pairs into the candidate graph in order, without creating cycles.
     *  locked[x][y] means x is locked in over y
     *  expected input like: 3 pairs; A>B, C>A, C>B
     *  output: AB++, CA++, CB++
     *  x2 1 1 0
     *  x1 0 0 0
     *  x0 0 1 0
     */
    int pair, x, y;
    for (pair = 0; pair < pair_count; pair++)
    {
        x = pairs[pair].winner;
        y = pairs[pair].loser;

        // Cycle recursion check
        if (cycle(x, y) == false)
        {
            locked[x][y]++;
        }
    }
}

bool cycle(int winner, int x)
{
    if (x == winner)
    {
        return true;
    }

    for (int y = 0; y < candidate_count; y++)
    {
        if (locked[x][y] == true)
        {
            if (cycle(winner, y) == true)
            {
                return true;
            }
        }
    }

    return false;
}

void print_winner(void)
{
    /* Print the winner of the election. */

    // List of pretenders
    bool pretenders[candidate_count];
    memset(pretenders, true, candidate_count);

    // If a candidate is locked, strike him from the list:
    int x, y;
    for (x = 0; x < candidate_count; x++)
    {
        for (y = 0; y < candidate_count; y++)
        {
            if (pretenders[y] != false and locked[x][y] == true)
            {
                pretenders[y] = false;
            }
        }
    }

    // Find the one last who is not locked and grac:
    for (int candidate = 0; candidate < candidate_count; candidate++)
    {
        if (pretenders[candidate] == true)
        {
            printf("%s\n", candidates[candidate]);
        }
    }
}
