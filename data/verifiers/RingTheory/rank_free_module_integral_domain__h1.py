import sympy
from sympy import S, eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: M is a finitely generated free R-module",
    "¬Q: M has bases of different cardinalities (rank is not well-defined)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            items = list(witness)
        else:
            items = [witness]
            
        h1 = False
        neg_q = False
        
        for w in items:
            w_str = str(w).lower()
            
            # The zero ring lacks IBN (bases of size 0, 1, 2... all span {0} and are linearly independent)
            if (isinstance(w, int) and w == 0) or w == S.Zero or w == trivial or w_str in ['0', 'zero ring', 'trivial ring', 'z1', '{0}']:
                h1 = True
                neg_q = True
                return [h1, neg_q]
                
            # Known non-commutative rings without IBN
            known_counterexamples = [
                'endomorphism', 'end(', 'infinite', 'column-finite', 
                'row-finite', 'b(h)', 'bounded operator',
                'leavitt', 'cuntz'
            ]
            if any(word in w_str for word in known_counterexamples):
                h1 = True
                neg_q = True
                return [h1, neg_q]
                
            # Standard commutative rings have IBN
            if w in [S.Integers, S.Reals, S.Rationals, S.Complexes]:
                h1 = True
                neg_q = False
                return [h1, neg_q]
                
            if hasattr(w, 'is_Matrix') and w.is_Matrix:
                h1 = True
                neg_q = False
                return [h1, neg_q]
                
        return [h1, neg_q]
    except Exception:
        return [False, False]