import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness) -> list[bool]:
    # H1: \Gamma = (V, E) is an undirected graph
    try:
        V = witness['V']
        E = witness['E']
        h1 = True
        for edge in E:
            if not isinstance(edge, (set, frozenset)):
                if not set(edge).issubset(set(V)):
                    h1 = False
                    break
            else:
                if not edge.issubset(set(V)):
                    h1 = False
                    break
            if len(edge) not in [1, 2]:
                h1 = False
                break
    except Exception:
        h1 = False

    # H2: e = {u, v} is an edge in E
    try:
        e = witness['e']
        u = witness['u']
        v = witness['v']
        E = witness['E']
        h2 = (set(e) == {u, v}) and (e in E)
    except Exception:
        h2 = False

    # neg_Q: G_e does not contain G_u \cap G_v as a normal subgroup of index at most 2
    try:
        G = witness['G']
        e_i = witness['e_index']
        u_i = witness['u_index']
        v_i = witness['v_index']
        
        # Compute stabilizers using the permutation group action
        G_e = G.stabilizer(e_i)
        G_u = G.stabilizer(u_i)
        G_uv = G_u.stabilizer(v_i)
        
        # Check if G_uv is a subgroup of G_e
        is_subgroup = all(g in G_e for g in G_uv.generators)
        
        if not is_subgroup:
            neg_q = True
        else:
            # Check if G_uv is a normal subgroup of G_e
            is_normal = True
            for h in G_e.generators:
                h_inv = h**-1
                for g in G_uv.generators:
                    conj = h * g * h_inv
                    if conj not in G_uv:
                        is_normal = False
                        break
                if not is_normal:
                    break
            
            if not is_normal:
                neg_q = True
            else:
                # Check if the index is at most 2
                if G_e.order() > 2 * G_uv.order():
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS: list[str] = [
    "H_1: Gamma = (V, E) is an undirected graph",
    "H_2: e = {u, v} is an edge in E",
    "¬Q: G_e does not contain G_u \\cap G_v as a normal subgroup of index at most 2"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2