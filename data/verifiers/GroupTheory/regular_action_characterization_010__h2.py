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
    try:
        # Parse witness
        if isinstance(witness, PermutationGroup):
            G_elements = list(witness.generate())
            id_g = witness.identity
            X = list(range(witness.degree))
            action = lambda g, x: g(x)
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                G, X, action = witness
            elif len(witness) == 2:
                G, X = witness
                action = lambda g, x: g(x)
            else:
                return [False, False, False]
                
            if hasattr(G, 'generate'):
                G_elements = list(G.generate())
                id_g = G.identity
            elif hasattr(G, 'elements'):
                G_elements = list(G.elements)
                id_g = G.identity if hasattr(G, 'identity') else G_elements[0]
            else:
                G_elements = list(G)
                id_g = G_elements[0]
        else:
            return [False, False, False]

        # H_1: G is a group
        h1 = len(G_elements) > 0

        # H_2: G acts on X
        h2 = True
        for g in G_elements:
            for x in X:
                if action(g, x) not in X:
                    h2 = False
                    break
            if not h2:
                break

        # Transitive: for all x, y in X, exists g in G, action(g, x) == y
        is_transitive = True
        for x in X:
            for y in X:
                if not any(action(g, x) == y for g in G_elements):
                    is_transitive = False
                    break
            if not is_transitive:
                break

        # Stabilizers trivial: for all x in X, for all g in G, action(g, x) == x implies g == id_g
        stabilizers_trivial = True
        for x in X:
            for g in G_elements:
                if action(g, x) == x and g != id_g:
                    stabilizers_trivial = False
                    break
            if not stabilizers_trivial:
                break

        # Regular action: isomorphic to left regular action.
        # This implies |X| == |G| and transitive and free.
        is_regular = (len(X) == len(G_elements)) and is_transitive and stabilizers_trivial

        # Conclusion: is_regular iff (is_transitive and stabilizers_trivial)
        Q = (is_regular == (is_transitive and stabilizers_trivial))
        neg_Q = not Q

        return [bool(h1), bool(h2), bool(neg_Q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on X",
    "¬Q: The action is transitive and stabilizers are trivial, but it is not regular"
]

N_HYP = 2
NEG_Q_INDEX = 2