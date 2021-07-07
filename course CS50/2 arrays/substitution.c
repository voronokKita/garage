/*  CS50 PSet 2: Substitution
 *
 *  Uses str-argument as encryption key;
 *  ask user for text and then print encrypted result of that text.
 */

#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

bool check_key(char*);
void substitution(char*, char*);

int main(int argc, char* argv[])
{
    // Is key correct?
    if (argc != 2)
    {
        printf("USAGE: %s alphabetical-key\n", argv[0]);
        return 1;
    }
    else if (check_key(argv[1]) == false)
    {
        return 1;
    }

    char* line = get_string("plaintext: ");

    substitution(line, argv[1]);

    printf("ciphertext: %s\n", line);
    return 0;
}

bool check_key(char* key)
{
    // Key is alphabetical length?
    if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return false;
    }    
    
    bool alphabet[26] = {false};
    for (int letter = 0, c = 0; c < 26; c++)
    {
        // It is only letters?
        if (!isalpha(key[c]))
        {
            printf("Key must contain only letters.\n");
            return false;
        }
        
        // Letters not repeated?
        letter = key[c];
        letter -= isupper(key[c]) ? 65 : 97;     
        if (alphabet[letter] == true)
        {
            printf("Key must not contain repeated characters.\n");
            return false;
        }
        else
        {
            alphabet[letter] = true;
        }
    }

    // Key is correct.
    return true;
}

void substitution(char* line, char* key)
{
    char mask = '\0';
    for (int letter = 0, c = 0; line[c] != '\0'; c++)
    {
        // Crypt letters only:
        if (isalpha(line[c]))
        {
            letter = line[c];

            // Check register
            if (isupper(line[c]))
            {
                letter -= 65;
                mask = isupper(key[letter]) ? key[letter] : toupper(key[letter]);
            }
            else
            {
                letter -= 97;
                mask = islower(key[letter]) ? key[letter] : tolower(key[letter]);
            }

            // Hide letter
            line[c] = mask;
        }
    }
}
