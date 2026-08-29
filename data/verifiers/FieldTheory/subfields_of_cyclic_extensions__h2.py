import itertools
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, d = witness
    except Exception:
        return [False, False, False]
        
    # H1: E is a finite Galois extension of F
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: d is a positive integer that divides the degree of E over F
    try:
        if not (isinstance(d, int) or (hasattr(d, 'is_integer') and d.is_integer)):
            h2 = False
        else:
            d_val = int(d)
            try:
                g_order = int(G.order())
            except TypeError:
                g_order = int(G.order)
                
            h2 = d_val > 0 and g_order % d_val == 0
    except Exception:
        h2 = False
        
    # neg_Q: There does NOT exist exactly one intermediate field K such that the degree of K over F is d
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            d_val = int(d)
            target_order = g_order // d_val
            
            try:
                elements = list(G.elements)
            except Exception:
                elements = list(G.generate())
                
            if not elements or target_order > len(elements):
                neg_q = False
            else:
                id_elem = elements[0]**0
                remaining = [e for e in elements if e != id_elem]
                
                count = 0
                for sub in itertools.combinations(remaining, target_order - 1):
                    closed = True
                    for a in sub:
                        a2 = a**2
                        if a2 != id_elem and a2 not in sub:
                            closed = False
                            break
                        for b in sub:
                            if a == b:
                                continue
                            ab = a * b
                            if ab != id_elem and ab not in sub:
                                closed = False
                                break
                        if not closed:
                            break
                    if closed:
                        count += 1
                
                neg_q = (count != 1)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: E is a finite Galois extension of F",
    "H_2: d is a positive integer that divides the degree of E over F",
    "¬Q: There does NOT exist exactly one intermediate field K such that the degree of K over F is d"
]

N_HYP = 2
NEG_Q_INDEX = 2