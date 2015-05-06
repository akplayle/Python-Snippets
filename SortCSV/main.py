import os
import sys

import argparse
import collections

import csv


class Symbol(object):

	def __init__(self, symbol):
		self.name = symbol

		self.timeStamps = []
		self.quantities = []
		self.prices = []


		self.maxTimeGap = None
		self.volume = None
		self.wAveragePrice = None
		self.maxPrice = None

	def setMaxTimeGap(self):
		if len(self.timeStamps)  == 1:
			self.maxTimeGap = 0
		else:
			maxTime = 0
			for i in range(1, len(self.timeStamps)):
				time_gap = abs(self.timeStamps[i] - self.timeStamps[i -1])
				if time_gap > maxTime:
					maxTime = time_gap

		self.maxTimeGap = maxTime

	def setVolume(self):
		self.volume = sum(self.quantities)

	def setWAveragePrice(self):
		if len(self.prices) != len(self.quantities):
			print 'ERROR inconsistent lists'
			return

		wa = 0.0
		for i in range(len(self.prices)):
			wa = wa + float(self.prices[i]) * float(self.quantities[i])/float(sum(self.quantities))

		self.wAveragePrice = int(wa + 0.5)

	def setMaxPrice(self):
		self.maxPrice = max(self.prices)


class App(object):

	def __init__(self, args = None):
		self.parser = argparse.ArgumentParser(description = 'Parse input and output files')

		self.parser.add_argument('-i', '--input',
			help = "The csv file to read in : assume delimiter is a comma and no content uses such",
			type = str, required = True)
		self.parser.add_argument('-o', '--output',
			help = "The output file to write to",
			type = str, required = True)


		if args is None:
			self.args = self.parser.parse_args()
		else:
			self.args = self.parser.parse_args(args.split())

		self.input = self.args.input
		self.output = self.args.output


		if not os.path.isfile(self.input):
			infile = os.path.join(os.path.dirname(__file__), self.input)


		self.symbols = dict()

	def readCSV(self, input):


		try:
			self.symbols = dict()
			#read csv file
			with open(input, 'rU') as csvfile:
				inputReader = csv.reader(csvfile, delimiter = ',', quotechar = '|')

				for row in inputReader:
					timestamp = int(row[0])
					id = row[1]
					quantity = int(row[2])
					price = int(row[3])

					# instert symbol id if it doesn't exist or consolidate information if it does
					if id not in self.symbols:
						symbol = Symbol(id)
						symbol.timeStamps.append(timestamp)
						symbol.quantities.append(quantity)
						symbol.prices.append(price)
						self.symbols.setdefault(id, symbol)
					else:
						symbol = self.symbols[id]
						symbol.timeStamps.append(timestamp)
						symbol.quantities.append(quantity)
						symbol.prices.append(price)
		except IOError:
			print "ERROR: error reading file, please make sure the input is a valid csv file"

	def writeCSV(self, output):
		
		try:
			# Write csv file
			with open(output, 'wb') as csvfile:
				outputWriter = csv.writer(csvfile, delimiter = ',', quotechar = '|')

				# Calculate informaation and write for each symbol
				sortedKeys = sorted(self.symbols)
				for key in sortedKeys:
					symbol = self.symbols[key]
					symbol.setMaxTimeGap()
					symbol.setVolume()
					symbol.setWAveragePrice()
					symbol.setMaxPrice()

					#setup row format and write
					row = [symbol.name, symbol.maxTimeGap, symbol.volume, symbol.wAveragePrice, symbol.maxPrice]
					outputWriter.writerow(row)
		except IOError:
			print "ERROR: error writing file, please make sure the output is a valid path"

	def run(self):
		self.readCSV(self.input)
		self.writeCSV(self.output)



if __name__ == "__main__":
	app = App()
	app.run()