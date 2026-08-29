import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import totient, reduced_totient

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: The characteristic of K does not divide n",
    "H_3: L is the splitting field of x^n - 1 over K",
    "¬Q: The Galois group Gal(L/K) is not isomorphic to a subgroup of (Z/nZ)^x"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    # H1: n is a positive integer
    try:
        if isinstance(witness, dict):
            n = witness['n']
        else:
            n = witness.n
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    # H2: The characteristic of K does not divide n
    try:
        char_K = None
        if isinstance(witness, dict) and 'char_K' in witness:
            char_K = witness['char_K']
        elif not isinstance(witness, dict) and hasattr(witness, 'char_K'):
            char_K = witness.char_K
        else:
            if isinstance(witness, dict):
                K = witness.get('K')
            else:
                K = getattr(witness, 'K', None)
            if K is not None and hasattr(K, 'characteristic'):
                char_K = K.characteristic()
                if callable(char_K):
                    char_K = char_K()
                
        if char_K is not None:
            h2 = (char_K == 0) or (n % char_K != 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: L is the splitting field of x^n - 1 over K
    try:
        if isinstance(witness, dict):
            h3 = bool(witness['is_splitting_field'])
        else:
            h3 = bool(witness.is_splitting_field)
    except Exception:
        h3 = False

    # neg_Q: The Galois group Gal(L/K) is NOT isomorphic to a subgroup of (Z/nZ)^x
    try:
        neg_q = False
        flag_found = False
        
        if isinstance(witness, dict) and 'galois_group_isomorphic_to_subgroup' in witness:
            neg_q = not bool(witness['galois_group_isomorphic_to_subgroup'])
            flag_found = True
        elif not isinstance(witness, dict) and hasattr(witness, 'galois_group_isomorphic_to_subgroup'):
            neg_q = not bool(witness.galois_group_isomorphic_to_subgroup)
            flag_found = True
            
        if not flag_found:
            if isinstance(witness, dict):
                G = witness.get('galois_group')
            else:
                G = getattr(witness, 'galois_group', None)
                
            if G is not None:
                if hasattr(G, 'is_abelian') and not G.is_abelian:
                    neg_q = True
                elif hasattr(G, 'order'):
                    order = G.order() if callable(G.order) else G.order
                    if totient(n) % order != 0:
                        neg_q = True
                    elif hasattr(G, 'elements'):
                        lam = reduced_totient(n)
                        for g in G.elements:
                            g_order = g.order() if callable(g.order) else g.order
                            if lam % g_order != 0:
                                neg_q = True
                                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]