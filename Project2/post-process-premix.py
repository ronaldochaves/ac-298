import os
import csv
import pylab
from scipy import interpolate
from numpy import floor, array

# Set chemckin output file
output_dir = '/Users/roncha/Master Degree/AC-298/Project2/'
prefix = 'CKSoln'
# suffix = 'solution_no_1_Run#'
suffix = 'Flame_SpeedC1_solution_point_value_vs_parameter'
file_format = '.csv'
plot_path = '/Users/roncha/Master Degree/AC-298/Project2/plots'
gases = ['S25', 'S50', 'S75', 'S50C10', 'S50C20', 'S50C30', 'S50C40', 'S50M5', 'S50M20', 'S50M40']
oxidizer = 'air'
mech = 'GRI-mech-modified'
dlmt = '_'


def extract_object(path):
	""" Extract simulation results as list of objects.""" 
	data = []
	with open(path, newline='') as csvfile:
		reader = csv.DictReader(csvfile, skipinitialspace=True)
		for row in reader:
			row = {k:float(v) for k,v in row.items()}
			data.append(row)
	return data


def filter_object(data, data_ref):
	""" Filter list of objects by specific sub-objects. """
	filtered = data
	try:
		for key, value in data_ref.items():
			filtered = list(filter(lambda elem: elem[key] == value, filtered))
	except KeyError:
		print('There is no key', key, 'to be reduced!')
	return filtered


def find_event_on_y(x, y, factor):
	Y_event = factor * y[0]
	f = interpolate.interp1d(y, x)
	T_event = f(Y_event)
	event = (T_event, Y_event)
	return event


def main(path, gas, mech):
	data_all = extract_object(path)

	sls = [_['Flame_speed_(cm/sec)'] for _ in data_all]
	phis = [_['Equivalence_Ratio_C1_Inlet1_Flame_Speed_(C1)_()'] for _ in data_all]
	print(sls)
	print(phis)
	plot_name = gas + '_' + mech + '.eps'

	###
	fig_index = 1
	fig = pylab.figure(fig_index)
	pylab.clf()
	# pylab.axes([0.125, 0.2, 0.95-0.125, 0.95-0.2])
	pylab.xlim(0.5, 2.5)
	pylab.ylim(0, 2.8)
	color = ['r', 'b', 'g', 'k', 'm']
	linestyle = ['-', '--']
	x = array(phis)
	y = array(sls) / 1e2
	clr = color[0]
	ls = linestyle[0]
	lbl = gas
	pylab.plot(x, y, color=clr, ls=ls, label=lbl)
	pylab.xlabel('Equivalence ratio [-]')
	pylab.ylabel('Laminar Flame Speed [m/s]')
	pylab.legend()
	pylab.savefig(os.path.join(plot_path, plot_name))
	pylab.close()


if __name__ == '__main__':
	gas = gases[0]
	case_name = gas + dlmt + oxidizer + dlmt + mech
	output_file_name = prefix + dlmt + case_name + dlmt + suffix
	path = os.path.join(output_dir, case_name, output_file_name + file_format)
	main(path, gas, mech)
