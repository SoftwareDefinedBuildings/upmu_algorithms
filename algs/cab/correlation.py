import qdf
import numpy as np

class Correlation(qdf.QDF2Distillate):
	def initialize(self, section , name ):
		self.set_section(section)
		self.set_name(name)
		self.set_version(11)
		self.register_input("Signal1")
		self.register_input("Signal2")
		self.register_output("correlation_output","none")
		#take the two signals impose a window on them and 


	def compute(self, changed_ranges, input_streams, params, report):
		#outliers in V1,3,4 mg +- 10 percent of Voltage
		Signal1 = input_streams["Signal1"]
		Signal2 = input_streams["Signal2"]
		correlation_output = report.output("correlation_output")
		i_Signal1 = 0
		i_Signal2 = 0
		windowsize = 10

		i_Signal1_array = []
		i_Signal2_array = []

		#line up first window
		while len(i_Signal1_array)< windowsize and len(i_Signal2_array) < windowsize:
		#if the time at a particular index of signal 1 is not equal to the time at the index of signal 2 increment the index of one of the
			if not (Signal1[i_Signal1][0] == Signal2[i_Signal2][0]): #if times are not equal to one another
				max_time = max(Signal1[i_Signal1][0],Signal2[i_Signal2][0])
				if Signal1[i_Signal1][0] < max_time:
						i_Signal1 += 1
				elif Signal2[i_Signal2][0] < max_time:
						i_Signal2 += 1
			else:
				i_Signal1_array.extend([i_Signal1]) #if signals line up take note of the index of each signal for which they do 
				i_Signal2_array.extend([i_Signal2])
				i_Signal1 += 1
				i_Signal2 += 1


		#continue up until the either signal reaches its end point for the given time window
		lined_up = True
		while i_Signal1 < (len(Signal1)) and i_Signal2 < (len(Signal2)): 

			#once window has been lined up perform calculation
			if lined_up:
				windowed_signal1 = [Signal1[i][1] for i in i_Signal1_array]
				windowed_signal2 = [Signal2[i][1] for i in i_Signal2_array]
				covariance_matrix = np.corrcoef(windowed_signal1,windowed_signal2)
				co = covariance_matrix[0,1]
				#get the starting index for the window and set this to be the corresponding time for window start time. 
				window_starttime = Signal1[i_Signal1_array[0]][0]
				correlation_output.addreading(window_starttime,co)
				#shift over window
				i_Signal1_array = i_Signal1_array[1:]
				i_Signal2_array = i_Signal2_array[1:]
				#note that window is still less than the required windowsize

			

			#line up signals again 
			if not (Signal1[i_Signal1][0] == Signal2[i_Signal2][0]):
				lined_up = False
				max_time = max(Signal1[i_Signal1][0],Signal2[i_Signal2][0])
				if Signal1[i_Signal1][0] < max_time:
						i_Signal1 += 1
				elif Signal2[i_Signal2][0] < max_time:
						i_Signal2 += 1
			else:
				i_Signal1_array.extend([i_Signal1])
				i_Signal2_array.extend([i_Signal2])
				i_Signal1 +=1
				i_Signal2 +=1
				lined_up = True


		

		correlation_output.addbounds(*changed_ranges["Signal1"])
		correlation_output.addbounds(*changed_ranges["Signal2"])
