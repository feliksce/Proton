class Fitter:

	def __init__(self, datafile, verbose=False):

		# properties
		self.verbose = verbose
		self.info("Initialising program...")

		# input
		self.datafile = datafile
		self.data = []

		# calculated or stored data
		self.x = []
		self.y = []
		self.on = []
		self.off = []

	def import_data(self):
		from pandas import read_csv as read
		self.info("Importing data...")
		self.data = read(self.datafile, sep="\t", header=None)
		self.on = self.data[0]
		self.off = self.data[1]
		return self.data

	# fit
	def fit(self, auto_xmin=False):
		from powerlaw import Fit

		def on():
			if auto_xmin:
				experimental = Fit(self.on)
			else:
				experimental = Fit(self.on, xmin=min(self.data))

			pl_alpha = experimental.power_law.alpha
			pl_Lambda = 0
			pl_D = experimental.power_law.D

			tpl_alpha = experimental.truncated_power_law.alpha
			tpl_Lambda = experimental.truncated_power_law.Lambda
			tpl_D = experimental.truncated_power_law.D

			return [[pl_alpha, pl_Lambda, pl_D], [tpl_alpha, tpl_Lambda, tpl_D]]

		def off():
			if auto_xmin:
				experimental = Fit(self.off)
			else:
				experimental = Fit(self.off, xmin=min(self.data))

			pl_alpha = experimental.power_law.alpha
			pl_Lambda = 0
			pl_D = experimental.power_law.D

			tpl_alpha = experimental.truncated_power_law.alpha
			tpl_Lambda = experimental.truncated_power_law.Lambda
			tpl_D = experimental.truncated_power_law.D

			return [[pl_alpha, pl_Lambda, pl_D], [tpl_alpha, tpl_Lambda, tpl_D]]

		self.on = on()
		self.off = off()

		return on(), off()

	def print_output(self):
		filename = self.datafile.split()[-1]
		print(filename)
		for mode in ["ON", "OFF"]:
			print(mode)
			print("\talpha\tlambda\tD value")
			row = "pl"
			if mode == "ON":
				for each in self.on:
					print("{}\t{:0.3f}\t{:0.3f}\t{:0.3f}".format(row, each[0], each[1], each[2]))
					row = "tpl"
				print("\n")
			if mode == "OFF":
				for each in self.off:
					print("{}\t{:0.3f}\t{:0.3f}\t{:0.3f}".format(row, each[0], each[1], each[2]))
					row = "tpl"
				print("\n")

	# verbose mode
	def info(self, information):
		if self.verbose:
			print(information)

	# run whole program
	def main(self):
		self.import_data()
		self.fit()
		self.print_output()
		exit()

if __name__ == "__main__":
	run = Fitter("1.txt", verbose=True)
	run.import_data()
	a, b = run.fit()
	print(a, b)
