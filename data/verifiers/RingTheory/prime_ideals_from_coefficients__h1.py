import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
from sympy.polys.rings import ring
import z3
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
    h1_ok = False
    neg_q_ok = False
    
    P_obj = witness
    if isinstance(witness, tuple) and len(witness) == 2:
        P_obj = witness[1]
        
    try:
        h1_ok = bool(P_obj.is_prime)
    except Exception:
        pass

    try:
        R = P_obj.ring
        var_name = 'x'
        while any(str(s) == var_name for s in R.symbols):
            var_name += '_'
        x_sym = sympy.Symbol(var_name)
        
        new_symbols = R.symbols + (x_sym,)
        Rx = ring(new_symbols, R.domain)[0]
        
        Px_gens = [Rx(g) for g in P_obj.gens]
        Px = Rx.ideal(*Px_gens)
        
        neg_q_ok = not bool(Px.is_prime)
    except Exception:
        pass

    if not h1_ok:
        try:
            h1_ok = bool(witness.is_prime_ideal())
        except Exception:
            pass
            
    if not neg_q_ok:
        try:
            neg_q_ok = not bool(witness.is_prime_ideal_in_poly_ring())
        except Exception:
            pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "not Q: P adjoined x is not a prime ideal in the polynomial ring R adjoined x"
]

N_HYP = 1
NEG_Q_INDEX = 1