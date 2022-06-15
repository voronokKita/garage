/*  fall 2020 CS50 PSet 4: Recover
 *
 *  Recovers 50 JPEGs from a forensic image of memory card.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <iso646.h>

// Number of bytes in block of memory
#define MEM_BLOCK 512

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("USAGE: %s card.raw\n", argv[0]);
        return 1;
    }

    // Open a memory card;
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Forensic image cannot be opened for reading.\n");
        return 1;
    }

    // Allocate memory for data buffer;
    BYTE *buffer = malloc(MEM_BLOCK * sizeof(BYTE));
    if (buffer == NULL)
    {
        printf("Dynamic Memory Allocation Fail.\n");
        fclose(card);
        return 2;
    }

    // Pointer to write JPEG's
    FILE *picture = NULL;

    bool jpeg_found = false;
    int filenum = 0;
    char filename[8];
    int readed_bytes = 0;

    // While != EOF:
    while (1)
    {
        // Reads block of bytes into a buffer;
        readed_bytes = fread(buffer, sizeof(BYTE), MEM_BLOCK, card);

        // Break if EOF.
        if (readed_bytes <= 0)
            break;

        // If it's a JPEG header;
        if (buffer[0] == 0xff and buffer[1] == 0xd8 and buffer[2] == 0xff and (buffer[3] & 0xf0) == 0xe0)
        {
            // If previous bytes was another JPEG;
            if (jpeg_found)
                fclose(picture);
            else
                jpeg_found = true;

            // Generate name for JPEG;
            sprintf(filename, "%03i.jpg", filenum);

            // Open file to write;
            picture = fopen(filename, "w");
            if (picture == NULL)
            {
                printf("Could not open %i file to write.\n", filenum);
                fclose(card);
                free(buffer);
                return 3;
            }

            filenum++;
        }
        // Write jpeg data;
        else if (jpeg_found)
        {
            fwrite(buffer, sizeof(BYTE), readed_bytes, picture);
        }
    }

    // End work and exit.
    fclose(picture);
    fclose(card);
    free(buffer);
    return 0;
}
