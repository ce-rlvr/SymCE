import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
from sympy.polys import Poly
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: a is a non-zero element of R",
    "¬Q: R/(a) is indecomposable iff a = p^k u fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        ring_str = ""
        if isinstance(witness, (tuple, list)):
            if len(witness) >= 2:
                ring_str = str(witness[0])
            a = witness[-1]
        else:
            a = witness
            
        a_sym = sympy.sympify(a)
    except Exception:
        return [False, False, False]

    try:
        # Determine H1: R is a PID
        h1 = True
        if ring_str:
            ring_str_clean = ring_str.replace(' ', '')
            if any(sub in ring_str_clean for sub in ['[x,y]', '[y,x]', '[x,z]', '[y,z]', '[x,y,z]']):
                h1 = False
            if any(sub in ring_str_clean for sub in ['Z[x]', 'Z[y]', 'Z[z]']):
                h1 = False
        
        free_symbols = list(a_sym.free_symbols)
        if len(free_symbols) > 1:
            h1 = False
            
        is_z = a_sym.is_zero
        if is_z is None:
            a_sym = sympy.simplify(a_sym)
            is_z = a_sym.is_zero
            if is_z is None:
                is_z = (a_sym == 0)
                
        h2 = not is_z
        
        if is_z:
            return [h1, h2, False]
            
        # Determine if a is a unit and count its prime factors
        is_unit = False
        num_prime_factors = 0
        
        if len(free_symbols) == 1:
            # Polynomial in one variable
            var = free_symbols[0]
            try:
                p = Poly(a_sym, var, domain='QQ')
                factors = sympy.factor_list(p)
                num_prime_factors = len(factors[1])
                if num_prime_factors == 0:
                    is_unit = True
            except Exception:
                h1 = False
                is_unit = False
                num_prime_factors = 2 # Dummy to make neg_q False
        elif a_sym.is_Rational:
            if a_sym.is_Integer:
                a_int = int(a_sym)
                if abs(a_int) == 1:
                    is_unit = True
                elif ring_str and any(sub in ring_str for sub in ['Q', 'R', 'C', 'Field', 'Rational', 'Real', 'Complex']):
                    is_unit = True
                else:
                    factors = factorint(abs(a_int))
                    num_prime_factors = len(factors)
            else:
                # Rational but not integer -> must be in a field
                is_unit = True
        else:
            # Constant but not rational (e.g. float, pi, I, sqrt(2))
            is_gaussian_int = False
            try:
                re, im = a_sym.as_real_imag()
                if re.is_Integer and im.is_Integer:
                    is_gaussian_int = True
                    norm = re**2 + im**2
                    if norm == 1:
                        is_unit = True
                    else:
                        is_unit = False
                        num_prime_factors = 1 # Dummy value to make neg_q = False
            except Exception:
                pass
                
            if not is_gaussian_int:
                is_unit = True # Assume field or unit in algebraic integer ring
                
        if is_unit:
            # For a unit, R/(a) = 0. In the context of this false conjecture, 
            # 0 is considered indecomposable, making units the counterexample.
            lhs = True
            rhs = False
        else:
            lhs = (num_prime_factors <= 1)
            rhs = (num_prime_factors == 1)
            
        conclusion = (lhs == rhs)
        neg_q = not conclusion
        
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]