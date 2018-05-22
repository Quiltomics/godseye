#!/usr/bin/python

# tempSeg.py                                                         #
# Author:  Dario Ghersi, Kasra A. Vand, Bohdan Khomtchouk            #
# Version: 20180521                                                  #
# Goal:    Implementation of the temporal segmentation of time       #
#          series as described in:                                   #
#          Siy, Chundi, Rosenkrantz, and Subramaniam                 #
#          Journal of Software maintenance and evolution, 2007; 11   #
# Usage:   tempSeg.py TIME_SERIES_DIR self.ALPHA P                   #

from collections import defaultdict
from itertools import chain
from config import MIN_SIZE
import glob
import sys


class BioTrend:
	def __init__(self, *args, **kwargs):
    	self.time_series_dir = kwargs["time_serise_dir"]
		self.all_abstr_file_name = kwargs["all_abstr_file_name"]
		self.alpha = kwargs["alpha"]
		self.p = kwargs["p"]

	def acquireTimeSeries(self):
		"""
		Store the time series as a list of dictionaries
		"""
		## set up the variables
		allFiles = glob.glob(self.time_series_dir + "/*")
		timeSeries = [{} for _ in range(numPoints)]
		## process each time point
		for i, f in enumerate(allFiles):
			with open(f) as timePointFile:
				for line in timePointFile:
					token, freq = line[:-1].split()
					# include only tokens above a minimum length
					if len(token) >= MIN_SIZE:
						timeSeries[i][token] = int(freq)
		return timeSeries

	def calcDecomp(self, T):
		"""
		Calculate the optimal decomposition
		"""

		curr = len(T) - 1
		decomp = []
		numCl = len(T[0]) # number of segments
		while curr > 0:
			decomp.append(curr)
			curr = T[curr][numCl - 1]
			numCl -= 1

		decomp.reverse()
		return decomp


	def calcNumPap(self):
		"""
		Calculate the total number of papers per year
		"""

		numPap = defaultdict(int)
		with open(self.all_abstr_file_name) as allAbstrFile:
			for line in allAbstrFile:
				fields = line[:-1].split()
				try:
					numPap[int(fields[0])] += 1
				except ValueError:
					# invalid literal for int() with base 10
					pass
		numPapSorted = [numPap[year] for year in sorted(numPap.keys())]
		return numPapSorted


	def computeSegDiff(self, timeSeries, numPap, self.alpha):
		"""
		Compute the loss for combining two or more segments together
		"""

		numSets = len(timeSeries)
		totSize = numSets * (numSets - 1) / 2
		segDiff = [[0 for x in range(totSize)] for x in range(totSize)]
		## extract the significant items for each item set
		signifItems = [getSignifItems2(timeSeries[i:i+1],
										numPap,
										self.alpha, i, i) for i in range(numSets)]
		## process each possible segment
		for i in range(numSets - 1):
			for j in range(i + 1, numSets):
				# extract the significant items
				#segmentItems = getSignifItems(timeSeries[i:j + 1], self.alpha)
				segmentItems = getSignifItems2(timeSeries[i:j + 1], numPap,
												self.alpha, i, j)
				segDiff[i][j] = fracDiff(signifItems, segmentItems, i, j)

		return segDiff, signifItems


	def fracDiff(self, signifItems, segmentItems, i, j):
		"""
		Compute the cumulative fractional difference between item sets in
		a segment i <= x <= j
		"""

		segmentItems = set(segmentItems)
		fracDiff = sum(len(segmentItems.symmetric_difference(
			set(signifItems[x]))
			) for x in range(i, j+1))

		return fracDiff


	def getSignifItems(self, segment, self.alpha):
		"""
		Extract the items in the segment whose relative
		frequency is above self.alpha
		"""
		totals = sum(Counter(timePoint) for timePoint in segment)
		## extract the items whose relative frequency is >= self.alpha
		total = float(sum(totals.values()))
		signifItems = [
			item for item, value in totals.items()
				if value / total >= self.alpha
					]
		return signifItems


	def getSignifItems2(self, segment, numPap, self.alpha, i, j):
		"""
		Extract the items in the segment whose relative
		frequency is above self.alpha
		"""

		signifItems = []
		avgs = defaultdict(int)
		weights = numPap[i:j+1]
		numSeg = j - i + 1
		for k in range(numSeg):
			timePoint = segment[k]
			for item in timePoint:
				avgs[item] += timePoint[item]

		## extract the items whose relative frequency is >= self.alpha
		total = float(sum(weights))
		signifItems = [
			item for item, value in avgs.items()
				if value / total >= self.alpha
		]
		#print signifItems, i, j
		#sys.exit(1)
		return signifItems


	def optimalSeg(self, segDiff, n):
		"""
		Apply dynamic programming to optimally segment the time series
		"""

		## initialize the R and T arrays, which will contain the loss values
		## and the segmentation path, respectively
		R = [[0 for x in range(self.p)] for x in range(n)]
		T = [[0 for x in range(self.p)] for x in range(n)]

		for j in range(n):
			R[j][0] = segDiff[0][j]
			kmax = min(j + 1, self.p)

			for k in range(1, kmax):
				R[j][k] = R[k - 1][k - 1] + segDiff[k][j]
				T[j][k] = k - 1

			for z in range(k - 1, j):
				if (R[z][k - 1] + segDiff[z + 1][j]) < R[j][k]:
					R[j][k] = R[z][k - 1] + segDiff[z + 1][j]
					T[j][k] = z

		return R, T

	def run(self):
		## calculate the number of papers for each year
		numPap = self.calcNumPap()
		## acquire the time series
		timeSeries = self.acquireTimeSeries()
		## compute the segment difference for each possible segment and
		## the significant items
		segDiff, signifItems = self.computeSegDiff(timeSeries, numPap)
		## run the optimal segmentation algorithm
		R, T = self.optimalSeg(segDiff, len(timeSeries), p)
		for i in range(len(T)):
			print i, T[i]
		## calculate the decomposition
		decomp = self.calcDecomp(T)
		return decomp
