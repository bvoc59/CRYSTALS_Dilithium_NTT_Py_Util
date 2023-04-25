# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 20:30:55 2023
@author: bvoc5

Generate test vectors for barret.v testbench file 
in CRYSTALS-Dilithium NTT FPGA Implementation 
"""

import random 

q = 8380417 
r = 8396807
k = 46

test_length  = 16
a_max        = 562949953421311 

test_vec_in      = [] 
test_vec_exp_out = [] 

def barret(a_in):
    t = a_in - ((a_in*r) >> k)*q 
    if(t >= q):
        a_out = t - q
    else:
        a_out = t
    return a_out 

#Open test vector file
barret_test_vec_file = open("barret_test_vec.txt", "w") 

barret_test_vec_file.write("\t //Input test vectors\n")
barret_test_vec_file.write("\t reg [23:0] test_vec_in[0:" + str(test_length - 1) + "];\n")
barret_test_vec_file.write("\n") 

barret_test_vec_file.write("\t //Expected-output test vectors\n")
barret_test_vec_file.write("\t reg [23:0] test_vec_exp_out[0:" + str(test_length - 1) + "];\n")
barret_test_vec_file.write("\n")

for i in range(test_length):
    a_in      = int(a_max * random.random())
    a_out_exp = barret(a_in)
    
    test_vec_in.append(a_in)
    test_vec_exp_out.append(a_out_exp)
 
#Input initial block 
barret_test_vec_file.write("\t initial begin\n") 
for i in range(test_length):
    barret_test_vec_file.write("\t \t test_vec_in[" + str(i) + "] = 49'd" + str(test_vec_in[i]) + ";\n")
    
barret_test_vec_file.write("\t end")
barret_test_vec_file.write("\n") 
barret_test_vec_file.write("\n") 

#Expected output initial block 
barret_test_vec_file.write("\t initial begin\n") 
for i in range(test_length):
    barret_test_vec_file.write("\t \t test_vec_exp_out[" + str(i) + "] = 49'd" + str(test_vec_exp_out[i]) + ";\n")

barret_test_vec_file.write("\t end")
barret_test_vec_file.write("\n") 
        
#Close test vector file 
barret_test_vec_file.close() 
