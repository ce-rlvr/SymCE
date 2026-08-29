import math
from sympy import isprime, Poly, factor_list, degree, sympify, Integer
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup
from sympy.combinatorics.named_groups import CyclicGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    try:
        if isinstance(witness, dict):
            p = witness.get('p', 2)
            q = witness.get('q', p)
            a = witness.get('a')
            f = witness.get('f')
        else:
            if len(witness) == 4:
                w1, w2, a, f = witness
                try:
                    iw1, iw2 = int(w1), int(w2)
                    if isprime(iw1) and not isprime(iw2):
                        p, q = iw1, iw2
                    elif isprime(iw2) and not isprime(iw1):
                        p, q = iw2, iw1
                    else:
                        p, q = iw1, iw2
                except Exception:
                    p, q = w1, w2
            elif len(witness) == 3:
                p, a, f = witness
                q = p
            elif len(witness) == 2:
                a, f = witness
                p, q = 2, 2
            else:
                return [False, False, False]
                
        # H1: F_q is a finite field of characteristic p
        k = 0
        try:
            p_val = int(p)
            q_val = int(q)
        except Exception:
            p_val = None
            q_val = None
            
        if p_val is not None and q_val is not None:
            if isprime(p_val) and q_val > 0:
                temp = q_val
                while temp % p_val == 0:
                    temp //= p_val
                    k += 1
                if temp == 1 and k >= 1:
                    h1 = True
                    
        # H2: a in F_q
        if h1:
            try:
                a_val = int(a)
                h2 = True
                # Trace of a from F_q to F_p, assuming a is in F_p
                trace_a = (k * a_val) % p_val
            except Exception:
                h2 = False
                
        # neg_Q
        if h1 and h2:
            try:
                if isinstance(f, str):
                    f = f.replace('^', '**')
                f_expr = sympify(f)
                free_syms = f_expr.free_symbols
                if len(free_syms) == 1:
                    var = list(free_syms)[0]
                else:
                    var = x
                
                f_poly = Poly(f_expr, var)
                flist = factor_list(f_poly, modulus=p_val)
                
                # Check irreducibility over F_p
                if len(flist[1]) == 1 and flist[1][0][1] == 1:
                    is_irred_Fp = True
                    deg_f = degree(flist[1][0][0], var)
                else:
                    is_irred_Fp = False
                    deg_f = 0
                    
                # Check irreducibility over F_q (where q = p^k)
                if is_irred_Fp:
                    is_irred_Fq = (math.gcd(int(deg_f), k) == 1)
                else:
                    is_irred_Fq = False
                    
                trace_nonzero = (trace_a != 0)
                
                conclusion = (is_irred_Fq == trace_nonzero)
                neg_q = not conclusion
            except Exception:
                neg_q = False
                
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field of characteristic p",
    "H_2: a in F_q",
    "¬Q: The conclusion fails (f(x) is irreducible over F_q iff Tr(a) != 0 is FALSE)"
]

N_HYP = 2
NEG_Q_INDEX = 2