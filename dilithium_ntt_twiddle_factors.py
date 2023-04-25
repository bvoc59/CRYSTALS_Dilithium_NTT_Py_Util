# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 14:43:08 2023
@author: bvoc5

Generate twiddle factors for CRYSTALS-Dilithium 
Cooley-Tukey NTT FPGA Implementation 
"""

q = 8380417 
r = 1753 

twiddle_file = open("twiddle.txt", "w")
 
for j in range(8):
    
    twiddle_file.write("--------------------\n")
    twiddle_file.write("NTT TWIDDLE FACTORS FOR j = " + str(j) + "\n")
    for k in range(int(128/2**j)):
    
        exp_factor      = (2**j)*(2*k + 1) 
        pos_twid_factor =     pow( r, exp_factor, q) 
        neg_twid_factor = q - pow( r, exp_factor, q) 
    
        twiddle_file.write("parameter C_POS_R_" + str(exp_factor) + " = 24'd" + str(pos_twid_factor) + ";\n")
        twiddle_file.write("parameter C_NEG_R_" + str(exp_factor) + " = 24'd" + str(neg_twid_factor) + ";\n")
    
    twiddle_file.write("--------------------\n")

twiddle_file.close() 