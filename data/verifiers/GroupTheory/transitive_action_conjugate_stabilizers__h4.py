import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            x = witness.get('x')
            y = witness.get('y')
        elif isinstance(witness, (list, tuple)) and len(witness) == 4:
            G, X, x, y = witness
        else:
            return [False, False, False, False, False]
    except Exception:
        return [False, False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = isinstance(X, (set, list, tuple))
    except Exception:
        h2 = False

    # H3: G acts transitively on X
    try:
        if h1 and h2 and len(X) > 0:
            X_set = set(X)
            elem = next(iter(X_set))
            if isinstance(elem, int) and 0 <= elem < G.degree:
                orbit = set(G.orbit(elem))
            else:
                orbit = {elem}
            h3 = (orbit == X_set)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: y is an element of X
    try:
        h4 = y in X
    except Exception:
        h4 = False

    # neg_Q: not (exists g in G, Stab_G(y) == g * Stab_G(x) * g^{-1})
    try:
        if not h1:
            neg_q = False
        else:
            def get_stabilizer(Grp, p):
                if not isinstance(p, int) or p < 0 or p >= Grp.degree:
                    return Grp
                return Grp.stabilizer(p)
            
            Stab_y = get_stabilizer(G, y)
            Stab_x = get_stabilizer(G, x)
            Stab_y_elems = set(Stab_y.generate())
            
            exists_g = False
            for g in G.generate():
                # In SymPy, permutations are applied left-to-right.
                # So g * h * g^-1 acting on a point is written as g**-1 * h * g
                conj_gens = [g**-1 * h * g for h in Stab_x.generators]
                try:
                    if not conj_gens:
                        conj_elems = {g * g**-1}
                    else:
                        conj_group = PermutationGroup(conj_gens)
                        conj_elems = set(conj_group.generate())
                except Exception:
                    conj_elems = {g * g**-1}
                
                if conj_elems == Stab_y_elems:
                    exists_g = True
                    break
            
            neg_q = not exists_g
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: G acts transitively on X",
    "H_4: y is an element of X",
    "¬Q: There does not exist g in G such that Stab_G(y) = g * Stab_G(x) * g^{-1}"
]

N_HYP = 4
NEG_Q_INDEX = 4