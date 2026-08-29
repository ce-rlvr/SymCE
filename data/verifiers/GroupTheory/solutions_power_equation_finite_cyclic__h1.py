import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, m = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a finite group
    try:
        n_val = G.order() if callable(G.order) else G.order
        n = int(n_val)
        h1 = isinstance(G, PermutationGroup) and n > 0
    except Exception:
        h1 = False
        
    # H_2: m is an integer
    try:
        h2 = isinstance(m, (int, sympy.Integer))
    except Exception:
        h2 = False
        
    # ¬Q: The number of elements x in G satisfying x^m = e is not exactly gcd(m,n)
    try:
        n_val = G.order() if callable(G.order) else G.order
        n = int(n_val)
        m_int = int(m)
        expected = math.gcd(abs(m_int), n)
        
        try:
            elements = list(G.elements)
        except Exception:
            elements = list(G.generate())
            
        e = G.identity if hasattr(G, 'identity') else elements[0]**0
        
        count = 0
        for x in elements:
            if x**m_int == e:
                count += 1
                
        neg_q = (count != expected)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: m is an integer",
    "¬Q: The number of elements x in G satisfying x^m = e is not exactly gcd(m,n)"
]

N_HYP = 2
NEG_Q_INDEX = 2