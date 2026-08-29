import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.matrices import *
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Expected witness format:
    witness = (R_mod, S_mod, phi_dict, f_coeffs)
    where:
      - R_mod, S_mod are integers representing the rings Z/R_mod and Z/S_mod.
      - phi_dict is a dictionary mapping elements of Z/R_mod to Z/S_mod.
      - f_coeffs is a list of integers representing the coefficients of f(x) in Z/R_mod.
    """
    try:
        R_mod, S_mod, phi_dict, f_coeffs = witness
        
        if not (isinstance(R_mod, int) and R_mod > 0): 
            return [False, False, False]
        if not (isinstance(S_mod, int) and S_mod > 0): 
            return [False, False, False]
        if not isinstance(phi_dict, dict): 
            return [False, False, False]
        if not isinstance(f_coeffs, list): 
            return [False, False, False]

        # H1: phi is a ring homomorphism
        h1 = True
        for x in range(R_mod):
            for y in range(R_mod):
                sum_xy = (x + y) % R_mod
                prod_xy = (x * y) % R_mod
                
                phi_x = phi_dict.get(x, 0) % S_mod
                phi_y = phi_dict.get(y, 0) % S_mod
                phi_sum = phi_dict.get(sum_xy, 0) % S_mod
                phi_prod = phi_dict.get(prod_xy, 0) % S_mod
                
                if phi_sum != (phi_x + phi_y) % S_mod:
                    h1 = False
                if phi_prod != (phi_x * phi_y) % S_mod:
                    h1 = False
                    
        # H2: f is a polynomial in R[x]
        h2 = True
        for c in f_coeffs:
            if not isinstance(c, int):
                h2 = False
                
        # neg_Q: The conclusion fails
        # If phi(1) != 1, the tensor product and the polynomial ring are not isomorphic
        # for finite rings S (S_mod > 1).
        neg_q = False
        phi_1 = phi_dict.get(1, 0) % S_mod
        if phi_1 != (1 % S_mod) and S_mod > 1:
            neg_q = True
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: phi is a ring homomorphism",
    "H_2: f is a polynomial over R",
    "not Q: S tensor_R R_x/f is not isomorphic to S_x/f_tilde"
]

N_HYP = 2
NEG_Q_INDEX = 2