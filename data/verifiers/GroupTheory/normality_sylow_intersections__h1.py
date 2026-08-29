import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory as nt

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(obj):
    if hasattr(obj, 'elements'):
        return set(obj.elements)
    return set(obj)

def conditions(witness):
    try:
        G, p, N = witness
    except Exception:
        return [False, False, False]
    
    # H1: p is a prime number dividing the order of G
    try:
        h1 = False
        if nt.isprime(p) and G.order() % p == 0:
            h1 = True
    except Exception:
        h1 = False

    # H2: N is the intersection of all Sylow p-subgroups of G
    try:
        h2 = False
        if hasattr(G, 'sylow_subgroup'):
            P = G.sylow_subgroup(p)
            P_elements = set(P.elements)
            intersect_elems = set(P_elements)
            
            for g in G.elements:
                Pg_elems = {g * x * (~g) for x in P_elements}
                intersect_elems = intersect_elems.intersection(Pg_elems)
            
            N_elements = get_elements(N)
            if N_elements == intersect_elems:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: N is NOT a normal subgroup of G
    try:
        neg_q = False
        N_elements = get_elements(N)
        
        # Check if N is a subgroup
        is_subgroup = True
        if not N_elements:
            is_subgroup = False
        else:
            # check identity
            if hasattr(G, 'identity'):
                id_elem = G.identity
            else:
                id_elem = list(G.elements)[0]**0
                
            if id_elem not in N_elements:
                is_subgroup = False
            else:
                # check closure
                for a in N_elements:
                    for b in N_elements:
                        if a * b not in N_elements:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
        
        # If it's not a subgroup, it cannot be a normal subgroup (conclusion fails)
        if not is_subgroup:
            neg_q = True
        else:
            # Check normality condition
            is_normal = True
            for g in G.elements:
                for n in N_elements:
                    if g * n * (~g) not in N_elements:
                        is_normal = False
                        break
                if not is_normal:
                    break
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number dividing the order of G",
    "H_2: N is the intersection of all Sylow p-subgroups of G",
    "¬Q: N is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2