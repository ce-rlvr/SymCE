import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
from sympy.polys.domains import Domain

# Top-level setup for witness expressions
# ZZ, QQ, x, y, z are available for constructing polynomial rings or ideals.

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I and J are ideals of R",
    "¬Q: S^{-1}(IJ) != (S^{-1}I)(S^{-1}J) as ideals in S^{-1}R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture drops the hypothesis that S is a multiplicatively closed subset.
    Without this, S^{-1}R is not a valid ring, and the equality of ideals fails.
    """
    try:
        # Case 1: Witness is a finite ring Z/nZ represented as a dictionary
        if isinstance(witness, dict) and 'n' in witness:
            n = witness['n']
            I = set(witness['I'])
            J = set(witness['J'])
            S = set(witness['S'])
            
            h1 = (n >= 2)
            
            def is_ideal(A):
                if not A: return False
                if 0 not in A: return False
                for a in A:
                    for b in A:
                        if (a + b) % n not in A: return False
                for a in A:
                    for r in range(n):
                        if (a * r) % n not in A: return False
                return True
                
            h2 = is_ideal(I) and is_ideal(J)
            
            # The conclusion fails if S is not multiplicatively closed (or empty)
            if not S:
                neg_q = True
            else:
                is_mult_closed = True
                for a in S:
                    for b in S:
                        if (a * b) % n not in S:
                            is_mult_closed = False
                            break
                    if not is_mult_closed:
                        break
                neg_q = not is_mult_closed
                
            return [bool(h1), bool(h2), bool(neg_q)]
            
        # Case 2: Witness uses sympy domains (e.g., ZZ, QQ)
        else:
            if isinstance(witness, dict) and 'R' in witness:
                R = witness['R']
                I = witness['I']
                J = witness['J']
                S = witness['S']
            elif isinstance(witness, (tuple, list)) and len(witness) == 4:
                R, I, J, S = witness
            else:
                return [False, False, False]
                
            h1 = isinstance(R, Domain) or R in (sympy.ZZ, sympy.QQ)
            
            h2 = False
            try:
                from sympy.polys.agca.ideals import Ideal
                if isinstance(I, Ideal) and isinstance(J, Ideal):
                    h2 = True
            except ImportError:
                pass
                
            if not h2:
                # If provided as lists of generators
                h2 = isinstance(I, (list, tuple, set)) and isinstance(J, (list, tuple, set))
                if h2:
                    for elem in I:
                        if elem not in R: h2 = False
                    for elem in J:
                        if elem not in R: h2 = False
                        
            if not S:
                neg_q = True
            else:
                is_mult_closed = True
                for a in S:
                    for b in S:
                        if (a * b) not in S:
                            is_mult_closed = False
                            break
                    if not is_mult_closed:
                        break
                neg_q = not is_mult_closed
                
            return [bool(h1), bool(h2), bool(neg_q)]
            
    except Exception:
        pass
        
    return [False, False, False]