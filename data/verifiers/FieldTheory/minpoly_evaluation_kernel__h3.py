import sympy as sp
from sympy import Poly, minpoly
from sympy.abc import x

# Top-level setup for potential witness expressions
QQ = sp.QQ
ZZ = sp.ZZ
RR = sp.RR
CC = sp.CC

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a dictionary or a tuple containing the algebraic element alpha and the 
    generator of the kernel of the homomorphism phi.
    """
    try:
        if isinstance(witness, dict):
            alpha = witness.get('alpha')
            if 'phi_ker' in witness:
                ker_gen = witness['phi_ker']
            elif 'phi_kernel' in witness:
                ker_gen = witness['phi_kernel']
            elif 'ker_phi' in witness:
                ker_gen = witness['ker_phi']
            elif 'beta' in witness:
                ker_gen = minpoly(witness['beta'], x)
            elif 'phi_image' in witness:
                ker_gen = minpoly(witness['phi_image'], x)
            else:
                ker_gen = witness.get('ker_gen', x)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                alpha, ker_gen = witness
            elif len(witness) == 3:
                _, alpha, ker_gen = witness
            elif len(witness) == 4:
                _, _, alpha, ker_gen = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: F is a field and E is an extension field of F
    # We implicitly work over F = QQ and E = QQ(alpha) or C.
    # This holds as long as alpha is a valid commutative expression.
    try:
        h1 = alpha is not None and getattr(alpha, 'is_commutative', True)
    except Exception:
        h1 = False

    # H_2: alpha in E is an element algebraic over F
    try:
        m_poly = minpoly(alpha, x)
        h2 = m_poly is not None and Poly(m_poly, x).degree() >= 1
    except Exception:
        h2 = False

    # neg_Q: The kernel of phi is NOT the principal ideal <m(x)>
    try:
        if not h2:
            neg_q = False
        else:
            p_m = Poly(m_poly, x)
            
            if isinstance(ker_gen, sp.Eq):
                ker_gen = ker_gen.lhs - ker_gen.rhs

            if not isinstance(ker_gen, dict) and not isinstance(ker_gen, sp.Poly):
                if hasattr(ker_gen, 'free_symbols'):
                    fs = ker_gen.free_symbols
                    if len(fs) == 1:
                        var = list(fs)[0]
                        ker_gen = ker_gen.subs(var, x)
            
            if isinstance(ker_gen, dict):
                if x in ker_gen:
                    p_k = Poly(minpoly(ker_gen[x], x), x)
                else:
                    p_k = Poly(0, x)
            elif isinstance(ker_gen, sp.Poly):
                if ker_gen.gen != x:
                    p_k = Poly(ker_gen.as_expr().subs(ker_gen.gen, x), x)
                else:
                    p_k = ker_gen
            else:
                p_k = Poly(ker_gen, x)
            
            if p_k.is_zero and p_m.is_zero:
                neg_q = False
            elif p_k.is_zero or p_m.is_zero:
                neg_q = True
            else:
                # In a field F, two polynomials generate the same ideal iff their monic forms are equal.
                expr_k = p_k.monic().as_expr()
                expr_m = p_m.monic().as_expr()
                diff = sp.expand(expr_k - expr_m)
                neg_q = diff != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field and E is an extension field of F",
    "H_2: alpha in E is an element algebraic over F",
    "¬Q: The kernel of phi is NOT the principal ideal <m(x)>"
]

N_HYP = 2
NEG_Q_INDEX = 2