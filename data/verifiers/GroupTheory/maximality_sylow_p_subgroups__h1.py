import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (G, P, p)
    where G is a group, P is a subgroup, and p is an integer.
    """
    try:
        if isinstance(witness, tuple) and len(witness) >= 3:
            G = witness[0]
            P = witness[1]
            p = witness[-1]
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: P is a Sylow p-subgroup of G
    # A Sylow p-subgroup is a subgroup of order p^k where p^k is the highest power of p dividing |G|.
    try:
        if not isinstance(p, int) or p <= 1:
            h1_ok = False
        elif not hasattr(P, 'is_subgroup') or not P.is_subgroup(G):
            h1_ok = False
        else:
            k = 0
            n = G.order()
            while n % (p**(k+1)) == 0:
                k += 1
            h1_ok = bool(P.order() == p**k)
    except Exception:
        h1_ok = False
        
    # neg_Q: P is NOT a maximal p-subgroup of G
    # A p-subgroup is a group where the order of every element is a power of p.
    # If P is not a p-subgroup, it cannot be a maximal p-subgroup.
    # (This occurs when the dropped hypothesis "p is prime" is violated).
    try:
        def is_p_subgroup(H, p_val):
            if p_val <= 1: 
                return False
            for g in H.elements:
                o = g.order()
                if o == 1: 
                    continue
                temp = o
                while temp % p_val == 0:
                    temp //= p_val
                if temp != 1: 
                    return False
            return True
            
        if not is_p_subgroup(P, p):
            neg_q_ok = True
        else:
            # If P is a valid p-subgroup and its order is p^k || |G|, 
            # Lagrange's theorem guarantees no strictly larger p-subgroup can exist.
            neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P is a Sylow p-subgroup of G",
    "¬Q: P is not a maximal p-subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1