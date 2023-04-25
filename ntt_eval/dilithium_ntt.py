# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 15:32:20 2023
@author: bvoc5

Radix-2 Cooley-Tukey NTT for CRYSTALS-Dilithium &
Radix-4 Cooley-Tukey NTT for CRYSTALS-Dilithium 

"""

import math

q = 8380417
r = 1753
N = 256
    
def cooleyTukey_NTT_Radix2(a):
    
    bitRevSort(a)
    A = a[:]

    for i in range(int(math.log2(N))):
        N_div = 2**(i+1)
        for j in range(int(N/N_div)):
            A_temp = [0]*N_div
            for k in range(N_div):
                A_temp[k] = A[N_div*j + k]

            F1 = A_temp[0 : int(N_div/2)]
            F2 = A_temp[int(N_div/2) : N_div]
            
            for k in range(int(N_div/2)):
                twid_factor = pow(r, int(128/(2**i)*(2*k + 1)), q)     
                u =                 F1[k]  
                v = (twid_factor *  F2[k]) % q
                F1[k] = (u + v) % q
                F2[k] = (u - v) % q
                
            A_temp[0 : int(N_div/2)]     = F1
            A_temp[int(N_div/2) : N_div] = F2

            for k in range(N_div):
                A[N_div*j + k] = A_temp[k] 

    return A


def bitRev(n):
    return int('{:08b}'.format(n)[::-1], 2)

def bitRevSort(a):
    for n in range(N):
        if(n != bitRev(n)) and (n < bitRev(n)):
            temp         = a[n]
            a[n]         = a[bitRev(n)]
            a[bitRev(n)] = temp  
     