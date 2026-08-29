import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
try:
    V4 = AbelianGroup(2, 2)
except Exception:
    V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: G and H are groups
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, H = witness
            h1 = hasattr(G, 'derived_subgroup') and hasattr(H, 'derived_subgroup')
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: G/G' is not isomorphic to H/H'
    try:
        if not h1:
            neg_q = False
        else:
            G, H = witness
            
            def is_abelianization_isomorphic(G, H):
                # Fast path: use SymPy's built-in abelian_invariants if available
                try:
                    inv_G = G.abelian_invariants() if callable(G.abelian_invariants) else G.abelian_invariants
                    inv_H = H.abelian_invariants() if callable(H.abelian_invariants) else H.abelian_invariants
                    return sorted(inv_G) == sorted(inv_H)
                except Exception:
                    pass
                
                # Fallback: compute the multiset of element orders in the quotient group G/G'
                # For finite abelian groups, the multiset of element orders uniquely determines the isomorphism class.
                def get_q_orders(Grp):
                    D = Grp.derived_subgroup()
                    D_elements = set(list(D.elements))
                    
                    reps = []
                    seen = set()
                    for g in list(Grp.elements):
                        if g not in seen:
                            reps.append(g)
                            coset = set(g * d for d in D_elements)
                            seen.update(coset)
                            
                    orders = []
                    for rep in reps:
                        k = 1
                        curr = rep
                        while curr not in D_elements:
                            k += 1
                            curr = curr * rep
                        orders.append(k)
                    return sorted(orders)
                
                return get_q_orders(G) == get_q_orders(H)
            
            neg_q = not is_abelianization_isomorphic(G, H)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "¬Q: G/G' is not isomorphic to H/H'"
]

N_HYP = 1
NEG_Q_INDEX = 1