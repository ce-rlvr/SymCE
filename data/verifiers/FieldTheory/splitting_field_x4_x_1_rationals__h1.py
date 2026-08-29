import sympy
from sympy import Poly, Symbol, sqrt
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup for potential witness references
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

x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Hypothesis: K is the splitting field of f(x) over Q
    Conclusion: The Galois group Gal(K/Q) is isomorphic to S4
    """
    try:
        # Extract expression if witness is an equation
        if hasattr(witness, 'lhs'):
            expr = witness.lhs - witness.rhs
        else:
            expr = witness
            
        free_syms = expr.free_symbols
        if len(free_syms) == 1:
            x_sym = list(free_syms)[0]
        elif len(free_syms) == 0:
            x_sym = Symbol('x')
        else:
            return [False, False]
            
        f = Poly(expr, x_sym)
        # Hypothesis 1: f(x) is a polynomial over Q (or Z)
        h1 = (f.domain.is_RationalField or f.domain.is_IntegerRing)
    except Exception:
        h1 = False

    try:
        if not h1:
            is_S4 = False
        else:
            factors = f.factor_list()
            # We only care about factors that contribute to the splitting field's non-triviality
            non_linear_factors = [fac for fac, mult in factors[1] if fac.degree() >= 2]
            
            if len(non_linear_factors) == 0:
                is_S4 = False
            elif len(non_linear_factors) == 1:
                fac = non_linear_factors[0]
                if fac.degree() < 4:
                    is_S4 = False
                elif fac.degree() == 4:
                    # For an irreducible quartic, Gal(K/Q) is S4 iff the discriminant is not a perfect square
                    # and the resolvent cubic is irreducible over Q.
                    disc = fac.discriminant()
                    if sqrt(sympy.S(disc)).is_rational:
                        is_S4 = False
                    else:
                        coeffs = fac.all_coeffs()
                        a4, a3, a2, a1, a0 = [sympy.S(c) for c in coeffs]
                        
                        # Make monic for the resolvent cubic formula
                        a = a3 / a4
                        b = a2 / a4
                        c = a1 / a4
                        d = a0 / a4
                        
                        dummy = Symbol('dummy_var_for_resolvent')
                        resolvent = dummy**3 - b*dummy**2 + (a*c - 4*d)*dummy - a**2*d + 4*b*d - c**2
                        res_poly = Poly(resolvent, dummy, domain='QQ')
                        
                        if res_poly.is_irreducible:
                            is_S4 = True
                        else:
                            is_S4 = False
                else:
                    # For degree > 4, it's generally not S4 (unless it's a very specific reducible polynomial,
                    # but we already isolated the single non-linear core factor).
                    is_S4 = False
            else:
                # Multiple non-linear factors generally do not yield S4 as the Galois group
                is_S4 = False
                
        # neg_q is True when the conclusion FAILS (i.e., Galois group is NOT S4)
        neg_q = not is_S4
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is the splitting field of f(x) over Q",
    "¬Q: The Galois group Gal(K/Q) is not isomorphic to the symmetric group S4"
]

N_HYP = 1
NEG_Q_INDEX = 1