import sympy
from sympy.combinatorics.free_groups import FreeGroup, FreeGroupElement, free_group
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = [
    "H_1: G is a group defined by the presentation <X | R>",
    "H_2: H is a group",
    "H_3: Substitution of f(x) for each x in X in every relation w=1 yields the identity in H",
    "¬Q: There does not exist a unique homomorphism phi: G -> H such that phi(x) = f(x) for all x in X"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        F, R, H, f = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        if isinstance(f, dict):
            f_dict = {str(k): v for k, v in f.items()}
        elif callable(f):
            f_dict = {}
            for x in F.generators:
                try:
                    f_dict[str(x)] = f(x)
                except Exception:
                    pass
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a group defined by the presentation <X | R>.
    try:
        h1 = isinstance(F, FreeGroup) and isinstance(R, (list, tuple))
        if h1:
            for r in R:
                if not isinstance(r, FreeGroupElement) or r.group != F:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: H is a group.
    try:
        h2 = hasattr(H, 'identity') and hasattr(H, '__contains__')
    except Exception:
        h2 = False

    # H3: For every relation w=1 in R, the substitution of f(x) for each x in X in the word w yields the identity element in H.
    try:
        h3 = True
        for w in R:
            val = H.identity
            for gen, exp in w.array_form:
                gen_str = str(gen)
                if gen_str not in f_dict:
                    h3 = False
                    break
                p = f_dict[gen_str]
                if exp != 0:
                    val = val * (p ** exp)
            if not h3:
                break
            if val != H.identity:
                h3 = False
                break
    except Exception:
        h3 = False

    # Conclusion: There exists a unique group homomorphism phi: G -> H such that phi(x) = f(x) for all x in X.
    try:
        conclusion_holds = True
        for x in F.generators:
            x_str = str(x)
            if x_str not in f_dict:
                conclusion_holds = False
                break
            try:
                in_H = f_dict[x_str] in H
            except Exception:
                in_H = False
            if not in_H:
                conclusion_holds = False
                break
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]