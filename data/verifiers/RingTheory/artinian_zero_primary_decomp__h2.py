import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
# (ZZ and QQ are imported above; no other specific named bindings are strictly required for this domain)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the false conjecture:
    "In an Artinian commutative ring with identity, the zero ideal has a minimal 
    primary decomposition where each Q_i is an M_i-primary ideal."
    
    The dropped hypothesis is that the ring is non-trivial (1 != 0).
    In the trivial ring, there are no proper ideals, hence no prime/maximal ideals,
    and the zero ideal cannot be decomposed into M_i-primary ideals.
    """
    h1 = False
    neg_q = False
    
    try:
        # Handle integer representing the ring Z/nZ
        if isinstance(witness, int) and not isinstance(witness, bool):
            if witness >= 1:
                h1 = True
                # The trivial ring Z/1Z is the counterexample
                neg_q = (witness == 1)
            return [h1, neg_q]
            
        # Handle common string representations for the trivial ring
        if isinstance(witness, str):
            w_lower = witness.lower().replace(" ", "_").replace("-", "_")
            if w_lower in ["trivial_ring", "zero_ring", "z/1z", "z1"]:
                return [True, True]
            
        # Check if it's a SymPy ring or a custom ring-like object
        if hasattr(witness, 'zero') and hasattr(witness, 'one'):
            is_comm = getattr(witness, 'is_commutative', True)
            has_id = True
        else:
            is_comm = getattr(witness, 'is_commutative', False)
            has_id = getattr(witness, 'has_Identity', False) or hasattr(witness, 'one')
        
        if is_comm and has_id:
            # Check if the ring is Artinian
            is_art = False
            if getattr(witness, 'is_Field', False):
                is_art = True
            elif getattr(witness, 'is_finite', False):
                is_art = True
            elif witness == ZZ:
                is_art = False
            elif getattr(witness, 'is_PolynomialRing', False):
                is_art = False
            elif hasattr(witness, 'is_Artinian'):
                is_art = witness.is_Artinian
            else:
                # Default to True for evaluation purposes if it has zero and one
                is_art = True
                
            h1 = is_art
            
            # Check if the conclusion fails (neg_Q is True)
            # The conclusion fails if the ring is trivial (no maximal ideals)
            # or if it's a non-Artinian domain like ZZ or QQ[x] where (0) is prime but not maximal.
            if hasattr(witness, 'zero') and hasattr(witness, 'one'):
                if witness.zero == witness.one:
                    neg_q = True
                elif witness == ZZ or getattr(witness, 'is_PolynomialRing', False):
                    neg_q = True
                else:
                    neg_q = False
            else:
                if witness == ZZ or getattr(witness, 'is_PolynomialRing', False):
                    neg_q = True
                    
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an Artinian commutative ring with identity",
    "¬Q: The zero ideal does not have a minimal primary decomposition into M_i-primary ideals"
]

N_HYP = 1
NEG_Q_INDEX = 1