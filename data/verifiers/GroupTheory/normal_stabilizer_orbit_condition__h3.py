import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        # Parse the witness
        # Expected formats: (G, x) or (G, X, x)
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, x = witness
                if not isinstance(G, PermutationGroup):
                    return [False, False, False, False]
                X = set(range(G.degree))
            elif len(witness) == 3:
                G, X, x = witness
                if not isinstance(G, PermutationGroup):
                    return [False, False, False, False]
                try:
                    X = set(X)
                except Exception:
                    return [False, False, False, False]
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        # H_1: G is a group acting on a set X
        h1 = isinstance(G, PermutationGroup)
        
        # H_2: x is an element of X
        h2 = x in X
        
        # H_3: O_x is the orbit of x under the action of G
        elements = list(G.elements)
        orbit = set()
        for g in elements:
            orbit.add(g(x))
        h3 = True
        
        # Evaluate Conclusion: G_x is a normal subgroup of G iff G_x <= G_y for all y in O_x
        
        # Find the stabilizer G_x
        G_x = set()
        for g in elements:
            if g(x) == x:
                G_x.add(g)
                
        # Check if G_x is a normal subgroup of G
        is_normal = True
        for g in elements:
            for h in G_x:
                conj = g * h * (g**-1)
                if conj not in G_x:
                    is_normal = False
                    break
            if not is_normal:
                break
                
        # Check if G_x <= G_y for all y in O_x
        all_le = True
        for y in orbit:
            G_y = set()
            for g in elements:
                if g(y) == y:
                    G_y.add(g)
            if not G_x.issubset(G_y):
                all_le = False
                break
                
        # The conclusion is the biconditional (is_normal <==> all_le)
        # We want the negation of the conclusion
        neg_q = not (is_normal == all_le)
        
        return [h1, h2, h3, neg_q]
        
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: x is an element of X",
    "H_3: O_x is the orbit of x under the action of G",
    "¬Q: The equivalence (G_x is normal in G iff G_x <= G_y for all y in O_x) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3