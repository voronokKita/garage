/*  fall 2020 CS50 Lab 4: Volume
 *
 *  Modifies the volume of an audio file using number-factor;
 *  Gets 3 command arguments: input audio file, name of output file, and number-factor.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <ctype.h>
#include <iso646.h>
#include <stdbool.h>

// Number of bytes in .wav header
const uint8_t HEADER_SIZE = 44;

bool copy_header(FILE *, FILE *, uint8_t *);
bool read_write_buffer(FILE *, FILE *, float);

int main(int argc, char *argv[])
{
    if (argc != 4)
    {
        printf("USAGE: %s input.wav output.wav factor\n", argv[0]);
        return 1;
    }

    // Determine scaling factor:
    for (int i = 0; argv[3][i] != '\0'; i++)
    {
        if (isdigit(argv[3][i]) == 0 and argv[3][i] != '.')
        {
            printf("Scaling factor must be digit.\n");
            return 2;
        }
    }
    float factor = atof(argv[3]);

    // Open files;
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open input file.\n");
        return 3;
    }
    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open output file.\n");
        fclose(input);
        return 4;
    }

    // DMA for header:
    uint8_t *header = malloc(HEADER_SIZE * sizeof(uint8_t));
    if (header == NULL)
    {
        printf("Dynamic Memory Allocation Fail.\n");
        fclose(input);
        fclose(output);
        return 5;
    }

    // Copy header from input to output file:
    if (copy_header(input, output, header) == false)
    {
        printf("Fail to read-write header.\n");
        fclose(input);
        fclose(output);
        free(header);
        return 6;
    }
    else
    {
        free(header);
    }

    // Read samples from input file and write updated data to output file:
    if (read_write_buffer(input, output, factor) == false)
    {
        printf("Error read-write buffer.\n");
        fclose(input);
        fclose(output);
        return 7;
    }

    // Close files and exit.
    fclose(input);
    fclose(output);
    return 0;
}

bool copy_header(FILE *input, FILE *output, uint8_t *header)
{
    if (fread(header, sizeof(uint8_t), HEADER_SIZE, input) == 0)
        return false;

    if (fwrite(header, sizeof(uint8_t), HEADER_SIZE, output) == 0)
        return false;

    return true;
}

bool read_write_buffer(FILE *input, FILE *output, float factor)
{
    int16_t buffer;

    while (fread(&buffer, sizeof(int16_t), 1, input) != 0)
    {
        buffer *= factor;

        if (fwrite(&buffer, sizeof(int16_t), 1, output) == 0)
            return false;
    }

    return true;
}
