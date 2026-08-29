import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
import sympy.ntheory

# Top-level setup: named object bindings
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

def _check_Gp(G, p):
    try:
        h1 = bool(sympy.ntheory.isprime(p) and G.order() % p == 0)
    except Exception:
        h1 = False
        
    try:
        H = G.sylow_subgroup(p)
        
        # Check uniqueness (equivalent to being a normal subgroup)
        unique = True
        for g in G.generators:
            for h in H.generators:
                if (g * h * ~g) not in H:
                    unique = False
                    break
            if not unique:
                break
                
        # Check if the subgroup is cyclic
        cyclic = False
        h_order = H.order()
        if h_order == 1:
            cyclic = True
        else:
            for x in H.generate():
                if x.order() == h_order:
                    cyclic = True
                    break
                    
        neg_q = not (unique and cyclic)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

def conditions(witness):
    G, p = None, None
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, p = witness
        elif hasattr(witness, 'G') and hasattr(witness, 'p'):
            G = witness.G
            p = witness.p
    except Exception:
        pass

    # If witness explicitly provides both G and p
    if G is not None and p is not None:
        return _check_Gp(G, p)
        
    # If witness is just G, try to find a prime p that makes it a counterexample
    try:
        G = witness
        order = G.order()
        factors = sympy.ntheory.primefactors(order)
    except Exception:
        return [False, False]
        
    for p_cand in factors:
        res = _check_Gp(G, p_cand)
        if res == [True, True]:
            return res
            
    # Fallback if no counterexample p is found, return evaluation for the first prime factor
    if factors:
        return _check_Gp(G, factors[0])
        
    return [False, False]

CONDITION_LABELS = [
    "H_1: p is a prime number that divides the order of G",
    "¬Q: The Sylow p-subgroup of G is not unique or not cyclic"
]

N_HYP = 1
NEG_Q_INDEX = 1