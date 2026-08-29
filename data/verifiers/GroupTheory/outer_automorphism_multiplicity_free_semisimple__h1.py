import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def check_simple(f):
    s = f.is_simple
    if callable(s):
        return s()
    return s

def check_abelian(f):
    a = f.is_abelian
    if callable(a):
        return a()
    return a

def get_factors(witness):
    # If the witness is provided as a tuple (G, [S1, ..., Sk])
    if isinstance(witness, tuple) and len(witness) == 2:
        return witness[0], witness[1]
    
    G = witness
    try:
        orbits = G.orbits()
    except Exception:
        return G, None

    factors = []
    for orb in orbits:
        if len(orb) > 1:
            gens = []
            orb_list = sorted(list(orb))
            val_map = {val: i for i, val in enumerate(orb_list)}
            for g in G.generators:
                mapping = {p: g(p) for p in orb}
                if any(mapping[p] != p for p in orb):
                    p_list = [val_map[mapping[orb_list[i]]] for i in range(len(orb_list))]
                    gens.append(Permutation(p_list))
            if gens:
                factors.append(PermutationGroup(gens))
    
    order_prod = 1
    for f in factors:
        order_prod *= f.order()
        
    if order_prod == G.order():
        return G, factors
        
    if check_simple(G):
        return G, [G]
        
    return G, None

def are_pairwise_non_isomorphic(factors):
    n = len(factors)
    for i in range(n):
        for j in range(i + 1, n):
            if factors[i].is_isomorphic(factors[j]):
                return False
    return True

def conditions(witness):
    try:
        G, factors = get_factors(witness)
        if factors is None:
            return [False, False]
            
        all_non_abelian_simple = True
        for f in factors:
            if not (check_simple(f) and not check_abelian(f)):
                all_non_abelian_simple = False
                break
                
        pairwise_non_iso = are_pairwise_non_isomorphic(factors)
        
        H1_ok = bool(all_non_abelian_simple and pairwise_non_iso)
        
        # For a direct product of simple groups, Out(G) is isomorphic to \prod Out(S_i)
        # if and only if the simple factors are pairwise non-isomorphic.
        # Thus, the conclusion fails (neg_Q is True) iff they are NOT pairwise non-isomorphic.
        if all_non_abelian_simple:
            neg_Q_ok = not pairwise_non_iso
        else:
            neg_Q_ok = False
            
        return [H1_ok, neg_Q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: G is a direct product of pairwise non-isomorphic non-abelian simple groups",
    "¬Q: Out(G) is not isomorphic to the direct product of Out(S_i)"
]

N_HYP = 1
NEG_Q_INDEX = 1