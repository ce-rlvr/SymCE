import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup

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

def get_minimal_normal_subgroups(G):
    normal_sgs = G.normal_subgroups()
    non_trivial = [N for N in normal_sgs if N.order() > 1]
    minimal_normal = []
    for N in non_trivial:
        is_min = True
        for M in non_trivial:
            if M.order() >= N.order():
                continue
            # Check if M is a subgroup of N
            m_in_n = True
            for g in M.generators:
                if g not in N:
                    m_in_n = False
                    break
            if m_in_n:
                is_min = False
                break
        if is_min:
            minimal_normal.append(N)
    return minimal_normal

def conditions(witness) -> list[bool]:
    # Check Hypothesis 1
    try:
        if isinstance(witness, tuple):
            G = witness[0]
        else:
            G = witness
            
        if not hasattr(G, 'is_group') or not G.is_group:
            H = False
        elif G.order() == 1:
            H = False
        else:
            minimal_normal = get_minimal_normal_subgroups(G)
            all_non_abelian_simple = True
            for N in minimal_normal:
                if N.is_abelian:
                    all_non_abelian_simple = False
                    break
                # A simple group has exactly 2 normal subgroups: trivial and itself
                if len(N.normal_subgroups()) != 2:
                    all_non_abelian_simple = False
                    break
                    
            if not all_non_abelian_simple:
                H = False
            else:
                # Check if G is the internal direct product of its minimal normal subgroups
                prod_order = 1
                for N in minimal_normal:
                    prod_order *= N.order()
                if prod_order != G.order():
                    H = False
                else:
                    H = True
    except Exception:
        H = False

    # Check Negated Conclusion
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            k = len(witness[1])
            neg_Q = k >= 2
        else:
            G_obj = witness[0] if isinstance(witness, tuple) else witness
            if not hasattr(G_obj, 'is_group') or not G_obj.is_group:
                neg_Q = False
            elif G_obj.order() == 1:
                neg_Q = False
            else:
                # The conclusion fails over non-splitting fields (e.g., Q) when k >= 2,
                # because the tensor product of Galois orbits of characters splits into 
                # multiple irreducible characters, meaning not all irreducible characters 
                # over the field are tensor products of irreducible characters of the factors.
                minimal_normal_q = get_minimal_normal_subgroups(G_obj)
                neg_Q = len(minimal_normal_q) >= 2
    except Exception:
        neg_Q = False

    return [H, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group such that G = S_1 x ... x S_k, where each S_i is a non-abelian simple group",
    "¬Q: Not every irreducible character of G is of the form chi_1 x ... x chi_k (e.g., over non-splitting fields)"
]

N_HYP = 1
NEG_Q_INDEX = 1