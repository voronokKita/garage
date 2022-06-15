/*  fall 2020 CS50 PSet 4: Filter helpers less
 *
 *  Applies filters to BMPs:
 *  Grayscale, Sepia, Reflect and Blur.
 */
#include <math.h>
#include <iso646.h>

#include "helpers.h"

void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    /* Convert am image to grayscale. */
    // Find average RGB:
    int x, y, average;
    for (y = 0; y < height; y++)
    {
        for (x = 0; x < width; x++)
        {
            average = image[y][x].rgbtRed;
            average += image[y][x].rgbtGreen;
            average += image[y][x].rgbtBlue;
            average = roundf(average / 3.0);

            image[y][x].rgbtRed = average;
            image[y][x].rgbtGreen = average;
            image[y][x].rgbtBlue = average;
        }
    }
}

void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    /*  Convert an image to sepia.
     *  Apply the sepia formula:
     *  output Red   = (inputRed * .393) + (inputGreen *.769) + (inputBlue * .189)
     *  output Green = (inputRed * .349) + (inputGreen *.686) + (inputBlue * .168)
     *  output Blue  = (inputRed * .272) + (inputGreen *.534) + (inputBlue * .131)
     */
    int x, y;
    float output_R, output_G, output_B;
    for (y = 0; y < height; y++)
    {
        for (x = 0; x < width; x++)
        {
            output_R = image[y][x].rgbtRed * .393;
            output_R += image[y][x].rgbtGreen * .769;
            output_R += image[y][x].rgbtBlue * .189;

            output_G = image[y][x].rgbtRed * .349;
            output_G += image[y][x].rgbtGreen * .686;
            output_G += image[y][x].rgbtBlue * .168;

            output_B = image[y][x].rgbtRed * .272;
            output_B += image[y][x].rgbtGreen * .534;
            output_B += image[y][x].rgbtBlue * .131;

            image[y][x].rgbtRed = (output_R > 255.0) ? 255 : roundf(output_R);
            image[y][x].rgbtGreen = (output_G > 255.0) ? 255 : roundf(output_G);
            image[y][x].rgbtBlue = (output_B > 255.0) ? 255 : roundf(output_B);
        }
    }
}

void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    /* Reflect an image horizontally. */
    
    int x, y, opposite;
    int tmp_R, tmp_G, tmp_B;
    const int half = width / 2;
    
    // Array reverse:
    for (y = 0; y < height; y++)
    {
        for (x = 0; x < half; x++)
        {
            opposite = width - 1 - x;

            tmp_R = image[y][x].rgbtRed;
            tmp_G = image[y][x].rgbtGreen;
            tmp_B = image[y][x].rgbtBlue;

            image[y][x].rgbtRed = image[y][opposite].rgbtRed;
            image[y][x].rgbtGreen = image[y][opposite].rgbtGreen;
            image[y][x].rgbtBlue = image[y][opposite].rgbtBlue;

            image[y][opposite].rgbtRed = tmp_R;
            image[y][opposite].rgbtGreen = tmp_G;
            image[y][opposite].rgbtBlue = tmp_B;
        }
    }
}

void blur(int height, int width, RGBTRIPLE image[height][width])
{
    /* Blur an image with the box blur. */
    
    RGBTRIPLE blur_image[height][width];
    int x, y, k, j, shift_y, shift_x, divisor;
    int average_red, average_green, average_blue;

    // Fill blurred copy of the image:
    for (y = 0; y < height; y++)
    {
        for (x = 0; x < width; x++)
        {
            // Clear
            average_red = 0;
            average_green = 0;
            average_blue = 0;
            divisor = 0;

            // Box around pixel:
            for (k = -1; k <= 1; k++)
            {
                if (y + k < 0 or y + k >= height)
                    continue;

                for (j = -1; j <= 1; j++)
                {
                    if (x + j < 0 or x + j >= width)
                        continue;

                    // Set indexes
                    shift_y = y + k;
                    shift_x = x + j;

                    // Count average for each color
                    average_red += image[shift_y][shift_x].rgbtRed;
                    average_green += image[shift_y][shift_x].rgbtGreen;
                    average_blue += image[shift_y][shift_x].rgbtBlue;
                    divisor++;
                }
            }
            // Apply
            blur_image[y][x].rgbtRed = roundf((float) average_red / divisor);
            blur_image[y][x].rgbtGreen = roundf((float) average_green / divisor);
            blur_image[y][x].rgbtBlue = roundf((float) average_blue / divisor);
        }
    }

    // Insert into original:
    for (y = 0; y < height; y++)
    {
        for (x = 0; x < width; x++)
        {
            image[y][x].rgbtRed = blur_image[y][x].rgbtRed;
            image[y][x].rgbtGreen = blur_image[y][x].rgbtGreen;
            image[y][x].rgbtBlue = blur_image[y][x].rgbtBlue;
        }
    }
}
