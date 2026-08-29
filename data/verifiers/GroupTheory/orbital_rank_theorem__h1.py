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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, x) where G is a PermutationGroup and x is an integer point.
    """
    try:
        G, x = witness
    except Exception:
        return [False, False, False, False]

    # H_1: x is an element of X
    try:
        # In SymPy, a PermutationGroup's domain X is {0, 1, ..., G.degree - 1}
        h1 = isinstance(G, PermutationGroup) and isinstance(x, int) and 0 <= x < G.degree
        # Limit group size to ensure fast execution
        if h1 and G.order() > 10000:
            h1 = False
    except Exception:
        h1 = False

    # H_2: G_x is the stabilizer of x in G
    # This is definitional and holds by construction of G_x in the evaluation.
    h2 = h1

    # H_3: G acts on the Cartesian product X x X via the diagonal action
    # This is also definitional and holds by construction of the action in the evaluation.
    h3 = h1

    # neg_Q: The number of orbits of G_x on X is NOT equal to the number of orbits of G on X x X
    try:
        if not h1:
            neg_q = False
        else:
            # Compute G_x, the stabilizer of x in G
            Gx = G.stabilizer(x)
            
            # Number of orbits of G_x on X using Burnside's Lemma
            # The number of orbits is the average number of fixed points.
            total_fixed_Gx = 0
            for g in Gx.generate():
                f = sum(1 for i in range(G.degree) if g(i) == i)
                total_fixed_Gx += f
            num_orbits_Gx = total_fixed_Gx // int(Gx.order())
            
            # Number of orbits of G on X x X using Burnside's Lemma
            # The number of fixed points of g on X x X is f^2, where f is the number of fixed points on X.
            total_fixed_G_XxX = 0
            for g in G.generate():
                f = sum(1 for i in range(G.degree) if g(i) == i)
                total_fixed_G_XxX += f**2
            num_orbits_G_XxX = total_fixed_G_XxX // int(G.order())
            
            neg_q = bool(num_orbits_Gx != num_orbits_G_XxX)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of X",
    "H_2: G_x is the stabilizer of x in G",
    "H_3: G acts on the Cartesian product X x X via the diagonal action",
    "¬Q: The number of orbits of G_x on X is not equal to the number of orbits of G on X x X"
]

N_HYP = 3
NEG_Q_INDEX = 3