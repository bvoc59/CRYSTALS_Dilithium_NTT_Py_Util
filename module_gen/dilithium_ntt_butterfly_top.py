# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 17:20:52 2023
@author: bvoc5

Top-level wiring and instantiations for ntt_unit_256x256.v in 
CRYSTALS-Dilithium Cooley-Tukey NTT FPGA Implementation

Output(s): 
ntt_unit_256x256.txt:  256-Input, 256-Output Module with all Butterfly Instantiations 
dilithium_ntt_top.txt: Contains I/O Registers for ntt_unit_256x256.v  
    
"""

bit_width    = 24 
N            = 256 
clk_sig      = "clk_100Mhz" 

dilithium_ntt_top_file  = " "
ntt_unit_256x256_file   = " "

def main():
    
    global dilithium_ntt_top_file
    global ntt_unit_256x256_file
    
    #Open dilithium_ntt_top file with writing priveleges
    dilithium_ntt_top_file_name = "dilithium_ntt_top" 
    dilithium_ntt_top_file      =  open(dilithium_ntt_top_file_name + ".txt", "w")
    
    #2 x 2 Butterfly Input Registers for dilithium_ntt_top
    for i in range(N): 
        dilithium_ntt_top_file.write("\t reg [" + str(bit_width-1) + ":0] ntt_256x256_in" + str(i))
        dilithium_ntt_top_file.write(";\n")
    dilithium_ntt_top_file.write("\n")

    #256 x 256 Butterfly Output Wires for dilithium_ntt_top 
    for i in range(N): 
        dilithium_ntt_top_file.write("\t wire [" + str(bit_width-1) + ":0] ntt_256x256_out" + str(i))
        dilithium_ntt_top_file.write(";\n")  
    dilithium_ntt_top_file.write("\n")
    dilithium_ntt_top_file.write("\n")
    
    #Instantiate ntt_unit_256x256 
    dilithium_ntt_top_file.write("\t ntt_unit_256x256 ntt_unit_256x256i(\n")
    dilithium_ntt_top_file.write("\t \t .clk_100Mhz(" + clk_sig + "),\n")
    
    for i in range(N):
        dilithium_ntt_top_file.write("\t \t .ntt_butterfly_2x2_in" + str(i) + "(ntt_256x256_in" + str(i) + "),\n")
        
    for i in range(N):
        if(i != (N-1)):
            dilithium_ntt_top_file.write("\t \t .ntt_butterfly_256x256_out" + str(i) + "(ntt_256x256_out" + str(i) + "),\n")
        else:
            dilithium_ntt_top_file.write("\t \t .ntt_butterfly_256x256_out" + str(i) + "(ntt_256x256_out" + str(i) + "));\n")
        
    #Close dilithium_ntt_top 
    dilithium_ntt_top_file.close() 
    
    #Open ntt_unit_256x256 file with writing priveleges 
    ntt_unit_256x256_file_name = "ntt_unit_256x256"
    ntt_unit_256x256_file      =  open(ntt_unit_256x256_file_name + ".txt", "w")
    
    #Module Header
    ntt_unit_256x256_file.write("module "   + ntt_unit_256x256_file_name + "(\n") 
    ntt_unit_256x256_file.write("\t input " + clk_sig + ",\n")
    
    #Input Ports 
    for i in range(N):
        ntt_unit_256x256_file.write("\t input[" + str(bit_width - 1) + ":0] ntt_butterfly_2x2_in" + str(i))
        ntt_unit_256x256_file.write(",\n")
        
    #Output Ports 
    for i in range(N):
        ntt_unit_256x256_file.write("\t output[" + str(bit_width - 1) + ":0] ntt_butterfly_256x256_out" + str(i))
        if(i != (N-1)): 
            ntt_unit_256x256_file.write(",\n") 
        else:
            ntt_unit_256x256_file.write(");\n") 
            
    ntt_unit_256x256_file.write("\n")  
    ntt_unit_256x256_file.write("\n")  
        
    #(4 x 4 - 256 x 256) Butterfly Input Wire Declarations 
    for i in range(7):
        butterfly_wire_declare(int(2**(i + 2)))
        
    #Butterfly module instantiations 
    for i in range(8): 
        butterfly_module_instantiate(int(2**(i+1)))
        
    #End module and close file 
    ntt_unit_256x256_file.write("endmodule") 
    ntt_unit_256x256_file.close() 

def butterfly_module_instantiate(n):
    
    global ntt_unit_256x256_file
    
    for i in range(int(256/n)):
        
        ntt_unit_256x256_file.write("\t ntt_butterfly_" + str(n) + "x" + str(n))
        ntt_unit_256x256_file.write(" ntt_butterfly_" + str(n) + "x" + str(n) + "_" + str(i) + "( \n")                        
        ntt_unit_256x256_file.write("\t \t .clk_100Mhz(" + clk_sig + "), \n")
       
        for j in range(n): 
            ntt_unit_256x256_file.write("\t \t .fi_" + str(j) + "(ntt_butterfly_" + str(n)   + "x" + str(n)   + "_in")
            ntt_unit_256x256_file.write(str(n*i + j) + "),\n")
            
        for j in range(n): 
            
            if(n != 256):
                ntt_unit_256x256_file.write("\t \t .Fi_" + str(j) + "(ntt_butterfly_" + str(2*n) + "x" + str(2*n) + "_in")
            else:
                ntt_unit_256x256_file.write("\t \t .Fi_" + str(j) + "(ntt_butterfly_" + str(n) + "x" + str(n) + "_out")

            if(j != (n - 1)):
                ntt_unit_256x256_file.write(str(n*i + j) + "),\n")
            else:
                ntt_unit_256x256_file.write(str(n*i + j) + ")")

        ntt_unit_256x256_file.write("); \n")
        ntt_unit_256x256_file.write("\n")
        
def butterfly_wire_declare(n): 
    
    global ntt_unit_256x256_file 
    
    #Inter-Module Butterfly Input Wires 
    for i in range(N): 
        ntt_unit_256x256_file.write("\t wire [" + str(bit_width-1) + ":0] ntt_butterfly_" + str(n) +  "x" + str(n) + "_in" + str(i))
        ntt_unit_256x256_file.write(";\n")
    ntt_unit_256x256_file.write("\n")

#Code to execute 
if __name__ == "__main__":
    main() 