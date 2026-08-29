import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import math
import itertools
import functools

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: M is a maximal ideal in R",
    "¬Q: The n-th symbolic power M^{(n)} is not equal to the ordinary power M^n"
]

def conditions(witness):
    h1, h2, neg_q = False, False, False
    
    R_gen, M_gen, n = None, None, None
    
    if isinstance(witness, tuple) and len(witness) == 3:
        R_gen, M_gen, n = witness
    elif isinstance(witness, dict):
        R_gen = witness.get('R_gen')
        M_gen = witness.get('M_gen')
        n = witness.get('n')
    else:
        try:
            R_gen = witness.R_gen
            M_gen = witness.M_gen
            n = witness.n
        except AttributeError:
            pass

    if isinstance(R_gen, int) and isinstance(M_gen, int) and isinstance(n, int):
        try:
            h1 = True
            
            if R_gen != 0 and M_gen % R_gen == 0:
                h2 = sympy.ntheory.isprime(abs(M_gen // R_gen))
            else:
                h2 = False
                
            neg_q = False
            if h2 and n > 1:
                M_n_gen = M_gen**n
                for x_k in range(1, abs(M_n_gen) + 1):
                    x = R_gen * x_k
                    if x % M_n_gen != 0:
                        for s_k in range(1, abs(M_gen) + 1):
                            s = R_gen * s_k
                            if s % M_gen != 0:
                                if (s * x) % M_n_gen == 0:
                                    neg_q = True
                                    break
                    if neg_q:
                        break
            return [h1, h2, neg_q]
        except Exception:
            pass

    try:
        h1 = bool(witness.R.is_Noetherian())
        h2 = bool(witness.M.is_maximal())
        neg_q = bool(witness.M.symbolic_power(witness.n) != witness.M.ordinary_power(witness.n))
        return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        h1 = bool(witness.is_Noetherian)
        h2 = bool(witness.is_maximal)
        neg_q = bool(witness.symbolic_power != witness.ordinary_power)
        return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]