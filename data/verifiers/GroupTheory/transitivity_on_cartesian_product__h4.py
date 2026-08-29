import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            G, X, Y, x_witness = witness
            x_list = [x_witness]
        elif len(witness) == 3:
            G, X, Y = witness
            x_list = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    try:
        X_list = list(X)
    except Exception:
        X_list = []
        
    try:
        Y_list = list(Y)
    except Exception:
        Y_list = []
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: G acts transitively on X
    try:
        if not X_list:
            h2 = False
        else:
            orbit_X = set(G.orbit(X_list[0]))
            h2 = (orbit_X == set(X_list))
    except Exception:
        h2 = False
        
    # H3: G acts transitively on Y
    try:
        if not Y_list:
            h3 = False
        else:
            orbit_Y = set(G.orbit(Y_list[0]))
            h3 = (orbit_Y == set(Y_list))
    except Exception:
        h3 = False
        
    # neg_Q: The diagonal action of G on X \times Y is transitive iff G_x acts transitively on Y
    try:
        if x_list is None:
            x_list = list(range(G.degree))
            
        if not X_list or not Y_list:
            neg_q = False
        else:
            # LHS: G acts transitively on X \times Y
            start_pair = (X_list[0], Y_list[0])
            orbit_XY = {start_pair}
            queue = [start_pair]
            gens = G.generators
            for pair in queue:
                for g in gens:
                    next_pair = (g(pair[0]), g(pair[1]))
                    if next_pair not in orbit_XY:
                        orbit_XY.add(next_pair)
                        queue.append(next_pair)
            lhs = (len(orbit_XY) == len(X_list) * len(Y_list))
            
            # RHS: G_x acts transitively on Y
            neg_q = False
            for x in x_list:
                try:
                    G_x = G.stabilizer(x)
                    orbit_Y_Gx = set(G_x.orbit(Y_list[0]))
                    rhs = (orbit_Y_Gx == set(Y_list))
                    if lhs != rhs:
                        neg_q = True
                        break
                except Exception:
                    continue
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts transitively on X",
    "H_3: G acts transitively on Y",
    "¬Q: The equivalence between transitivity of G on X x Y and G_x on Y fails"
]

N_HYP = 3
NEG_Q_INDEX = 3