import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup
from sympy.combinatorics.named_groups import AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    # witness could be G or a tuple (G, C)
    if isinstance(witness, tuple) and len(witness) == 2:
        G, C = witness
        witness_has_C = True
    else:
        G = witness
        witness_has_C = False

    # H1: G is a subgroup of the symmetric group Sym(X)
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: G acts transitively on X
    try:
        if h1:
            h2 = G.is_transitive()
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: C is the centralizer of G in Sym(X)
    try:
        if not h1:
            h3 = False
        else:
            degree = G.degree
            gens = G.generators
            
            # Compute the actual centralizer of G in Sym(degree)
            if degree <= 6:
                S = SymmetricGroup(degree)
                C_elements = []
                for p in S.generate():
                    if all(p * g == g * p for g in gens):
                        C_elements.append(p)
                C_actual = PermutationGroup(C_elements) if C_elements else PermutationGroup([Permutation(degree-1)])
            else:
                # Fast method for larger degrees (assumes G is transitive)
                g_to_x = {0: Permutation(degree-1)}
                queue = [0]
                while queue:
                    curr = queue.pop(0)
                    curr_g = g_to_x[curr]
                    for gen in gens:
                        nxt = gen(curr)
                        if nxt not in g_to_x:
                            g_to_x[nxt] = curr_g * gen
                            queue.append(nxt)
                
                if len(g_to_x) < degree:
                    # Fallback if not transitive
                    C_actual = PermutationGroup([Permutation(degree-1)])
                else:
                    C_elements = []
                    for y in range(degree):
                        c_array = [g_to_x[x](y) for x in range(degree)]
                        if len(set(c_array)) == degree:
                            c = Permutation(c_array)
                            if all(c * gen == gen * c for gen in gens):
                                C_elements.append(c)
                    C_actual = PermutationGroup(C_elements) if C_elements else PermutationGroup([Permutation(degree-1)])
            
            if witness_has_C:
                if isinstance(C, PermutationGroup):
                    if C.order() == C_actual.order():
                        h3 = set(C.generate()) == set(C_actual.generate())
                    else:
                        h3 = False
                else:
                    h3 = False
            else:
                C = C_actual
                h3 = True
    except Exception:
        h3 = False

    # neg_Q: C does NOT act semi-regularly on X
    # Semi-regular means no non-identity element fixes any point.
    # Negation: there exists a non-identity element in C that fixes at least one point.
    try:
        if not h1 or not h3:
            neg_q = False
        else:
            neg_q = False
            degree = G.degree
            for c in C.generate():
                supp_len = len(c.support())
                # If supp_len == 0, c is the identity.
                # If supp_len < degree, c fixes at least one point in {0, ..., degree-1}.
                if supp_len > 0 and supp_len < degree:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a subgroup of the symmetric group Sym(X)",
    "H_2: G acts transitively on X",
    "H_3: C is the centralizer of G in Sym(X)",
    "¬Q: C does not act semi-regularly on X"
]

N_HYP = 3
NEG_Q_INDEX = 3