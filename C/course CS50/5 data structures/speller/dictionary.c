/*  CS50 PSet 5: Speller
 *
 *  Implements a dictionary's functionality.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Pointer to future hash_table
node *hash_table = NULL;

// Number of "buckets" in hash table
unsigned int BUCKETS = 1;

// Lazy way: max number of words in one "bucket"
const int PACK = 30;

unsigned int WORDS_FOUND = 0;

bool load(const char *dictionary)
{
    /*  Loads dictionary into memory, returning true if successful, else false.
     *
     *  May assume that any dictionary passed to program will be structured exactly same way,
     *  alphabetically sorted from top to bottom with one word per line, each of which ends
     *  with '\n'. Dictionary will contain at least one word, no word will be longer than LENGTH
     *  (a constant defined in dictionary.h) characters, that no word will appear more
     *  than once, that each word will contain only lowercase alphabetical characters and
     *  possibly apostrophes, and no word will start with an apostrophe.
     */
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }

    // Pre-process dictionary in order to count words;
    for (char c = getc(dict); c != EOF; c = getc(dict))
    {
        if (c == '\n')
        {
            WORDS_FOUND++;
        }
    }
    rewind(dict);

    // Count number of "buckets" needed in hash table;
    BUCKETS = WORDS_FOUND / PACK;
    BUCKETS = BUCKETS > 0 ? BUCKETS : 1;

    // Allocate memory for dictionary;
    hash_table = malloc(BUCKETS * sizeof(node));
    if (hash_table == NULL)
    {
        printf("Dynamic Memory Allocation Fail.\n");
        return false;
    }

    // Initialise values;
    node *n = NULL;
    unsigned int h;
    for (h = 0; h < BUCKETS; h++)
    {
        n = &hash_table[h];
        n->word[0] = '\0';
        n->next = NULL;
    }

    node *list = NULL;
    char dict_word[LENGTH + 1];
    // Read strings from a file:
    while (fscanf(dict, "%s", dict_word) != EOF)
    {
        // Hash word to obtain a hash value;
        h = hash(dict_word);

        // Look at linked list with this hash;
        n = &hash_table[h];

        // If list already have words:
        if (n->word[0] != '\0')
        {
            // Create a new node;
            n = malloc(sizeof(node));
            if (n == NULL)
            {
                printf("Dynamic Memory Allocation Fail.\n");
                return false;
            }

            // Insert new node into linked list;
            list = &hash_table[h];
            n->next = list->next;
            list->next = n;
        }

        // Insert word into node.
        strcpy(n->word, dict_word);
    }

    // Dictionary load successful.
    fclose(dict);
    return true;
}

unsigned int hash(const char *word)
{
    /*  Hashes word to a number.
     *  Thanks for the algorithm goto:
     *  https://e-maxx.ru/algo/string_hashes
     */
    size_t len = strlen(word);
    char s[len + 1];
    strcpy(s, word);
    
    for (int i = 0; i < len; i++)
    {
        s[i] = tolower(s[i]);
    }

    const int P = 31;
    long long h = 0, p_pow = 1;

    // hash 1:
    for (size_t i = 0; i < len; i++)
    {
        h += (s[i] - 'a' + 1) * p_pow;
        p_pow *= P;
    }

    // hash 2:
    h %= BUCKETS;
    if (h < 0)
    {
        h *= -1;
    }

    return h;
}

unsigned int size(void)
{
    /* Returns number of words in dictionary if loaded, else 0 if not yet loaded. */
    return WORDS_FOUND;
}

bool check(const char *word)
{
    /*  Returns true if word is in dictionary, else false.
     *
     *  May assume that check will only be passed words that contain (uppercase or lowercase)
     *  alphabetical characters and possibly apostrophes.
     */
    // Get hash from word;
    unsigned int h = hash(word);

    // Make the cursor and point to table with hash;
    node *cursor = &hash_table[h];

    // Check words in a linked list:
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            // 1 word found.
            return true;
        }

        cursor = cursor->next;
    }

    // 0 word not found.
    return false;
}

bool unload(void)
{
    /* Unloads dictionary from memory. */

    node *todell = NULL;
    node *cursor = NULL;

    // Free linked lists:
    for (unsigned int h = 0; h < BUCKETS; h++)
    {
        cursor = &hash_table[h];
        cursor = cursor->next;

        while (cursor != NULL)
        {
            todell = cursor;
            cursor = cursor->next;
            free(todell);
        }
    }

    // Free dictionary hash table;
    free(hash_table);

    // Unload successful.
    return true;
}
