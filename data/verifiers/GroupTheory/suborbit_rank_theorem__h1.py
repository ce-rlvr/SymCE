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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: The action of G on X is transitive.",
    "H_2: Let G act on X \\times X diagonally via g * (y, z) = (g * y, g * z).",
    "H_3: Let x be a fixed element of X, and let G_x be its stabilizer in G.",
    "¬Q: The number of orbits of G on X \\times X is not equal to the number of orbits of G_x on X."
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    def get_val(attr):
        return attr() if callable(attr) else attr

    try:
        if isinstance(witness, tuple):
            G = witness[0]
            x = 0
            for item in witness[1:]:
                if isinstance(item, int):
                    x = item
                    break
        else:
            G = witness
            x = 0
            
        if not isinstance(G, PermutationGroup):
            return [False, False, False, False]
            
        degree = get_val(G.degree)
        if degree == 0:
            return [False, False, False, False]
            
        X = list(range(degree))
    except Exception:
        return [False, False, False, False]

    # H1: The action of G on X is transitive.
    try:
        h1 = get_val(G.is_transitive)
    except Exception:
        h1 = False

    # H2: Let G act on X \times X diagonally via g * (y, z) = (g * y, g * z).
    try:
        h2 = True
    except Exception:
        h2 = False

    # H3: Let x be a fixed element of X, and let G_x be its stabilizer in G.
    try:
        if x in X:
            Gx = G.stabilizer(x)
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The number of orbits of G on X \times X is NOT equal to the number of orbits of G_x on X.
    try:
        # Compute orbits of G on X \times X using BFS
        visited_XxX = set()
        orbits_G_XxX = 0
        gens_G = get_val(G.generators)
        for y in range(degree):
            for z in range(degree):
                if (y, z) not in visited_XxX:
                    orbits_G_XxX += 1
                    queue = [(y, z)]
                    visited_XxX.add((y, z))
                    head = 0
                    while head < len(queue):
                        curr_y, curr_z = queue[head]
                        head += 1
                        for g in gens_G:
                            next_y = g(curr_y)
                            next_z = g(curr_z)
                            if (next_y, next_z) not in visited_XxX:
                                visited_XxX.add((next_y, next_z))
                                queue.append((next_y, next_z))
                                
        # Compute orbits of G_x on X using BFS
        visited_X = set()
        orbits_Gx_X = 0
        gens_Gx = get_val(Gx.generators)
        for y in range(degree):
            if y not in visited_X:
                orbits_Gx_X += 1
                queue = [y]
                visited_X.add(y)
                head = 0
                while head < len(queue):
                    curr_y = queue[head]
                    head += 1
                    for g in gens_Gx:
                        next_y = g(curr_y)
                        if next_y not in visited_X:
                            visited_X.add(next_y)
                            queue.append(next_y)
                            
        neg_Q = (orbits_G_XxX != orbits_Gx_X)
    except Exception:
        neg_Q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_Q)]