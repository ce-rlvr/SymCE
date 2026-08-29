import sympy
import sympy.combinatorics.named_groups
import sympy.matrices

# Top-level setup for standard algebra objects
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: n >= 2 is an integer",
    "H_2: G is defined by the presentation with generators s_1..s_{n-1}",
    "H_3: s_i^2 = 1 for all 1 <= i <= n-1",
    "H_4: (s_i s_j)^2 = 1 for all |i - j| >= 2",
    "¬Q: G is not isomorphic to S_n"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    try:
        n = None
        if type(witness) is int:
            n = witness
        elif isinstance(witness, tuple) and len(witness) >= 1 and type(witness[0]) is int:
            n = witness[0]
            
        if n is None:
            return [False, False, False, False, False]
            
        # H_1: n >= 2 is an integer
        h1 = (n >= 2)
        
        # Since G is uniquely determined by the presentation given in the hypotheses,
        # any valid integer n >= 2 uniquely defines G satisfying H_2, H_3, and H_4.
        h2 = h1
        h3 = h1
        h4 = h1
        
        # ¬Q: G is not isomorphic to S_n
        # For n = 2, G is Z_2, which is isomorphic to S_2.
        # For n >= 3, G is infinite (e.g., for n=3, G is the infinite dihedral group),
        # whereas S_n is finite. Thus G is not isomorphic to S_n.
        neg_q = h1 and (n >= 3)
        
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]