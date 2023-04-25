# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 22:58:06 2023
@author: bvoc5
"""

temp_file = open("temp.txt", "w")

for i in range(256):
    temp_file.write("\t wire  [23:0] ntt_core_in" + str(i) + ";\n")
        
#for i in range(256):
#    temp_file.write("\t wire [23:0] ntt_core_out" + str(i) + ";\n")
 
#for i in range(256):
#    temp_file.write("\t .ntt_core_in" + str(i) + "(")
#    temp_file.write("ntt_core_in"     + str(i) + "),\n")


#for i in range(256): 
#    temp_file.write("\t .ntt_butterfly_2x2_in" + str(i) + "(")
#    temp_file.write("ntt_core_in" + str(i) + "), \n")

#for i in range(256):
#    temp_file.write("\t .ntt_butterfly_256x256_out" + str(i) + "(")
#    temp_file.write("ntt_core_out" + str(i) + "),\n")

#for i in range(256):
#    temp_file.write("\t .ntt_core_out" + str(i) + "(")
#    temp_file.write("ntt_core_out" + str(i) + "),\n")

temp_file.close() 