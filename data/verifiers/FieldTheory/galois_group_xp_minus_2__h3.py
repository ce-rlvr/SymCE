import sympy
from sympy import Symbol, Poly
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        p = None
        L_order = None
        
        # Extract p and L_order from the witness
        if isinstance(witness, tuple):
            p = witness[0]
            if len(witness) >= 2:
                L_order = witness[1]
        elif isinstance(witness, dict):
            p = witness.get('p')
            L_order = witness.get('L_order', witness.get('L_galois_order'))
        else:
            p = witness
            
        # H_1: p is an odd prime number
        try:
            h1 = sympy.isprime(p) and p % 2 != 0
        except Exception:
            h1 = False
            
        # H_2: f(x) = x^p - 2 is a polynomial over Q
        try:
            h2 = isinstance(p, int) and p > 0
        except Exception:
            h2 = False
            
        # ¬Q: The Galois group Gal(L/Q) does not have order p(p-1)
        try:
            if L_order is not None:
                neg_q = L_order != p * (p - 1)
            else:
                neg_q = False
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: f(x) = x^p - 2 is a polynomial over Q",
    "¬Q: The Galois group Gal(L/Q) does not have order p(p-1)"
]

N_HYP = 2
NEG_Q_INDEX = 2