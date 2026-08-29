import sympy
from sympy import Rational, gcd

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def get_penultimate_convergents(r):
    """
    Given a rational number r, returns a list of its possible penultimate convergents
    based on its two finite simple continued fraction representations.
    """
    p, q = r.p, r.q
    a = []
    while q != 0:
        a.append(p // q)
        p, q = q, p % q
        
    def get_conv(cf):
        if not cf:
            return None
        num, den = 1, 0
        for x in reversed(cf):
            num, den = den + x * num, num
        if den == 0:
            return None
        return Rational(num, den)
        
    res = []
    
    # First standard continued fraction expansion
    if len(a) > 1:
        c = get_conv(a[:-1])
        if c is not None:
            res.append(c)
            
    # Second equivalent continued fraction expansion (ending in 1)
    if a:
        cf2 = a[:-1] + [a[-1] - 1, 1]
        if len(cf2) > 1:
            c = get_conv(cf2[:-1])
            if c is not None:
                res.append(c)
                
    return res

def conditions(witness):
    # H1: p_{n-1}/q_{n-1} and p_{n-2}/q_{n-2} are the (n-1)-th and (n-2)-th convergents 
    # of a simple continued fraction, respectively.
    try:
        p_n1 = witness['p_n1']
        q_n1 = witness['q_n1']
        p_n2 = witness['p_n2']
        q_n2 = witness['q_n2']
        
        if q_n1 == 0 or q_n2 == 0:
            h1 = False
        else:
            r1 = Rational(p_n1, q_n1)
            r2 = Rational(p_n2, q_n2)
            pens = get_penultimate_convergents(r1)
            h1 = r2 in pens
    except Exception:
        h1 = False

    # H2: x = p_{n-2} + k p_{n-1} and y = q_{n-2} + k q_{n-1}
    try:
        p_n1 = witness['p_n1']
        q_n1 = witness['q_n1']
        p_n2 = witness['p_n2']
        q_n2 = witness['q_n2']
        k = witness['k']
        x = witness['x']
        y = witness['y']
        
        h2 = (x == p_n2 + k * p_n1) and (y == q_n2 + k * q_n1)
    except Exception:
        h2 = False

    # Negated Conclusion: The integers x and y are NOT coprime
    try:
        x = witness['x']
        y = witness['y']
        
        if int(x) != x or int(y) != y:
            neg_q = False
        else:
            neg_q = gcd(int(x), int(y)) != 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p_{n-1}/q_{n-1} and p_{n-2}/q_{n-2} are the (n-1)-th and (n-2)-th convergents of a simple continued fraction",
    "H_2: x = p_{n-2} + k p_{n-1} and y = q_{n-2} + k q_{n-1}",
    "¬Q: The integers x and y are not coprime"
]

N_HYP = 2
NEG_Q_INDEX = 2