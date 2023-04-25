# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 22:12:20 2023
@author: bvoc5

"""

index_width =  8
bit_width   = 24
N           = 256 

clk_signal  = "clk_100Mhz"

demux_file_name = "ntt_core_mux.txt"
demux_file = open(demux_file_name, "w")

demux_file.write("module ntt_core_mux( \n")
demux_file.write("\t input " + clk_signal + ",\n")
demux_file.write("\t input [" + str(index_width - 1) + ":0] index, \n" )
demux_file.write("\t output reg [" + str(bit_width - 1)    + ":0] ntt_data_out, \n")

for i in range(N):
    if(i != (N-1)):
        demux_file.write("\t input [" + str(bit_width - 1) + ":0] ntt_core_out" + str(i) + ", \n") 
    else:
        demux_file.write("\t input [" + str(bit_width - 1) + ":0] ntt_core_out" + str(i) + "); \n") 

demux_file.write("\n")
demux_file.write("\t always @(posedge " + clk_signal + ") begin \n")

for i in range(N):
    if(i == 0):
        demux_file.write("\t \t if(index == 8'd" + str(i) + ") begin \n")
        demux_file.write("\t \t \t ntt_data_out <= ntt_core_out" + str(i) + "; \n")
        demux_file.write("\t \t end\n")
    else:
        demux_file.write("\t \t else if(index == 8'd" + str(i) + ") begin \n")
        demux_file.write("\t \t \t ntt_data_out <= ntt_core_out" + str(i) + "; \n")
        demux_file.write("\t \t end \n") 

demux_file.write("\t end \n")
demux_file.write("endmodule")
demux_file.close() 