import sympy
from sympy import Poly, Symbol, groebner
from sympy.abc import x, y, z

# Top-level setup
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC
ZZ = sympy.ZZ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the Weak Nullstellensatz
    without the algebraically closed field hypothesis.
    
    Witness format: (domain, variables, generators)
    Example: (QQ, (x,), [x**2 + 1])
    """
    
    def check_H1():
        try:
            if not isinstance(witness, (list, tuple)) or len(witness) != 3:
                return False
            domain, variables, generators = witness
            if not hasattr(domain, 'is_Field') or not domain.is_Field:
                return False
            if not isinstance(variables, (list, tuple)) or len(variables) < 1:
                return False
            if not all(isinstance(v, Symbol) for v in variables):
                return False
            if not isinstance(generators, (list, tuple)) or len(generators) < 1:
                return False
            # Verify that all generators are valid polynomials in the given variables
            for g in generators:
                Poly(g, *variables, domain=domain)
            return True
        except Exception:
            return False

    def check_H2():
        try:
            domain, variables, generators = witness
            gb = groebner(generators, *variables, domain=domain)
            
            # A zero-dimensional ideal in n variables must have a Groebner basis of length >= n.
            # For our supported maximal ideals, we expect exactly n elements.
            if len(gb) != len(variables):
                return False
            
            non_linear_count = 0
            for g in gb:
                p = Poly(g, *variables, domain=domain)
                if p.degree() == 1:
                    continue
                else:
                    non_linear_count += 1
                    # The non-linear generator must be univariate and irreducible
                    free = p.as_expr().free_symbols.intersection(set(variables))
                    if len(free) != 1:
                        return False
                    v = list(free)[0]
                    p_uni = Poly(p.as_expr(), v, domain=domain)
                    if not p_uni.is_irreducible:
                        return False
                    
            # To be a maximal ideal (and a field quotient), at most one generator 
            # in the reduced Groebner basis can be non-linear (degree > 1) under this simplified check.
            if non_linear_count > 1:
                return False
                
            return True
        except Exception:
            return False

    def check_neg_Q():
        try:
            domain, variables, generators = witness
            gb = groebner(generators, *variables, domain=domain)
            
            # If it doesn't have exactly n generators, it's not of the form (x_1 - a_1, ..., x_n - a_n)
            if len(gb) != len(variables):
                return True
                
            # If it is of the form (x_1 - a_1, ..., x_n - a_n), the reduced Groebner basis 
            # will consist entirely of degree 1 polynomials.
            for g in gb:
                p = Poly(g, *variables, domain=domain)
                if p.degree() != 1:
                    return True
            return False
        except Exception:
            return False

    return [check_H1(), check_H2(), check_neg_Q()]

CONDITION_LABELS = ["H_1: R is a polynomial ring in n variables over K", "H_2: M is a maximal ideal of R", "¬Q: M is not of the form (x_1 - a_1, ..., x_n - a_n)"]

N_HYP = 2
NEG_Q_INDEX = 2