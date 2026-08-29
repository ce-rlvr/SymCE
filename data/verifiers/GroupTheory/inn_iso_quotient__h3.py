import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Z(G) is the center of G",
    "¬Q: Inn(G) is not isomorphic to the quotient group G/Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # H_1: G is a group
    # H_2: Z(G) is the center of G
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, Z = witness
        else:
            G = witness
            Z = G.center() if hasattr(G, 'center') else None
            
        h1 = isinstance(G, PermutationGroup)
        
        if h1 and Z is not None:
            if isinstance(Z, PermutationGroup):
                C = G.center()
                h2 = bool(Z.is_subgroup(C) and C.is_subgroup(Z))
            else:
                h2 = False
        else:
            h2 = False
            
    except Exception:
        h1 = False
        h2 = False

    # ¬Q: Inn(G) is not isomorphic to the quotient group G/Z(G)
    try:
        if not h1:
            neg_q = False
        else:
            E = list(G.generate())
            Z_group = G.center()
            Z_elems = list(Z_group.generate())
            
            cosets = []
            seen = set()
            for g in E:
                if g in seen:
                    continue
                coset = set()
                for z in Z_elems:
                    cz = g * z
                    coset.add(cz)
                    seen.add(cz)
                cosets.append(frozenset(coset))
                
            # Precompute deterministic representatives for each coset
            reps = {}
            for c in cosets:
                for x in E:
                    if x in c:
                        reps[c] = x
                        break
                        
            coset_to_inn = {}
            inns = set()
            for c in cosets:
                g = reps[c]
                # Inner automorphism mapping f_g(x) = g * x * g^-1
                mapping = tuple(E.index(g * x * ~g) for x in E)
                coset_to_inn[c] = mapping
                inns.add(mapping)
                
            if len(cosets) != len(inns):
                neg_q = True
            else:
                is_iso = True
                for c1 in cosets:
                    for c2 in cosets:
                        g1 = reps[c1]
                        g2 = reps[c2]
                        prod = g1 * g2
                        
                        c3 = None
                        for c in cosets:
                            if prod in c:
                                c3 = c
                                break
                        
                        m1 = coset_to_inn[c1]
                        m2 = coset_to_inn[c2]
                        m3 = coset_to_inn[c3]
                        
                        # Check composition of mappings
                        composed = tuple(m1[m2[i]] for i in range(len(E)))
                        composed_alt = tuple(m2[m1[i]] for i in range(len(E)))
                        
                        if composed != m3 and composed_alt != m3:
                            is_iso = False
                            break
                    if not is_iso:
                        break
                neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]