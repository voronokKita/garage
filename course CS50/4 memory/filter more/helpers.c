/*  fall 2020 CS50 PSet 4: Filter helpers more
 *
 *  Applies filters to BMPs:
 *  Grayscale, Reflect, Blur and Edges with the Sobel–Feldman operator.
 */
#include <math.h>
#include <iso646.h>

#include "helpers.h"

void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    /* Convert an image to grayscale. */
    
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
    
    // Copy of the image
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

void edges(int height, int width, RGBTRIPLE image[height][width])
{
    /* Detect edges with the Sobel–Feldman operator. */

    const int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    const int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    // Copy of the image
    RGBTRIPLE image_copy[height][width];

    int x, y, k, j, s_y, s_x;
    int shift_x, shift_y;
    int sum_x_red, sum_x_green, sum_x_blue;
    int sum_y_red, sum_y_green, sum_y_blue;
    double G_red, G_green, G_blue;
    
    // Sobel algorithm:
    for (y = 0; y < height; y++)
    {
        for (x = 0; x < width; x++)
        {
            // Clear
            sum_x_red = 0;
            sum_x_green = 0;
            sum_x_blue = 0;
            sum_y_red = 0;
            sum_y_green = 0;
            sum_y_blue = 0;
            G_red = 0;
            G_green = 0;
            G_blue = 0;

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
                    s_y = k + 1;
                    s_x = j + 1;

                    // Apply Sobel–Feldman algorithm to every color:
                    sum_x_red += (image[shift_y][shift_x].rgbtRed * Gx[s_y][s_x]);
                    sum_x_green += (image[shift_y][shift_x].rgbtGreen * Gx[s_y][s_x]);
                    sum_x_blue += (image[shift_y][shift_x].rgbtBlue * Gx[s_y][s_x]);

                    sum_y_red += (image[shift_y][shift_x].rgbtRed * Gy[s_y][s_x]);
                    sum_y_green += (image[shift_y][shift_x].rgbtGreen * Gy[s_y][s_x]);
                    sum_y_blue += (image[shift_y][shift_x].rgbtBlue * Gy[s_y][s_x]);
                }
            }

            // Calculating the square root of Gx^2 + Gy^2
            G_red = sqrt(pow(sum_x_red, 2) + pow(sum_y_red, 2));
            G_green = sqrt(pow(sum_x_green, 2) + pow(sum_y_green, 2));
            G_blue = sqrt(pow(sum_x_blue, 2) + pow(sum_y_blue, 2));

            // Capped or round, and add pixel to copy
            image_copy[y][x].rgbtRed = (G_red > 255.0) ? 255 : round(G_red);
            image_copy[y][x].rgbtGreen = (G_green > 255.0) ? 255 : round(G_green);
            image_copy[y][x].rgbtBlue = (G_blue > 255.0) ? 255 : round(G_blue);
        }
    }

    // Insert the copy into the original:
    for (y = 0; y < height; y++)
    {
        for (x = 0; x < width; x++)
        {
            image[y][x].rgbtRed = image_copy[y][x].rgbtRed;
            image[y][x].rgbtGreen = image_copy[y][x].rgbtGreen;
            image[y][x].rgbtBlue = image_copy[y][x].rgbtBlue;
        }
    }
}
