from distillate import Distillate
from library import *
from get_stream import *
import numpy as np
import math
import qdf
Stream=[]
Stream_id=[]
Out=[]
Calculation=input('Enter 1 for DPF 2 for sequence 3 for angle difference 4 for total dpf pos seq: ')
while True:
        stream=input("Enter the stream name or N (eg 'upmu/grizzly_new/L1ANG'): ")
        if stream !='N':
           Stream.append(stream)
           temp=get_streams(stream)
           Stream_id.append(temp)
           continue 
        else:
           break 
print   Stream_id      
while True:        
        out=input('Enter out put stream name or N: ')
        if out !='N':
           Out.append(out)                             
           continue
        else:
           break                                   

def compute(input_streams):
        if Calculation==1:
          DPF_A= DPF(input_streams)
          return[DPF_A]
        
    
opts = { 'input_streams'  : Stream, \
         'input_uids'     : ['4b7fec6d-270e-4bd6-b301-0eac6df17ca2', 'b4776088-2f85-4c75-90cd-7472a949a8fa'], \
         'start_date'     : '2014-10-01T00:00:00.000000', \
         'end_date'       : '2014-10-19T00:00:00.000000', \
         'output_streams' : Out, \
         'output_units'   : ['Precent','Precent','Precent'], \
         'author'         : 'Andrew', \
         'name'           : 'Test', \
         'version'        : 6, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()
