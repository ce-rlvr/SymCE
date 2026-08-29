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
    try:
        # Handle witness as a tuple (G, X) or just a group G
        if isinstance(witness, tuple) and len(witness) == 2:
            G = witness[0]
        else:
            G = witness
            
        if not hasattr(G, 'degree') or not hasattr(G, 'stabilizer') or not hasattr(G, 'orbit'):
            return [False, False, False]
            
        h1 = True # X is a set (implicitly the domain of the permutation group)
        h2 = True # G acts on X
        
        degree = G.degree
        if degree == 0:
            any_triv = False
            all_triv = True
            is_trans = True
        else:
            trivials = [G.stabilizer(x).order() == 1 for x in range(degree)]
            any_triv = any(trivials)
            all_triv = all(trivials)
            # A group is transitive if the orbit of a single element covers the entire domain
            is_trans = (len(G.orbit(0)) == degree)
            
        is_regular = is_trans and all_triv
        
        # The literal conclusion "free action iff Stab(x) is trivial for every x" is a tautology.
        # The false conjecture likely arises from dropping the "transitive" hypothesis from:
        # "If G acts transitively, the action is free iff Stab(x) is trivial for SOME x."
        # (with a typographical error replacing "some" with "every" in the prompt's text),
        # OR from dropping "transitive" from:
        # "If G acts transitively, the action is regular iff Stab(x) is trivial for EVERY x."
        # In either interpretation, a valid counterexample will have at least one trivial stabilizer,
        # but will fail to be a regular/free action across the entire domain.
        # We capture both likely intended counterexamples robustly:
        neg_q = any_triv and not is_regular
        
        return [h1, h2, bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts on X",
    "¬Q: The equivalence between free action and trivial stabilizers fails"
]

N_HYP = 2
NEG_Q_INDEX = 2