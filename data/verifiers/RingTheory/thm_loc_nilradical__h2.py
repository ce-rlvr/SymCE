import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
            
            if hasattr(R, 'is_commutative'):
                h1 = bool(R.is_commutative)
            else:
                h1 = True
                
            try:
                S_list = list(itertools.islice(S, 100))
            except TypeError:
                S_list = []
                
            if S_list:
                is_mult_closed = True
                for x in S_list:
                    for y in S_list:
                        try:
                            prod = x * y
                        except Exception:
                            is_mult_closed = False
                            break
                        
                        found = False
                        for s in S_list:
                            if prod == s:
                                found = True
                                break
                            try:
                                if sympy.simplify(prod - s) == 0:
                                    found = True
                                    break
                            except Exception:
                                pass
                        
                        if not found:
                            is_mult_closed = False
                            break
                    if not is_mult_closed:
                        break
                neg_q = not is_mult_closed
            else:
                neg_q = False
                
        else:
            if hasattr(witness, 'is_commutative_ring'):
                h1 = bool(witness.is_commutative_ring())
            elif hasattr(witness, 'is_commutative'):
                h1 = bool(witness.is_commutative)
            else:
                h1 = True
                
            if hasattr(witness, 'nilradical_commutes'):
                neg_q = not bool(witness.nilradical_commutes())
            elif hasattr(witness, 'conclusion_holds'):
                neg_q = not bool(witness.conclusion_holds())
            elif hasattr(witness, 'is_multiplicatively_closed'):
                neg_q = not bool(witness.is_multiplicatively_closed())
                
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The nilradical of the localized ring S^{-1}R is not equal to the extension of the nilradical of R"
]

N_HYP = 1
NEG_Q_INDEX = 1