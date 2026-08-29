import sympy
from sympy import QQ, ZZ

# Top-level setup
# A witness can be a tuple (R, d) where R is a SymPy domain (like QQ) and d is an integer,
# or a dictionary/object explicitly providing the boolean properties and integer values.

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # 1. Dictionary-based witness
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative', False) and witness.get('is_noetherian', False))
            h2 = bool(witness.get('is_local', False))
            d = witness.get('d', None)
            min_gens = witness.get('min_gens', None)
            if d is not None and min_gens is not None:
                neg_q = (d != min_gens)
                
        # 2. Tuple-based witness: (Ring, d)
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, d = witness
            
            is_field = False
            if hasattr(R, 'is_Field') and R.is_Field:
                is_field = True
            elif type(R).__name__ in ('RationalField', 'RealField', 'ComplexField', 'FiniteField'):
                is_field = True
                
            if is_field:
                # Fields are commutative, Noetherian, and local.
                # The only maximal ideal is (0), which requires 0 generators.
                h1 = True
                h2 = True
                min_gens = 0
                neg_q = (d != min_gens)
            elif R == ZZ:
                # The integers are commutative and Noetherian, but not local.
                h1 = True
                h2 = False
                
        # 3. Object-based witness
        elif hasattr(witness, 'is_commutative'):
            h1 = bool(getattr(witness, 'is_commutative', False) and getattr(witness, 'is_noetherian', False))
            h2 = bool(getattr(witness, 'is_local', False))
            d = getattr(witness, 'd', None)
            min_gens = getattr(witness, 'min_gens', None)
            if d is not None and min_gens is not None:
                neg_q = (d != min_gens)
                
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: R is a local ring with maximal ideal m",
    "¬Q: d is NOT equal to the minimum number of generators required to generate an m-primary ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2