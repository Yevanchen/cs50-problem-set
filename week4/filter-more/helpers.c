#include <math.h>
#include "helpers.h"

// 将图像转换为灰度
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // 遍历每个像素
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // 计算RGB平均值
            float gray = 0.299 * image[i][j].rgbtRed + 
                        0.587 * image[i][j].rgbtGreen + 
                        0.114 * image[i][j].rgbtBlue;
            
            // 四舍五入取整
            int roundedGray = (int)(gray + 0.5);
            
            // 将RGB三个通道都设为相同的灰度值
            image[i][j].rgbtRed = roundedGray;
            image[i][j].rgbtGreen = roundedGray; 
            image[i][j].rgbtBlue = roundedGray;
        }
    }
    return;
}

// 水平翻转图像
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // 遍历每一行
    for (int i = 0; i < height; i++)
    {
        // 只需要遍历到宽度的一半
        for (int j = 0; j < width / 2; j++)
        {
            // 使用临时变量交换像素
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of the image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    
    // For each pixel in the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int redSum = 0, greenSum = 0, blueSum = 0;
            float count = 0.0;
            
            // For each pixel in the blur box
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    // Check if pixel is valid
                    if (i + di >= 0 && i + di < height && j + dj >= 0 && j + dj < width)
                    {
                        redSum += copy[i + di][j + dj].rgbtRed;
                        greenSum += copy[i + di][j + dj].rgbtGreen;
                        blueSum += copy[i + di][j + dj].rgbtBlue;
                        count++;
                    }
                }
            }
            
            // Calculate average and update pixel
            image[i][j].rgbtRed = round(redSum / count);
            image[i][j].rgbtGreen = round(greenSum / count);
            image[i][j].rgbtBlue = round(blueSum / count);
        }
    }
    
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of the image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // Sobel kernels
    int Gx[3][3] = {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };
    int Gy[3][3] = {
        {-1, -2, -1},
        {0, 0, 0},
        {1, 2, 1}
    };

    // For each pixel in the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int redX = 0, greenX = 0, blueX = 0;
            int redY = 0, greenY = 0, blueY = 0;

            // For each pixel in the 3x3 box
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    // Check if pixel is valid
                    if (i + di >= 0 && i + di < height && j + dj >= 0 && j + dj < width)
                    {
                        // Calculate Gx
                        redX += copy[i + di][j + dj].rgbtRed * Gx[di + 1][dj + 1];
                        greenX += copy[i + di][j + dj].rgbtGreen * Gx[di + 1][dj + 1];
                        blueX += copy[i + di][j + dj].rgbtBlue * Gx[di + 1][dj + 1];

                        // Calculate Gy
                        redY += copy[i + di][j + dj].rgbtRed * Gy[di + 1][dj + 1];
                        greenY += copy[i + di][j + dj].rgbtGreen * Gy[di + 1][dj + 1];
                        blueY += copy[i + di][j + dj].rgbtBlue * Gy[di + 1][dj + 1];
                    }
                }
            }

            // Calculate final values using Sobel formula
            int red = round(sqrt(redX * redX + redY * redY));
            int green = round(sqrt(greenX * greenX + greenY * greenY));
            int blue = round(sqrt(blueX * blueX + blueY * blueY));

            // Cap values at 255
            image[i][j].rgbtRed = (red > 255) ? 255 : red;
            image[i][j].rgbtGreen = (green > 255) ? 255 : green;
            image[i][j].rgbtBlue = (blue > 255) ? 255 : blue;
        }
    }

    return;
}
