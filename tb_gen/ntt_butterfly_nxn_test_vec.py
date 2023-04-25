# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 01:06:59 2023
@author: bvoc5

Generate test vectors for ntt_butterfly_nxn unit testbench file 
in CRYSTALS-Dilithium NTT FPGA Implementation
"""

import random 

q = 8380417 
r = 1753
N = 8 

test_length = 8 

def ntt_nxn_butterfly(fi):

    Fi = [0]*N 
    
    f1 = fi[0 : int(N/2)]
    f2 = fi[int(N/2) : N]
    
    for k in range(int(N/2)): 
        Fi[k]             = (f1[k] + pow(r, int((256/N)*(2*k + 1)), q)*f2[k]) % q
        Fi[k + int(N/2)]  = (f1[k] - pow(r, int((256/N)*(2*k + 1)), q)*f2[k]) % q
        
    return Fi 
    
butterfly_test_vec_file = open("ntt_butterfly_" + str(N) + "x" + str(N) + "_test_vec.txt", "w")
butterfly_test_vec_file.write("\n")

for i in range(N):
    butterfly_test_vec_file.write("\t reg  [23:0] fi_" + str(i) + ";\n")
butterfly_test_vec_file.write("\n")

for i in range(N):
    butterfly_test_vec_file.write("\t wire [23:0] Fi_" + str(i) + ";\n")
butterfly_test_vec_file.write("\n")

for i in range(N):
    butterfly_test_vec_file.write("\t //Input test vectors: fi_"  + str(i) + " \n")
    butterfly_test_vec_file.write("\t reg [23:0] test_vec_in_fi_" + str(i) + "[0:" + str(test_length-1) + "];\n")
    butterfly_test_vec_file.write("\n")
    
for i in range(N):
    butterfly_test_vec_file.write("\t //Expected-output test vectors: Fi_"  + str(i) + " \n")
    butterfly_test_vec_file.write("\t reg [23:0] test_vec_exp_out_Fi_"      + str(i) + "[0:" + str(test_length-1) + "];\n")
    butterfly_test_vec_file.write("\n")
    
butterfly_test_vec_file.write("\t //Initialization Blocks\n") 
for i in range(test_length):
    
    fi = [] 
    for j in range(N):
        fi_in = int((q-1)*random.random()) 
        fi.append(fi_in)
        
    Fi = ntt_nxn_butterfly(fi) 
    
    butterfly_test_vec_file.write("\t initial begin\n")
    
    for j in range(N):
        butterfly_test_vec_file.write("\t \t test_vec_in_fi_" + str(j) + "[" + str(i) + "] = ")
        butterfly_test_vec_file.write("24'd" + str(fi[j]) + ";\n")

    butterfly_test_vec_file.write("\n")
        
    for j in range(N):
        butterfly_test_vec_file.write("\t \t test_vec_exp_out_Fi_" + str(j) + "[" + str(i) + "] = ")
        butterfly_test_vec_file.write("24'd" + str(Fi[j]) + ";\n")
        
    butterfly_test_vec_file.write("\t end\n")
    butterfly_test_vec_file.write("\n")
    
butterfly_test_vec_file.close() 