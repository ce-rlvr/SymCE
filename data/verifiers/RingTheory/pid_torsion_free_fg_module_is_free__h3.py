import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy import Matrix, eye, zeros, S, Integer
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    h2 = False
    neg_q = False
    
    try:
        from sympy.combinatorics import PermutationGroup
        from sympy import Matrix, Integer, S
        
        # If witness is provided as (R, M) where R is the ring of integers
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
            if R == S.Integers:
                witness = M
                
        # If witness is provided as a list of lists, convert to Matrix
        if isinstance(witness, list) and len(witness) > 0 and isinstance(witness[0], list):
            witness = Matrix(witness)
            
        if isinstance(witness, PermutationGroup):
            # Finite abelian groups are finitely generated Z-modules
            h1 = True
            h2 = bool(witness.is_abelian)
            try:
                order = witness.order()
            except TypeError:
                order = witness.order
            # A finite Z-module is free iff it is the trivial module
            neg_q = order > 1
            
        elif isinstance(witness, Matrix):
            # A matrix over Z presents a finitely generated Z-module M = Z^m / Im(A)
            h1 = True
            h2 = all(e.is_integer == True for e in witness)
            if h2:
                k = witness.rank()
                if k == 0:
                    neg_q = False
                else:
                    from sympy import gcd
                    from itertools import combinations
                    minors_gcd = 0
                    # The module is free iff the k-th determinantal divisor D_k is 1
                    for rows in combinations(range(witness.rows), k):
                        for cols in combinations(range(witness.cols), k):
                            minor_val = witness.extract(rows, cols).det()
                            minors_gcd = gcd(minors_gcd, minor_val)
                            if minors_gcd == 1:
                                break
                        if minors_gcd == 1:
                            break
                    neg_q = (minors_gcd != 1)
                    
        elif isinstance(witness, (int, Integer)):
            # An integer n represents the cyclic Z-module Z/nZ
            h1 = True
            h2 = True
            neg_q = abs(witness) > 1
            
        elif isinstance(witness, list) and all(isinstance(x, (int, Integer)) for x in witness):
            # A list of integers represents the direct sum of cyclic Z-modules
            h1 = True
            h2 = True
            neg_q = any(abs(x) > 1 for x in witness)
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is a finitely generated R-module",
    "¬Q: M is not a free R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2