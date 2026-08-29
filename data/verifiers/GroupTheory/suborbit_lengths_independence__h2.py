import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture drops the hypothesis that x and y must belong to the set X.
    A valid counterexample will provide a transitive group G, and points x, y
    such that one is in the domain X and the other is not, causing their
    stabilizers to have different orbit sizes on X.
    """
    try:
        # Extract G, x, y from the witness
        if isinstance(witness, dict):
            G = witness.get('G')
            x = witness.get('x', 0)
            y = witness.get('y', getattr(G, 'degree', 100))
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                G, x, y = witness
            elif len(witness) == 4:
                G, _, x, y = witness
            elif len(witness) >= 1:
                G = witness[0]
                x = 0
                y = getattr(G, 'degree', 100)
            else:
                return [False, False]
        else:
            G = witness
            x = 0
            y = getattr(G, 'degree', 100)
    except Exception:
        return [False, False]

    # H_1: G is a group acting transitively on a set X
    try:
        h1 = bool(G.is_transitive())
    except Exception:
        h1 = False

    # ¬Q: The multiset of orbit sizes of G_x on X is NOT identical to G_y on X
    try:
        domain = set(range(G.degree))
        
        def get_orbit_sizes(pt):
            H = G
            try:
                # If the point is in the domain, we take its stabilizer.
                # If it's outside the domain, its stabilizer is the whole group G.
                if isinstance(pt, (int, sympy.Integer)) and pt in domain:
                    H = G.stabilizer(int(pt))
            except Exception:
                pass
            
            orbs = H.orbits()
            covered = sum(len(o) for o in orbs)
            sizes = [len(o) for o in orbs]
            # Pad with 1s for any points in the domain that are fixed and not listed in orbits
            sizes.extend([1] * (G.degree - covered))
            return sorted(sizes)
            
        sizes_x = get_orbit_sizes(x)
        sizes_y = get_orbit_sizes(y)
        
        neg_q = sizes_x != sizes_y
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting transitively on a set X",
    "¬Q: The multiset of orbit sizes of G_x on X is not identical to the multiset of orbit sizes of G_y on X"
]

N_HYP = 1
NEG_Q_INDEX = 1