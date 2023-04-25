# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 14:58:56 2023
@author: bvoc5

Generate n x n butterfly module for CRYSTALS-Dilithium 
Radix-2 Cooley-Tukey NTT FPGA Implementation 
"""

#Enable cycle counter for start/done signals
clocked_en = 0

def butterfly_gen(n):

    r               = 1753 
    q               = 8380417 
    exp_factor_list = []

    bit_width      = 24
    num_cycles     = 15 
    cycles_width   =  4
    barret_count   =  0 

    clk_signal = "clk_100Mhz"
    rst_signal = "rst_n" 
    str_signal = "start"
    dne_signal = "done"

    #Open file with writing priveleges 
    butterfly_file_name = "ntt_butterfly_"  + str(n) + "x" + str(n)
    butterfly_file      = open(butterfly_file_name + ".txt", "w")

    #Port declaration 
    butterfly_file.write("module "   + butterfly_file_name + "(\n") 
    butterfly_file.write("\t input " + clk_signal + ",\n")
    
    if(clocked_en == 1):
        butterfly_file.write("\t input " + rst_signal + ",\n")
        butterfly_file.write("\t input " + str_signal + ",\n")
    
    #Butterfly input(s)
    for i in range(n):
        butterfly_file.write("\t input [" + str(bit_width - 1) + ":0] ")
        butterfly_file.write("fi_" + str(i) + ",\n")

    #Butterfly output(s) 
    for i in range(n):
        butterfly_file.write("\t output [" + str(bit_width - 1) + ":0] ")
        butterfly_file.write("Fi_" + str(i))

        if(i != (n - 1)):
            butterfly_file.write(",\n")
        else:
            if(clocked_en == 0):
                butterfly_file.write("\n \t );\n")
                butterfly_file.write("\n")
            else:
                butterfly_file.write(",\n")

    if(clocked_en == 1):
        butterfly_file.write("\t output " + dne_signal + "\n")
        butterfly_file.write("\t );\n")
        butterfly_file.write("\n")

    #C_Q_Const
    #butterfly_file.write("\t parameter C_Q_CONST = 24'd" + str(q) + ";\n"); 

    #Twiddle factor calculation 
    for k in range(int(n/2)):
    
        exp_factor      =    int((256 / n)*(2*k + 1))
        pos_twid_factor =      pow( r, exp_factor, q) 
        neg_twid_factor =  q - pow( r, exp_factor, q) 
        
        butterfly_file.write("\t parameter C_POS_R_" + str(exp_factor) + " = 24'd" + str(pos_twid_factor) + ";\n")
        butterfly_file.write("\t parameter C_NEG_R_" + str(exp_factor) + " = 24'd" + str(neg_twid_factor) + ";\n")
        
        exp_factor_list.append(exp_factor)
        
    #Cycles to wait  
    if(clocked_en == 1):
        butterfly_file.write("\t parameter C_CYCLES_TO_WAIT = " + str(cycles_width) + "'d" + str(num_cycles) + ";\n")
    
    butterfly_file.write("\n")
    
    #Subtraction wire declaration 
    #for i in range(int(n/2)):
    #    butterfly_file.write("\t wire [" + str(bit_width-1) + ":0] ")
    #    butterfly_file.write("sub" + str(i) + ";\n")
    #butterfly_file.write("\n")
        
    #Sum wire declaration 
    for i in range(n):
        butterfly_file.write("\t wire [48:0] ")
        #butterfly_file.write("\t wire [" + str(bit_width) + ":0] ")
        butterfly_file.write("sum" + str(i) + ";\n")
            
    butterfly_file.write("\n")
            
    #Product wire declaration 
    for i in range(n):
        butterfly_file.write("\t wire [" + str(2*bit_width - 1) + ":0] ")
        butterfly_file.write("prod" + str(i) + ";\n")
                
    butterfly_file.write("\n")
                
    #Padded sum wire declaration 
    #for i in range(n):
    #    butterfly_file.write("\t wire [" + str(2*bit_width - 1) + ":0] ")
    #    butterfly_file.write("sum" + str(i) + "_pdd;\n")
    
   # butterfly_file.write("\n")

    #Reduced product wire declaration 
    #for i in range(n):
    #    butterfly_file.write("\t wire [" + str(bit_width - 1) + ":0] ")
    #    butterfly_file.write("prod" + str(i) + "_rdd;\n")

    if(clocked_en == 1):    
        butterfly_file.write("\t reg [" + str(cycles_width - 1) + ":0] clk_count;\n")
        butterfly_file.write("\n") 

    #Padded sum assignments 
    #for i in range(n): 
    #    butterfly_file.write("\t assign sum" + str(i) + "_pdd = {" + str(bit_width - 1) + "'d0, sum" + str(i) + "};\n")

    #butterfly_file.write("\n") 
    
    #c_sub_24_bit instantiations 
    #for i in range(int(n/2)):
    #    butterfly_file.write("\t c_sub_24_bit c_sub_24_bit" + str(i)     + "i(")
    #    butterfly_file.write(".CLK("                        + clk_signal + "), ")
    #    butterfly_file.write(".A(C_Q_CONST), ")
    #    butterfly_file.write(".B(C_POS_R_"  + str(exp_factor_list[i]) + "), ")
    #    butterfly_file.write(".S(sub"       + str(i) + "));\n")
    #butterfly_file.write("\n") 

    #mult_gen instantiations
    for i in range(n): 
    
        butterfly_file.write("\t mult_gen_0 mult_gen_" + str(i)     + "i(") 
        butterfly_file.write(".CLK("                   + clk_signal + "), ") 
    
        if(i < int(n/2)):
            butterfly_file.write(".A(fi_"      + str(i + int(n/2))       + "), ")
            butterfly_file.write(".B(C_POS_R_" + str(exp_factor_list[i]) + "), ")
        else:
            butterfly_file.write(".A(fi_"      + str(i)                             + "), ")
            #butterfly_file.write(".B(sub"      + str(i - int(n/2))   + "), ")
            butterfly_file.write(".B(C_NEG_R_" + str(exp_factor_list[i - int(n/2)]) + "), ")

        butterfly_file.write(".P(prod" + str(i) + "));\n")

    butterfly_file.write("\n") 

    #barret instantiations
    #for i in range(n): 
    
        #butterfly_file.write("\t barret barret_" + str(barret_count) + "i(.clk_100Mhz(" + clk_signal + "), ")
        #butterfly_file.write(".rst_n("     + rst_signal + "), ")
        #butterfly_file.write(".a_in(prod"  + str(i)     + "), ")
        #butterfly_file.write(".a_out(prod" + str(i) + "_rdd)); \n")
        #barret_count = barret_count + 1 

    #c_add_0 instantiations
    for i in range(n): 

        butterfly_file.write("\t c_add_0 c_add_"   + str(i) + "i(")
        butterfly_file.write(".A(prod"             + str(i) + "), ")
        #butterfly_file.write(".A(prod"             + str(i) + "_rdd), ")    
        
        if(i < int(n/2)):
            butterfly_file.write(".B(fi_" + str(i)             + "), ")
        else:
            butterfly_file.write(".B(fi_" + str(i - int(n/2))  + "), ")

        butterfly_file.write(".CLK("      + clk_signal + "),  ") 
        butterfly_file.write(".CE(1'b1), ") 
        butterfly_file.write(".S(sum"   + str(i)     + "));\n") 

    butterfly_file.write("\n") 

    #barret instantiations
    for i in range(n): 
    
        butterfly_file.write("\t barret barret_" + str(barret_count) + "i(.clk_100Mhz(" + clk_signal + "), ")
        #butterfly_file.write(".rst_n("     + rst_signal + "), ")
        #butterfly_file.write(".a_in(sum"   + str(i)     + "_pdd), ")
        butterfly_file.write(".a_in(sum"   + str(i)     + "), ")
        butterfly_file.write(".a_out(Fi_"  + str(i)     + ")); \n")
        barret_count = barret_count + 1 

    if(clocked_en == 1):
        butterfly_file.write("\n") 
        butterfly_file.write("\t assign " + dne_signal + " = (clk_count == C_CYCLES_TO_WAIT) ? 1'b1 : 1'b0;\n") 
        butterfly_file.write("\n") 

        #Clock counter
        butterfly_file.write("\t always @ (posedge "  + clk_signal + ") begin \n")
        butterfly_file.write("\t \t if("              + rst_signal + " == 1'b1) begin \n") 
        butterfly_file.write("\t \t \t clk_count <= " + str(cycles_width) + "'d0;\n") 
        butterfly_file.write("\t \t end \n") 

        butterfly_file.write("\t \t else begin\n")
        butterfly_file.write("\t \t \t if(clk_count == C_CYCLES_TO_WAIT) begin\n")
        butterfly_file.write("\t \t \t \t clk_count <= " + str(cycles_width) + "'d0;\n")
        butterfly_file.write("\t \t \t end \n") 

        butterfly_file.write("\t \t \t else begin\n")
        butterfly_file.write("\t \t \t \t if(" + str_signal + " == 1'b1) begin\n")
        butterfly_file.write("\t \t \t \t \t clk_count <= clk_count + " + str(cycles_width) + "'d1;\n")
        butterfly_file.write("\t \t \t \t end \n")
        butterfly_file.write("\t \t \t end \n")
        butterfly_file.write("\t \t end \n")
        butterfly_file.write("\t end \n")
    
    #End module 
    butterfly_file.write("\n")
    butterfly_file.write("endmodule")

    #Close file 
    butterfly_file.close() 
    
#Code to Execute 
butterfly_gen(2)
butterfly_gen(4)
butterfly_gen(8)
butterfly_gen(16)
butterfly_gen(32)
butterfly_gen(64)
butterfly_gen(128)
butterfly_gen(256)
