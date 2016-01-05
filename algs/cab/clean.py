import qdf

class Clean (qdf.QDF2Distillate):
  def initialize(self, section="Clean", name="default", stream_type="ANG"):
    self.set_section(section)
    self.set_name(name)
    self.set_version(2)

    if 'ANG' in stream_type:
      units = 'deg'
    elif 'MAG' in stream_type:
      if 'C' in stream_type:
        units = 'A'
      else:
        units = 'V'
    elif 'LSTATE' in stream_type:
      units = 'bitmap'
    else:
      units = 'arb'

    self.register_output('CLEAN', units)
    self.register_input('raw')
    self.register_input('LSTATE')

  def compute(self, changed_ranges, input_streams, params, report):
    raw = input_streams['raw']
    lstates = input_streams['LSTATE']
    clean = report.output('CLEAN')
    
    # for point in raw:
      # clean.addreading(point[0], point[1])
    
    i1 = 0
    i2 = 0
    while i1 < len(lstates) and i2 < len(raw):
      if not (lstates[i1][0] == raw[i2][0]):
        # if times do not align, iteratively increment trailing stream until equal
        max_time = max(lstates[i1][0], raw[i2][0])
        if lstates[i1][0] < max_time:
          i1 += 1
        if raw[i2][0] < max_time:
          i2 += 1
        continue

      if lstates[i1][1] == 0:
        clean.addreading(raw[i2][0], raw[i2][1])

      #increment counters and loop
      i1 += 1
      i2 += 1

    clean.addbounds(*changed_ranges['raw'])
    clean.addbounds(*changed_ranges['LSTATE'])
