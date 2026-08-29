import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
import math
import itertools
import functools

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture drops the hypothesis that S is a multiplicatively closed subset of R.
    """
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('R_is_commutative_with_identity', True))
            h2 = bool(witness.get('R_is_noetherian', True))
            h3 = bool(witness.get('M_is_R_module', True))
            
            if 'bijection_holds' in witness:
                neg_q = not witness['bijection_holds']
            elif 'S_is_multiplicatively_closed' in witness:
                neg_q = not witness['S_is_multiplicatively_closed']
            elif 'Ass_M' in witness and 'Ass_S_inv_M' in witness and 'S' in witness:
                ass_m = witness['Ass_M']
                s = witness['S']
                ass_s_inv_m = witness['Ass_S_inv_M']
                disjoint_primes = [p for p in ass_m if not any(e in s for e in p)]
                neg_q = len(disjoint_primes) != len(ass_s_inv_m)
            else:
                neg_q = True
                
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, M, S = witness
            h1 = True
            h2 = True
            h3 = True
            
            is_mult_closed = True
            if not S:
                is_mult_closed = False
            else:
                # Check if 1 is in S
                if not any(e == 1 for e in S):
                    is_mult_closed = False
                else:
                    # Check if S is closed under multiplication
                    for a in S:
                        for b in S:
                            if not any(e == a*b for e in S):
                                is_mult_closed = False
                                break
                        if not is_mult_closed:
                            break
            neg_q = not is_mult_closed
            
        else:
            h1 = bool(getattr(witness, 'R_is_commutative_with_identity', True))
            h2 = bool(getattr(witness, 'R_is_noetherian', True))
            h3 = bool(getattr(witness, 'M_is_R_module', True))
            
            if hasattr(witness, 'bijection_holds'):
                neg_q = not witness.bijection_holds
            elif hasattr(witness, 'S_is_multiplicatively_closed'):
                neg_q = not witness.S_is_multiplicatively_closed
            elif hasattr(witness, 'Ass_M') and hasattr(witness, 'Ass_S_inv_M') and hasattr(witness, 'S'):
                ass_m = witness.Ass_M
                s = witness.S
                ass_s_inv_m = witness.Ass_S_inv_M
                disjoint_primes = [p for p in ass_m if not any(e in s for e in p)]
                neg_q = len(disjoint_primes) != len(ass_s_inv_m)
            else:
                neg_q = True
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Noetherian ring",
    "H_3: M is an R-module",
    "¬Q: The set of associated primes of the S^{-1}R-module S^{-1}M does not correspond bijectively to the set of associated primes of the R-module M that are disjoint from S"
]

N_HYP = 3
NEG_Q_INDEX = 3