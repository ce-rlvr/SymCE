import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Matrix, Symbol, expand, eye, zeros

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
    try:
        if isinstance(witness, dict):
            sigma = witness.get('sigma')
            P = witness.get('P')
        elif hasattr(witness, 'sigma') and hasattr(witness, 'P'):
            sigma = witness.sigma
            P = witness.P
        else:
            sigma, P = witness
            
        h1 = isinstance(sigma, Permutation) and isinstance(P, Matrix) and P.is_square and P.rows == sigma.size
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            sigma = witness.get('sigma')
            P = witness.get('P')
        elif hasattr(witness, 'sigma') and hasattr(witness, 'P'):
            sigma = witness.sigma
            P = witness.P
        else:
            sigma, P = witness
            
        if not (isinstance(sigma, Permutation) and isinstance(P, Matrix) and P.is_square):
            neg_q = False
        else:
            t = Symbol('t')
            L = [len(c) for c in sigma.full_cyclic_form]
            
            expected_poly = 1
            for l in L:
                expected_poly *= (t**l - 1)
                
            actual_poly = P.charpoly(t).as_expr()
            
            neg_q = bool(expand(actual_poly - expected_poly) != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: sigma is a permutation and P is a square matrix of the same size",
    "¬Q: The characteristic polynomial of P is not the product of (t^{L_i} - 1)"
]

N_HYP = 1
NEG_Q_INDEX = 1