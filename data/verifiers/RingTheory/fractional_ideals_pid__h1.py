import sympy
import functools

# Top-level setup: named object bindings that the witness expression may reference.
# We provide standard variables for defining polynomial rings and ideals.
x, y, z, t = sympy.symbols('x y z t')

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (vars, M_gens)
    where:
      - vars is a tuple of sympy.Symbol objects defining the polynomial ring R = QQ[vars].
      - M_gens is a list of sympy.Expr objects (rational functions in vars) 
        generating the fractional ideal M.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        vars, M_gens = witness
    except Exception:
        return [False, False, False]
        
    # H_1: K is the field of fractions of R
    # By our representation, R = QQ[vars] and K = QQ(vars).
    # We just verify that vars is a valid non-empty tuple of symbols.
    try:
        h1 = isinstance(vars, (tuple, list)) and len(vars) > 0 and all(isinstance(v, sympy.Symbol) for v in vars)
    except Exception:
        h1 = False

    # H_2: M is a finitely generated fractional ideal of R
    # We verify that M_gens is a non-empty list of valid rational functions in vars.
    try:
        h2 = False
        if h1 and isinstance(M_gens, (tuple, list)) and len(M_gens) > 0:
            valid_gens = True
            for m in M_gens:
                if not isinstance(m, sympy.Expr):
                    valid_gens = False
                    break
                try:
                    n, d = sympy.fraction(sympy.cancel(m))
                    # Ensure the expression only uses the allowed variables
                    if not n.free_symbols.issubset(set(vars)) or not d.free_symbols.issubset(set(vars)):
                        valid_gens = False
                        break
                    # Ensure numerator and denominator are polynomials
                    if not n.is_polynomial(*vars) or not d.is_polynomial(*vars):
                        valid_gens = False
                        break
                except Exception:
                    valid_gens = False
                    break
            h2 = valid_gens
    except Exception:
        h2 = False

    # neg_Q: M is NOT a principal fractional ideal
    # M is principal iff there exists d in K such that M = dR.
    # We can clear denominators by multiplying M by the product of all denominators,
    # yielding an ideal I in R. M is principal iff I is principal.
    # In QQ[vars], an ideal I is principal iff its Groebner basis generates the GCD of its generators.
    try:
        neg_q = False
        if h1 and h2:
            # Find the product of all denominators
            denoms = [sympy.fraction(sympy.cancel(m))[1] for m in M_gens]
            common_d = sympy.S.One
            for d in denoms:
                common_d *= d
            
            # Generators of the ideal I = common_d * M in R
            I_gens = [sympy.cancel(m * common_d) for m in M_gens]
            
            I_gens_poly = []
            for p in I_gens:
                n, d = sympy.fraction(p)
                I_gens_poly.append(n)
            
            # If all generators are 0, the ideal is (0), which is principal.
            if all(p == 0 for p in I_gens_poly):
                neg_q = False
            else:
                # Compute the GCD of all generators
                g = functools.reduce(sympy.gcd, I_gens_poly)
                
                # Compute the Groebner basis of I
                gb = sympy.groebner(I_gens_poly, *vars, domain='QQ')
                
                # Reduce the GCD modulo the Groebner basis
                rem = sympy.reduced(g, gb, *vars, domain='QQ')[1]
                
                # If the remainder is not 0, the GCD is not in I, so I is not principal.
                neg_q = (rem != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "H_2: M is a finitely generated fractional ideal of R",
    "¬Q: M is not a principal fractional ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2