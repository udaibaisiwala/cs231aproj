import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread



def getDistance(pixel1, pixel2):

	distance = 0.0
	for i in range(len(pixel1)):
		distance+=pixel2[i]-pixel1[i]
	distance = distance**2

	return distance

def findCorrespondences(line1, line2, row):
	print line1.shape
	distances = {};
	skipCost = 50;
	editGrid = {}
	for i in range(line1.shape[0]):
		editGrid[i, -1] = ((i+1)*skipCost, "-")
		editGrid[-1, i] = ((i+1)*skipCost, "-")
	editGrid[-1, -1] = (0, "-")

	for i in range(line1.shape[0]):
		print i;
		for j in range(line2.shape[0]):
			distance = getDistance((i, line1[i][0], line1[i][1], line1[i][2]), (j, line2[j][0], line2[j][1], line2[j][2]))
			if int(distance)/1000 not in distances.keys():
				distances[int(distance)/1000] = 1
			else:
				distances[int(distance)/1000]+=1
			if distance<skipCost:
				editGrid[i, j] = (editGrid[i-1, j-1][0] + distance, "m")
			elif editGrid[i-1, j][0]<editGrid[i, j-1][0]:
				editGrid[i, j] = (editGrid[i-1, j][0] + skipCost, "si")
			else:
				editGrid[i, j] = (editGrid[i, j-1][0] + skipCost, "sj")

	for key in distances.keys():
		print key, distances[key]

	correspondences = []
	i = line1.shape[0]-1
	j = line2.shape[0]-1
	prev = editGrid[i, j][1]
	while not prev=="-":
		if(prev=="m"):
			correspondences.append(((row, i), (row, j)))
			i-=1
			j-=1
		elif prev=="si":
			i-=1
		else:
			j-=1

		prev = editGrid[i, j][1]

	print "final cost is ", editGrid[line1.shape[0]-1, line2.shape[0]-1]

	return correspondences


if __name__ == '__main__':

	fileNom = 'Adirondack-perfect'

	leftImg = imread('data/'+fileNom+"/im0.png");
	rightImg = imread('data/'+fileNom+"/im1.png"); #remember - camera to the right, not image

	print("pls confirm calib distance is correct.");
	calib = 209.059

	allCorr = []

	for i in range(500, 750, 25):
		allCorr = allCorr + findCorrespondences(leftImg[i, 1000:1500], rightImg[i, 1000:1500], i)

	print allCorr

	for i in range(len(allCorr)):
		leftImg[allCorr[i][0]] = (0,0,0)
		rightImg[allCorr[i][1]] = (0,0,0)

	plt.imshow(leftImg)
	plt.show()

	plt.imshow(rightImg)
	plt.show()






