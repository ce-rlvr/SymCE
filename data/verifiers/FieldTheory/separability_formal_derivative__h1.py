import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
x = sp.Symbol('x')
y = sp.Symbol('y')
z = sp.Symbol('z')

def conditions(witness) -> list[bool]:
    """
    Given a witness polynomial, checks if it satisfies the remaining hypotheses
    and falsifies the conclusion of the conjecture.
    """
    try:
        # Ensure the witness is a sympy Poly object
        if isinstance(witness, sp.Poly):
            f = witness
        else:
            f = sp.Poly(witness)
            
        # The conjecture specifies f(x) \in F[x], so it must be univariate
        if len(f.gens) != 1:
            return [False, False]
            
        # H_1: f(x) is a non-constant polynomial
        h1 = f.degree() >= 1
        
        # Evaluate the conclusion:
        # "f(x) has no multiple roots in any extension field of F iff f(x) and f'(x) are relatively prime in F[x]"
        
        # 1. Check if f(x) has no multiple roots in any extension field.
        # This is equivalent to checking if f and f' are relatively prime over the fraction field of F.
        K = f.domain.get_field()
        f_K = f.set_domain(K)
        g_K = f_K.gcd(f_K.diff())
        has_no_mult_roots = (g_K.degree() == 0)
        
        # 2. Check if f(x) and f'(x) are relatively prime in F[x].
        # This means their gcd in F[x] must be a unit in F[x] (which implies degree 0 and LC is a unit in F).
        g = f.gcd(f.diff())
        if g.degree() == 0:
            try:
                is_unit = f.domain.is_unit(g.LC())
            except AttributeError:
                # Fallback if the domain lacks the is_unit method
                is_unit = (sp.S(1) / g.LC() in f.domain)
            is_rel_prime = bool(is_unit)
        else:
            is_rel_prime = False
            
        # The conclusion Q is the equivalence of the two statements above
        Q = (has_no_mult_roots == is_rel_prime)
        
        # We want the conclusion to FAIL at the witness
        neg_Q = not Q
        
        return [bool(h1), bool(neg_Q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: f(x) is a non-constant polynomial",
    "¬Q: The equivalence between having no multiple roots and being relatively prime to its derivative fails"
]

N_HYP = 1
NEG_Q_INDEX = 1