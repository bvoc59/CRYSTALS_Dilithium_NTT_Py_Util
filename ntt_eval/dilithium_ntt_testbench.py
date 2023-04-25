# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 15:32:20 2023
@author: bvoc5
"""

import sys 
import random 
import dilithium_ntt

q = 8380417
r = 1753
N = 256

def initPolynomial():
    a      = [0]*N
    for n in range(N):
        a[n] = int((q-1) * random.random()) 
    return a 

def directForm(a):
    A = [0]*N    
    for k in range(N): 
        ntt_sum = 0 
        for n in range(N): 
            ntt_term = 0 
            if(a[n] != 0): 
                exp_factor = pow(r, (2*k + 1)*n, q)
                ntt_term   = (a[n] * exp_factor) % q
            ntt_sum  = (ntt_term + ntt_sum) % q     
        A[k] = ntt_sum   
    return A 
    

def main(): 
    
    a  = initPolynomial() 
    a1 = a.copy()
    a2 = a.copy() 
    a3 = a.copy() 

    A1 = dilithium_ntt.cooleyTukey_NTT_Radix2(a1) 
    A2 = dilithium_ntt.cooleyTukey_NTT_Radix4(a2) 
    A3 = directForm(a3)

    print(A1)
    print(A2)
    print(A3)

    sys.exit() 
    
if __name__ == "__main__":
    main() 
