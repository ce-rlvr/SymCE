import sympy as sp
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            sigma = witness.get('sigma')
            n = witness.get('n')
            if not isinstance(sigma, Permutation) or not isinstance(n, int):
                return [False, False]
        elif isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], Permutation) and isinstance(witness[1], int):
                sigma, n = witness
            elif isinstance(witness[1], Permutation) and isinstance(witness[0], int):
                n, sigma = witness
            else:
                return [False, False]
        else:
            return [False, False]
            
        if n < 1:
            return [False, False]
        h1 = True
    except Exception:
        return [False, False]
        
    try:
        max_idx = max(n, sigma.size)
        x = sp.symbols(f'x0:{max_idx}')
        
        delta = sp.Integer(1)
        for i in range(n):
            for j in range(i + 1, n):
                delta *= (x[i] - x[j])
                
        def apply_sigma(sig, idx):
            if idx < sig.size:
                return sig(idx)
            return idx
            
        sigma_delta = sp.Integer(1)
        for i in range(n):
            for j in range(i + 1, n):
                idx_i = apply_sigma(sigma, i)
                idx_j = apply_sigma(sigma, j)
                sigma_delta *= (x[idx_i] - x[idx_j])
                
        sgn = sigma.signature()
        
        diff = sp.expand(sigma_delta - sgn * delta)
        q = (diff == 0)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Delta is the alternating polynomial in n variables",
    "¬Q: The action of sigma on Delta does not yield sgn(sigma)*Delta"
]

N_HYP = 1
NEG_Q_INDEX = 1