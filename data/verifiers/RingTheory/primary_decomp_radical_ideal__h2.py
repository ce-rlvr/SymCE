import sympy
from sympy.ntheory import factorint

# Top-level setup for potential witness expressions
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    """
    Evaluates the hypotheses and negated conclusion for the false conjecture:
    "If R is a commutative ring with identity and I admits a minimal primary 
    decomposition, then each primary component is a prime ideal."
    
    The witness can be:
      - An integer `m` (or sympy.Integer), interpreted as the ideal <m> in Z.
      - A univariate sympy polynomial `f(x)`, interpreted as the ideal <f> in QQ[x].
    """
    try:
        # 1. Interpret polynomial witness as an ideal in QQ[x]
        if isinstance(witness, (sympy.Expr, sympy.Poly)) and len(witness.free_symbols) == 1:
            f = sympy.poly(witness, domain='QQ')
            
            # H1: QQ[x] is a commutative ring with identity
            h1 = True
            
            # H2: Proper ideals in QQ[x] admit a minimal primary decomposition
            h2 = f.degree() > 0
            
            # ¬Q: In a PID like QQ[x], primary components are <p_i^k_i>.
            # They are prime ideals iff k_i = 1.
            factors = sympy.factor_list(f)
            neg_q = any(k > 1 for p, k in factors[1])
            
            return [bool(h1), bool(h2), bool(neg_q)]
            
        # 2. Interpret integer witness as an ideal in Z
        if isinstance(witness, tuple):
            ring, m = witness
            if ring != 'Z':
                return [False, False, False]
        else:
            m = witness
            
        if isinstance(m, sympy.Expr):
            if not m.is_Integer:
                return [False, False, False]
        elif not isinstance(m, int) or isinstance(m, bool):
            return [False, False, False]
            
        m = abs(int(m))
        
        # H1: Z is a commutative ring with identity
        h1 = True
        
        # H2: Proper ideals in Z admit a minimal primary decomposition
        h2 = (m != 1)
        
        # ¬Q: In Z, primary components of <m> are <p_i^k_i>. 
        # They are prime ideals iff k_i = 1.
        if m == 0:
            # <0> is prime, so its primary component is prime
            neg_q = False
        else:
            factors = factorint(m)
            neg_q = any(k > 1 for k in factors.values())
            
        return [bool(h1), bool(h2), bool(neg_q)]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I admits a minimal primary decomposition",
    "¬Q: At least one primary component is not a prime ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2