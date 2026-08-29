import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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
    """
    Evaluates the hypotheses and negated conclusion for the false conjecture:
    Hypotheses:
      - f: G -> H is a group homomorphism
      - A and B are subgroups of G
      - ker(f) is a subset of A
    Conclusion:
      - f(A \cap B) = f(A) \cap f(B)
    """
    
    # H_1: f: G -> H is a group homomorphism
    try:
        G = witness['G']
        H = witness['H']
        f = witness['f']
        
        h1 = True
        G_elems = list(G.elements)
        H_elems = list(H.elements)
        
        for x in G_elems:
            fx = f(x) if callable(f) else f[x]
            if fx not in H_elems:
                h1 = False
                break
            for y in G_elems:
                fy = f(y) if callable(f) else f[y]
                fxy = f(x * y) if callable(f) else f[x * y]
                if fxy != fx * fy:
                    h1 = False
                    break
            if not h1:
                break
    except Exception:
        h1 = False

    # H_2: A and B are subgroups of G
    try:
        G = witness['G']
        A = witness['A']
        B = witness['B']
        
        def is_subgroup(sub_elems, grp):
            if not sub_elems:
                return False
            sub_set = set(sub_elems)
            if grp.identity not in sub_set:
                return False
            grp_elems = set(grp.elements)
            for x in sub_set:
                if x not in grp_elems:
                    return False
                if x**-1 not in sub_set:
                    return False
                for y in sub_set:
                    if x * y not in sub_set:
                        return False
            return True
            
        h2 = is_subgroup(A, G) and is_subgroup(B, G)
    except Exception:
        h2 = False

    # H_3: ker(f) is a subset of A
    try:
        G = witness['G']
        H = witness['H']
        f = witness['f']
        A = witness['A']
        
        h3 = True
        e_H = H.identity
        A_set = set(A)
        
        for x in G.elements:
            fx = f(x) if callable(f) else f[x]
            if fx == e_H and x not in A_set:
                h3 = False
                break
    except Exception:
        h3 = False

    # neg_Q: f(A \cap B) != f(A) \cap f(B)
    try:
        f = witness['f']
        A = witness['A']
        B = witness['B']
        
        A_set = set(A)
        B_set = set(B)
        A_cap_B = A_set.intersection(B_set)
        
        f_A_cap_B = set(f(x) if callable(f) else f[x] for x in A_cap_B)
        f_A = set(f(x) if callable(f) else f[x] for x in A_set)
        f_B = set(f(x) if callable(f) else f[x] for x in B_set)
        
        f_A_cap_f_B = f_A.intersection(f_B)
        
        neg_q = f_A_cap_B != f_A_cap_f_B
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a group homomorphism from G to H",
    "H_2: A and B are subgroups of G",
    "H_3: ker(f) is a subset of A",
    "¬Q: f(A ∩ B) != f(A) ∩ f(B)"
]

N_HYP = 3
NEG_Q_INDEX = 3