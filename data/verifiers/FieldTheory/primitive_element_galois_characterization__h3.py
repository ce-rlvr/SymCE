import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
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

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: G is the Galois group of L/K",
    "¬Q: L = K(alpha) is NOT equivalent to the stabilizer of alpha in G being trivial"
]

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    
    The dropped hypothesis from the true theorem is that alpha must be an element of L.
    If alpha is not in L, the equivalence L = K(alpha) <=> Stab_G(alpha) = {1} can fail.
    
    Since SymPy cannot natively compute Galois group actions on elements outside the 
    splitting field, the witness is expected to provide the boolean evaluations directly 
    via a dictionary, a 4-tuple, a callable, or an object with attributes.
    """
    try:
        # Extract boolean flags from the witness based on its type
        if isinstance(witness, (list, tuple)) and len(witness) == 4:
            H1, H2, L_eq, stab = witness
        elif isinstance(witness, dict):
            H1 = witness.get("is_finite_galois", False)
            H2 = witness.get("is_galois_group", False)
            L_eq = witness.get("L_eq_K_alpha", False)
            stab = witness.get("stab_is_trivial", False)
        elif callable(witness):
            H1, H2, L_eq, stab = witness()
        else:
            H1 = getattr(witness, "is_finite_galois", False)
            H2 = getattr(witness, "is_galois_group", False)
            L_eq = getattr(witness, "L_eq_K_alpha", False)
            stab = getattr(witness, "stab_is_trivial", False)
            
        H1_ok = bool(H1)
        H2_ok = bool(H2)
        
        # Conclusion Q: L = K(alpha) iff Stab_G(alpha) is trivial
        # neg_Q is True when this equivalence fails
        neg_Q_ok = (bool(L_eq) != bool(stab))
        
        return [H1_ok, H2_ok, neg_Q_ok]
    except Exception:
        return [False, False, False]