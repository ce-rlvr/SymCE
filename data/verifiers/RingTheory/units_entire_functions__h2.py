import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import *
import math

# Top-level setup
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

CONDITION_LABELS = [
    "H_1: Let H(C) be the ring of entire functions from C to C under pointwise addition and multiplication",
    "¬Q: f is a unit in H(C) if and only if there exists an entire function g in H(C) such that f(z) = e^{g(z)} for all z in C is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    h1_ok = True
    
    try:
        # Evaluate LHS: f is a unit in H(C)
        # Evaluate RHS: there exists an entire function g in H(C) such that f(z) = e^{g(z)}
        
        if not isinstance(witness, sympy.Expr):
            lhs = False
            rhs = False
        else:
            free_syms = witness.free_symbols
            if len(free_syms) > 1:
                lhs = False
                rhs = False
            else:
                z_sym = list(free_syms)[0] if free_syms else sympy.Symbol('z')
                
                from sympy.calculus.singularities import singularities
                
                # Check if witness is entire
                sings = singularities(witness, z_sym)
                is_entire = sings.is_empty
                
                if not is_entire:
                    lhs = False
                    rhs = False
                else:
                    # Check if 1/witness is entire (i.e. witness has no zeros)
                    sings_inv = singularities(1/witness, z_sym)
                    is_unit = sings_inv.is_empty
                    
                    lhs = is_unit
                    rhs = is_unit
                    
        neg_q_ok = not (lhs == rhs)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]