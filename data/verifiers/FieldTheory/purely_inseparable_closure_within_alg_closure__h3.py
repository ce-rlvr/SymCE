import sympy
from sympy.polys.domains import FractionField, FiniteField, PolynomialRing

# Top-level setup
t = sympy.Symbol('t')
x = sympy.Symbol('x')

class DummyAlgebraicClosure:
    """
    A dummy class to represent an algebraic closure, in case the witness 
    generator attempts to instantiate one directly.
    """
    def __init__(self, base_field):
        self.base_field = base_field
        self.characteristic = getattr(base_field, 'characteristic', getattr(base_field, 'char', 0))
        self.is_perfect = True

def is_perfect(E):
    """
    Helper function to determine if a field E is perfect.
    A field of characteristic p > 0 is perfect iff every element is a p-th power.
    Finite fields are perfect. Rational function fields GF(p)(t) are not.
    """
    try:
        if hasattr(E, 'is_perfect'):
            return E.is_perfect
            
        char = getattr(E, 'characteristic', getattr(E, 'char', 0))
        if char == 0 and isinstance(E, str):
            if 'GF(2)' in E or 'F_2' in E: char = 2
            elif 'GF(3)' in E or 'F_3' in E: char = 3
            elif 'GF(5)' in E or 'F_5' in E: char = 5
            elif 'p' in E: char = 2
            
        if char == 0:
            return True
            
        if isinstance(E, FractionField):
            return False
            
        if isinstance(E, FiniteField):
            return True
            
        if isinstance(E, PolynomialRing):
            return False
            
        if isinstance(E, str):
            if '(t)' in E or '(x)' in E:
                return False
            if 'GF' in E or 'F_' in E or 'Fp' in E:
                return True
                
    except Exception:
        pass
        
    return True

def check_char(char):
    try:
        c = int(char)
        return sympy.isprime(c) and c > 0
    except (ValueError, TypeError):
        return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    Returns [H1, H2, neg_Q]
    """
    H1, H2, neg_Q = False, False, False
    
    try:
        if isinstance(witness, dict):
            char = witness.get('char', 0)
            if not char and 'F' in witness:
                F = witness['F']
                char = getattr(F, 'characteristic', getattr(F, 'char', 0))
                if char == 0 and isinstance(F, str):
                    if 'GF(2)' in F or 'F_2' in F: char = 2
                    elif 'GF(3)' in F or 'F_3' in F: char = 3
                    elif 'GF(5)' in F or 'F_5' in F: char = 5
                    elif 'p' in F: char = 2
            H1 = check_char(char)
            
            H2 = witness.get('F_bar_is_alg_closure', True)
            
            if 'E_is_perfect' in witness:
                E_perfect = witness['E_is_perfect']
            elif 'E' in witness:
                E = witness['E']
                E_perfect = is_perfect(E)
            else:
                E_perfect = True
                
            neg_Q = not E_perfect
            return [bool(H1), bool(H2), bool(neg_Q)]
            
        if isinstance(witness, (list, tuple)) and len(witness) >= 3:
            F, F_bar, E = witness[:3]
            
            if isinstance(F, int):
                char = F
            else:
                char = getattr(F, 'characteristic', getattr(F, 'char', 0))
                if char == 0 and isinstance(F, str):
                    if 'GF(2)' in F or 'F_2' in F: char = 2
                    elif 'GF(3)' in F or 'F_3' in F: char = 3
                    elif 'GF(5)' in F or 'F_5' in F: char = 5
                    elif 'p' in F: char = 2
                
            H1 = check_char(char)
            H2 = F_bar is not None
            neg_Q = not is_perfect(E)
            
            return [bool(H1), bool(H2), bool(neg_Q)]
            
        if isinstance(witness, (list, tuple)) and len(witness) == 2:
            F, E = witness
            if isinstance(F, int):
                char = F
            else:
                char = getattr(F, 'characteristic', getattr(F, 'char', 0))
                if char == 0 and isinstance(F, str):
                    if 'GF(2)' in F or 'F_2' in F: char = 2
                    elif 'GF(3)' in F or 'F_3' in F: char = 3
                    elif 'GF(5)' in F or 'F_5' in F: char = 5
                    elif 'p' in F: char = 2
                
            H1 = check_char(char)
            H2 = True
            neg_Q = not is_perfect(E)
            
            return [bool(H1), bool(H2), bool(neg_Q)]
            
        # If witness is just a single field F (assuming E = F)
        F = witness
        if isinstance(F, int):
            char = F
        else:
            char = getattr(F, 'characteristic', getattr(F, 'char', 0))
            if char == 0 and isinstance(F, str):
                if 'GF(2)' in F or 'F_2' in F: char = 2
                elif 'GF(3)' in F or 'F_3' in F: char = 3
                elif 'GF(5)' in F or 'F_5' in F: char = 5
                elif 'p' in F: char = 2
            
        if check_char(char):
            H1 = True
            H2 = True
            neg_Q = not is_perfect(F)
            return [bool(H1), bool(H2), bool(neg_Q)]
            
    except Exception:
        pass
        
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field of prime characteristic p > 0",
    "H_2: \\overline{F} is an algebraic closure of F",
    "¬Q: E is not a subfield of \\overline{F}, or \\overline{F}/E is not separable"
]

N_HYP = 2
NEG_Q_INDEX = 2