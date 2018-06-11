# KLTCompressionOfGrayscaleImages script

This is a small script to perform KLT on a grayscale image (e.g. "Lena").
Steps that script does:

1. Partitions image into numerous NxN image blocks.
2. Represents each imageblock lexicographically creating a vector image of the original image.
3. Performs zerocentering and computes covariance matrix.
4. Performs eigen-decomposition of the covariance matrix.
5. Takes a requested number of principles components and calculates square error based on that.

User should provide following arguments:
* **-i**  name of the file containing grayscale image.
* **-b**  size of the imageblock side in pixels, N in NxN

Amount of principle components is represented as a fraction, for example 50% or half of components to be kept for compression is represented as 1/2, third, 33% is represented as 1/3. The user has to provide the numerator and denominator of this fraction:
* **-n**  numerator
* **-d**  denominator

Example for a grayscale file named "lena.png" to be compressed using KLT with 2x2 imageblocks and 3/4 of principle components kept:

`$: python KLTCompressionOfGrayscaleImages.py -i lena.png -b 2 -n 3 -d 4`
