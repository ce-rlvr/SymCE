import sympy
from sympy import sympify, factor_list
from sympy.ntheory import factorint
from sympy.abc import x, y, z

# Top-level setup
# No specific named objects needed for this ring theory conjecture,
# but we provide common symbols in case the witness is a polynomial.

def conditions(witness):
    try:
        # The witness can be just the element `a`, or a tuple `(R, a)`.
        if isinstance(witness, tuple) and len(witness) == 2:
            R, a = witness
        else:
            a = witness
            
        a_sym = sympify(a)
        if hasattr(a_sym, 'as_expr'):
            a_sym = a_sym.as_expr()
            
        # H1: R is a principal ideal domain
        # We assume R is Z if a is an integer, or F[x] if a is a univariate polynomial.
        # Both are PIDs. If there are multiple variables, it's not a PID.
        free_syms = a_sym.free_symbols
        if len(free_syms) > 1:
            h1 = False
        else:
            h1 = True
            
        # Evaluate properties of `a`
        if a_sym.is_zero:
            is_zero = True
            is_unit = False
            is_pp = False
        elif a_sym.is_number:
            if not a_sym.is_Integer:
                return [False, False, False]
            is_zero = False
            val = int(a_sym)
            is_unit = abs(val) == 1
            if not is_unit:
                factors = factorint(abs(val))
                is_pp = len(factors) == 1
            else:
                is_pp = False
        else:
            is_zero = False
            if a_sym.is_constant():
                is_unit = True
                is_pp = False
            else:
                is_unit = False
                const, factors = factor_list(a_sym)
                is_pp = len(factors) == 1
                
        # H2: a is not a unit in R
        h2 = not is_unit
        
        # Evaluate if R/(a) is indecomposable
        # If a = 0, R/(0) is isomorphic to R. Since R is a PID, it is an integral domain,
        # and thus indecomposable as a module over itself.
        # If a != 0, R/(a) is a torsion module, which is indecomposable iff a is a prime power.
        if is_zero:
            is_indec = True
        else:
            is_indec = is_pp
            
        # Conclusion Q: R/(a) is indecomposable iff a = p^k u
        conclusion = (is_indec == is_pp)
        
        # neg_Q: The conclusion fails
        neg_q = not conclusion
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: a is not a unit in R",
    "¬Q: R/(a) is indecomposable iff a = p^k u fails"
]

N_HYP = 2
NEG_Q_INDEX = 2