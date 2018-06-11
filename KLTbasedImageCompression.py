from __future__ import print_function
from PIL import Image
from matplotlib import pyplot as plt
import pylab
import os, sys, time
import numpy as np
import argparse

def squareError(vector, cm, evals, evecs, nopc):
	components = [] # to store indexes of components
	
	for x in range(0, np.array(evals).size):
		if np.array(components).size != nopc:
			components.append(x)
		else:
			for y in range(0, nopc):
				minimal = evals[x]
				if minimal > evals[components[y]]:
					minimal = components[y]
					components[y] = x

	b_cap = []

	for x in range(0,np.array(vector).size):
		b_cap.append(0.0)

	for x in range(0, nopc):
		tmp = np.dot(np.array(vector), evecs[components[x]]) * evecs[components[x]]
		b_cap = np.array(b_cap) + np.array(tmp)

	b_minus_bcap = np.array(vector) - np.array(b_cap);
	b_minus_bcap = abs(b_minus_bcap)
	b_minus_bcap = b_minus_bcap * b_minus_bcap

	sq_err = 0

	for x in range(0 , b_minus_bcap.size):
		sq_err += b_minus_bcap[x]

	return sq_err

def klt(a):
    a = np.array(a).transpose() # since we recieve vectors in horizontal arrays
    cm = np.cov(a)
    val,vec = np.linalg.eig(cm)
    return cm,val,np.array(vec).transpose()

# n - block width
# m - block height
def crop(filename, n, m):
	im = Image.open(filename)
	width, height = im.size
	vector_image = [];
   
	for i in range(0, height, m):
		for j in range(0, width, n):
			box = (j, i, j+n, i+m)
			a = im.crop(box) # a is subimage
			block = [] # block with pixelvalues

			for x in range(0, n):
				for y in range(0, m):
					#print(a.getpixel((x,y)))
					block.append(a.getpixel((x,y)))
			vector_image.append(block);

	vector_image = np.array(vector_image);

	mean = np.mean(vector_image, axis=0)

	covmat, eigenval, eigenvecs = klt(np.array(vector_image))

	return vector_image, covmat, eigenval, eigenvecs, mean

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="Filename of grayscale image for analysis")
ap.add_argument("-b", "--block_side", required=True,
	help="Length of block (subimage) side  in number of pixels")
ap.add_argument("-n", "--numerator", required=True,
	help="Numerator of fraction representing amount of principles components kept for compression (e.g 3/4=75% to be kept, 3 is numerator)")
ap.add_argument("-d", "--denominator", required=True,
	help="Denominator of fraction representing amount of principles components kept for compression (e.g. 3/4=75% to be kept, 4 is denominator)")
args = vars(ap.parse_args())

sq_err = 0
numerator, denominator = int(args["numerator"]), int(args["denominator"])
block_side = int(args["block_side"])

t1 = time.time()

print('Block size is {0}x{1}'.format(block_side,block_side))
vi, cm, evals, evecs, mean = crop(args["image"], block_side, block_side)
principal_components = (evals.shape[0]/denominator)*numerator

mean_sq_err = squareError(mean, cm, evals, evecs, principal_components)

t2 = time.time()

print('\nVector image of size: {0}x{1}'.format(vi.shape[0], vi.shape[1]))
print(vi)
print('\nCovariance matrix of size: {0}x{1}'.format(cm.shape[0], cm.shape[1]))
print(cm)
print('\nEigenvalues: {0}'.format(evals.shape[0]))
print(evals)
print("\nEigenvectors:")
print(evecs)

print('\nTotal number of principal components:		{0}'.format(evals.shape[0]))
print('Number of principal components kept:		{0}'.format(principal_components))
print('Square error for mean vector: 			{0}'.format(mean_sq_err))
print ('Time for calculation: 				%.2f sec\n' % (t2-t1))