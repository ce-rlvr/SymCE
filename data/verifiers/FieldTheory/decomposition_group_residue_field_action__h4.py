import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Since SymPy does not have a built-in algebraic number theory module for 
    fractional ideals and decomposition groups, this verifier expects a mock 
    object, dictionary, or tuple that provides the boolean values for the conditions.
    """
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_finite_Galois', witness.get('H1', False)))
            h2 = bool(witness.get('p_is_prime', witness.get('H2', False)))
            h3 = bool(witness.get('P_over_p', witness.get('H3', False)))
            
            if 'map_is_surjective' in witness:
                neg_q = not bool(witness['map_is_surjective'])
            elif 'Q' in witness:
                neg_q = not bool(witness['Q'])
            elif 'neg_Q' in witness:
                neg_q = bool(witness['neg_Q'])
                
        elif isinstance(witness, (list, tuple)) and len(witness) >= 4:
            # Assume tuple format is (H1, H2, H3, Q)
            h1 = bool(witness[0])
            h2 = bool(witness[1])
            h3 = bool(witness[2])
            neg_q = not bool(witness[3])
            
        else:
            h1 = bool(getattr(witness, 'is_finite_Galois', getattr(witness, 'H1', False)))
            h2 = bool(getattr(witness, 'p_is_prime', getattr(witness, 'H2', False)))
            h3 = bool(getattr(witness, 'P_over_p', getattr(witness, 'H3', False)))
            
            if hasattr(witness, 'map_is_surjective'):
                neg_q = not bool(getattr(witness, 'map_is_surjective'))
            elif hasattr(witness, 'Q'):
                neg_q = not bool(getattr(witness, 'Q'))
            elif hasattr(witness, 'neg_Q'):
                neg_q = bool(getattr(witness, 'neg_Q'))
                
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension of number fields",
    "H_2: p is a prime ideal of O_K",
    "H_3: P is a prime ideal of O_L lying over p",
    "¬Q: The natural map from D_P to Gal((O_L/P) / (O_K/p)) is not a surjective group homomorphism"
]

N_HYP = 3
NEG_Q_INDEX = 3