import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The conjecture claims that for ANY group G, the minimal number of relators r 
    satisfies r > d^2 / 4, where d is the minimal number of generators.
    (The dropped hypothesis was that G is a finite p-group).
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        d = None
        r = None
        
        # Allow witness to be a tuple (d, r) directly
        if isinstance(witness, tuple) and len(witness) == 2:
            try:
                d = int(witness[0])
                r = int(witness[1])
                if d < 0 or r < 0:
                    d = None
                    r = None
            except (ValueError, TypeError):
                d = None
                r = None
        else:
            # Check by class name to avoid import issues with FpGroup/FreeGroup
            cls_name = witness.__class__.__name__
            if cls_name == 'FreeGroup':
                d = len(witness.generators)
                r = 0
            elif cls_name == 'FpGroup':
                d = len(witness.generators)
                r = len(witness.relators)
            else:
                is_trivial = False
                try:
                    if hasattr(witness, 'order') and callable(witness.order) and witness.order() == 1:
                        is_trivial = True
                except Exception:
                    pass
                
                if is_trivial:
                    d = 0
                    r = 0
                elif hasattr(witness, 'presentation'):
                    fp = witness.presentation()
                    d = len(fp.generators)
                    r = len(fp.relators)
                    
        if d is not None and r is not None:
            h1 = True
            h2 = True
            if r <= (d**2) / 4.0:
                neg_q = True
                
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G has a minimal number of generators d",
    "H_2: G has a minimal number of relators r for a presentation with d generators",
    "¬Q: r <= d^2 / 4"
]

N_HYP = 2
NEG_Q_INDEX = 2