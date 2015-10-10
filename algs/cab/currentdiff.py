import qdf
import numpy as np

class Currentdiff(qdf.QDF2Distillate):

	def initialize(self, section, name):
		self.set_section(section)
		self.set_name(name)
		self.set_version(1)
		self.register_input("current_mag")
		self.register_output("currentdifference", "A")

    def compute(self, changed_ranges, input_streams, params, report):
	    current_mag = input_streams["current_mag"]


	    currentdifference = report.output("currentdifference")
	    i_cur_mag = 0
	    
	    while  i_cur_mag < len(current_mag):
	      
		    #now peform calculation and output stream
		    time = current_mag[i_cur_mag][0]
		    current_diff = current_mag[i_cur_mag + 1][1] - current_mag[i_cur_mag][1]
		    currentdifference.addreading(time,current_diff)
	    	#increment counter now that calculation is performed for this data point
	    	i_cur_mag += 1
	    

	    currentdifference.addbounds(*changed_ranges["current_mag"])
