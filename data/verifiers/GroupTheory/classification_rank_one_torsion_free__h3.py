import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Linear algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

class FinitelyGeneratedAbelianGroup:
    """
    Helper class to represent a finitely generated abelian group
    by its invariant factors. 0 represents a Z factor.
    """
    def __init__(self, invariants):
        self.invariants = list(invariants)
        self.is_abelian = True
        self.is_torsion_free = all(val == 0 for val in self.invariants)

    def abelian_invariants(self):
        return self.invariants

    def order(self):
        if all(val != 0 for val in self.invariants):
            ans = 1
            for val in self.invariants:
                ans *= val
            return ans
        return sympy.oo

# Custom bindings for this specific domain
Z2_free = FinitelyGeneratedAbelianGroup([0, 0])
Z3_free = FinitelyGeneratedAbelianGroup([0, 0, 0])

def conditions(witness):
    # Allow passing a list of invariant factors directly
    if isinstance(witness, (list, tuple)) and all(isinstance(val, int) for val in witness):
        witness = FinitelyGeneratedAbelianGroup(witness)
        
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Check H1: G is an abelian group
        if hasattr(witness, 'is_abelian'):
            h1 = bool(witness.is_abelian)
        elif hasattr(witness, 'generators'):
            gens = witness.generators
            is_ab = True
            for g in gens:
                for h in gens:
                    if g * h != h * g:
                        is_ab = False
                        break
                if not is_ab:
                    break
            h1 = is_ab
    except Exception:
        h1 = False

    try:
        # Check H2: G is torsion-free
        if hasattr(witness, 'order') and witness.order() != sympy.oo:
            # A finite group is torsion-free iff it is the trivial group
            h2 = (witness.order() == 1)
        elif hasattr(witness, 'abelian_invariants'):
            invs = witness.abelian_invariants()
            h2 = all(val == 0 for val in invs)
        elif hasattr(witness, 'is_torsion_free'):
            h2 = bool(witness.is_torsion_free)
    except Exception:
        h2 = False

    try:
        # Check neg_Q: G is NOT isomorphic to a subgroup of Q
        if hasattr(witness, 'order') and witness.order() != sympy.oo:
            # The only finite subgroup of Q is the trivial group
            is_subgroup_of_Q = (witness.order() == 1)
            neg_q = not is_subgroup_of_Q
        elif hasattr(witness, 'abelian_invariants'):
            # A finitely generated abelian group is isomorphic to a subgroup of Q
            # iff it is torsion-free and has rank <= 1.
            invs = witness.abelian_invariants()
            rank = len([val for val in invs if val == 0])
            has_torsion = any(val != 0 for val in invs)
            is_subgroup_of_Q = (not has_torsion) and (rank <= 1)
            neg_q = not is_subgroup_of_Q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: G is torsion-free",
    "¬Q: G is not isomorphic to a subgroup of Q"
]

N_HYP = 2
NEG_Q_INDEX = 2