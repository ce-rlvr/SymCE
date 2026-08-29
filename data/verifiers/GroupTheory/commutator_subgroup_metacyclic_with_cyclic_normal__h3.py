import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import primefactors

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
V4 = A4.derived_subgroup()
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_order(group):
    return group.order() if callable(group.order) else group.order

def get_elements(group):
    elems = group.elements
    return list(elems() if callable(elems) else elems)

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False
        
    # H_3: The quotient group G/N is a cyclic group
    try:
        h3 = False
        if h1 and h2:
            order_G = get_order(G)
            order_N = get_order(N)
            order_quotient = order_G // order_N
            if order_quotient == 1:
                h3 = True
            else:
                pf = primefactors(order_quotient)
                for g in get_elements(G):
                    is_gen = True
                    for p in pf:
                        val = g**(order_quotient // p)
                        if hasattr(N, 'contains'):
                            in_N = N.contains(val)
                        else:
                            in_N = val in N
                        if in_N:
                            is_gen = False
                            break
                    if is_gen:
                        h3 = True
                        break
    except Exception:
        h3 = False
        
    # neg_Q: The commutator subgroup G' is not a cyclic group
    try:
        neg_q = False
        if h1:
            try:
                G_prime = G.derived_subgroup()
            except TypeError:
                G_prime = G.derived_subgroup
                
            order = get_order(G_prime)
            if order == 1:
                is_cyc = True
            else:
                pf = primefactors(order)
                is_cyc = False
                for h in get_elements(G_prime):
                    is_gen = True
                    for p in pf:
                        val = h**(order // p)
                        is_id = val.is_Identity() if callable(val.is_Identity) else val.is_Identity
                        if is_id:
                            is_gen = False
                            break
                    if is_gen:
                        is_cyc = True
                        break
            neg_q = not is_cyc
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: The quotient group G/N is a cyclic group",
    "¬Q: The commutator subgroup G' is not a cyclic group"
]

N_HYP = 3
NEG_Q_INDEX = 3