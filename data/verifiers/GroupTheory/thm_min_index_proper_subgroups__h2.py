import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def get_elements(grp):
    if hasattr(grp, 'elements'):
        return list(grp.elements)
    elif hasattr(grp, 'generate_dimino'):
        return list(grp.generate_dimino())
    else:
        raise ValueError("Cannot get elements")

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a semisimple finite group
    # A finite group is semisimple if it has no non-trivial abelian normal subgroups.
    # Equivalently, no non-trivial element has an abelian normal closure.
    try:
        G_elements = get_elements(G)
        id_el = getattr(G, 'identity', None)
        if id_el is None:
            for e in G_elements:
                if e * e == e:
                    id_el = e
                    break
        
        is_semi = True
        if len(G_elements) <= 1:
            is_semi = True
        else:
            for g in G_elements:
                if g == id_el:
                    continue
                
                conjugates = []
                for x in G_elements:
                    try:
                        inv_x = ~x
                    except Exception:
                        inv_x = x**-1
                    
                    c = x * g * inv_x
                    
                    if c not in conjugates:
                        conjugates.append(c)
                
                is_abelian = True
                for i in range(len(conjugates)):
                    for j in range(i, len(conjugates)):
                        if conjugates[i] * conjugates[j] != conjugates[j] * conjugates[i]:
                            is_abelian = False
                            break
                    if not is_abelian:
                        break
                
                if is_abelian:
                    is_semi = False
                    break
        h1 = is_semi
    except Exception:
        h1 = False

    # H_2: H is a proper subgroup of G
    try:
        G_elements = get_elements(G)
        H_elements = get_elements(H)
        
        is_subgroup = True
        for h in H_elements:
            if h not in G_elements:
                is_subgroup = False
                break
                
        is_proper = len(H_elements) < len(G_elements)
        h2 = is_subgroup and is_proper
    except Exception:
        h2 = False

    # ¬Q: The index of H in G is less than 5
    try:
        if h2:
            index = len(G_elements) // len(H_elements)
            neg_q = index < 5
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "H_2: H is a proper subgroup of G",
    "¬Q: The index of H in G is less than 5"
]

N_HYP = 2
NEG_Q_INDEX = 2