import qdf
import numpy as np

class Phase_Reverse (qdf.QDF2Distillate):
  def initialize(self, section="Phase_Reverse", name="default"):
		self.set_section(section)
		self.set_name(name)
		self.set_version(1)
		self.register_output("phase_reverse", "Degrees")
		self.register_input("phase1")

  def compute(self, changed_ranges, input_streams, params, report):
		phase_reverse_output = report.output("phase_reverse")
		phase1 = input_streams["phase1"]

		i1 = 0
		while i1 < len(phase1):
			time = phase1[i1][0]
			pr = (phase1[i1][1] + 180) % 360
			phase_reverse_output.addreading(time,pr)
			i1 += 1

		phase_reverse_output.addbounds(*changed_ranges["phase1"])
