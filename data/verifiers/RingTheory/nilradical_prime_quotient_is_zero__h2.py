import sympy
from sympy import ntheory
from sympy.abc import x, y, z
from sympy import ZZ, QQ

# Top-level setup for potential witness expressions
Z = ZZ
Q = QQ

def conditions(witness):
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    
    H_1: R is a commutative ring with identity
    Conclusion: The nilradical of the quotient ring R/P is the zero ideal
    """
    h1 = True
    neg_q = False
    
    try:
        # Unpack tuple witnesses like (Ring, Ideal) or (Ring, Generator)
        if isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                ring_obj = witness[0]
                witness = witness[1]
                if hasattr(ring_obj, 'is_commutative'):
                    h1 = bool(ring_obj.is_commutative)
            elif len(witness) == 1:
                witness = witness[0]

        # Case 1: Witness is an integer (representing the ideal nZ in the ring Z)
        if isinstance(witness, (int, sympy.Integer)):
            n = abs(int(witness))
            if n == 0 or n == 1:
                # Z/0Z is Z (nilradical is 0), Z/1Z is the zero ring (nilradical is 0)
                neg_q = False
            else:
                # The nilradical of Z/nZ is non-zero iff n is not square-free
                neg_q = not ntheory.is_square_free(n)
            return [h1, neg_q]
            
        # Case 2: Witness is a SymPy ideal object
        if hasattr(witness, 'ring') and hasattr(witness, 'gens'):
            R = witness.ring
            h1 = getattr(R, 'is_commutative', True)
            gens = witness.gens
            if len(gens) == 1:
                f_expr = gens[0].as_expr()
                coeff, factors = sympy.sqf_list(f_expr)
                is_sqf = all(exp == 1 for _, exp in factors)
                if isinstance(coeff, (int, sympy.Integer)):
                    c = abs(int(coeff))
                    if c > 1 and not ntheory.is_square_free(c):
                        is_sqf = False
                neg_q = not is_sqf
                return [bool(h1), bool(neg_q)]
                
        # Case 3: Witness is a SymPy expression (representing a principal ideal generator)
        if isinstance(witness, sympy.Expr):
            coeff, factors = sympy.sqf_list(witness)
            is_sqf = all(exp == 1 for _, exp in factors)
            if isinstance(coeff, (int, sympy.Integer)):
                c = abs(int(coeff))
                if c > 1 and not ntheory.is_square_free(c):
                    is_sqf = False
            neg_q = not is_sqf
            return [h1, neg_q]
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: The nilradical of the quotient ring R/P is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1