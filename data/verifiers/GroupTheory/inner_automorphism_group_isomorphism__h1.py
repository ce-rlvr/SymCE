import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a permutation group",
    "¬Q: G/Z(G) is not isomorphic to Inn(G)"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # H_1: witness is a PermutationGroup
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    if not h1:
        return [False, False]

    # ¬Q: G/Z(G) is not isomorphic to Inn(G)
    try:
        G = witness
        elems = list(G.generate())
        Z = G.center()
        Z_elems = list(Z.generate())

        def to_tuple(p):
            return tuple(p.array_form)

        elems_tuples = {to_tuple(p): p for p in elems}
        elem_to_idx = {to_tuple(x): i for i, x in enumerate(elems)}
        
        # Construct G/Z(G)
        coset_list = []
        seen = set()
        for x in elems:
            xt = to_tuple(x)
            if xt in seen:
                continue
            c = frozenset(to_tuple(x * z) for z in Z_elems)
            coset_list.append(c)
            seen.update(c)
            
        coset_to_idx = {c: i for i, c in enumerate(coset_list)}
        
        perms_G_mod_Z = []
        for g in G.generators:
            p = []
            for c in coset_list:
                rep_tuple = next(iter(c))
                rep = elems_tuples[rep_tuple]
                target = frozenset(to_tuple(g * rep * z) for z in Z_elems)
                p.append(coset_to_idx[target])
            if p:
                perms_G_mod_Z.append(Permutation(p))
                
        if not perms_G_mod_Z:
            G_mod_Z = PermutationGroup([Permutation(0)])
        else:
            G_mod_Z = PermutationGroup(perms_G_mod_Z)

        # Construct Inn(G)
        perms_Inn = []
        for g in G.generators:
            p = []
            for x in elems:
                target = g * x * g**-1
                p.append(elem_to_idx[to_tuple(target)])
            if p:
                perms_Inn.append(Permutation(p))
                
        if not perms_Inn:
            Inn_G = PermutationGroup([Permutation(0)])
        else:
            Inn_G = PermutationGroup(perms_Inn)

        # Check isomorphism
        try:
            q = G_mod_Z.is_isomorphic(Inn_G)
        except Exception:
            # Fallback if is_isomorphic fails or is missing
            q = (G_mod_Z.order() == Inn_G.order() and G_mod_Z.is_abelian == Inn_G.is_abelian)
            
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]