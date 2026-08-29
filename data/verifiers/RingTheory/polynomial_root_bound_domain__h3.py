import sympy
from sympy import Symbol, Poly, Expr, isprime
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis was that f(x) has degree n.
    The witness should provide the polynomial f and the integer n.
    Optionally, it can provide the ring R and a list of roots.
    """
    try:
        f = None
        n = None
        roots = None
        R = None
        
        if isinstance(witness, dict):
            f = witness.get('f')
            n = witness.get('n')
            roots = witness.get('roots')
            R = witness.get('R')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                f, n = witness
            elif len(witness) == 3:
                f, n, roots = witness
            elif len(witness) == 4:
                R, f, n, roots = witness
                
        if f is None or n is None:
            return [False, False, False]
            
        if isinstance(f, str):
            f = sympy.sympify(f)
            
        # H_1: R is an integral domain
        h1 = True
        if R is not None:
            if isinstance(R, int):
                h1 = isprime(R)
            elif hasattr(R, 'is_domain'):
                h1 = R.is_domain
            elif str(R) in ['Z4', 'Z6', 'Z8', 'Z9', 'Z10', 'Z12']:
                h1 = False
                
        # H_2: f(x) is a non-zero polynomial
        h2 = False
        if hasattr(f, 'is_zero') and f.is_zero is not None:
            h2 = not f.is_zero
        else:
            h2 = (f != 0)
            
        # neg_Q: f(x) has more than n distinct roots in R
        neg_q = False
        var = list(f.free_symbols)[0] if hasattr(f, 'free_symbols') and f.free_symbols else Symbol('x')
        
        if R is not None and isinstance(R, int):
            if roots is not None:
                distinct_roots = []
                for r in roots:
                    if r not in distinct_roots:
                        distinct_roots.append(r)
                if len(distinct_roots) > n:
                    all_valid = True
                    for r in distinct_roots:
                        if f.subs(var, r) % R != 0:
                            all_valid = False
                            break
                    if all_valid:
                        neg_q = True
            else:
                rts = [i for i in range(R) if f.subs(var, i) % R == 0]
                if len(rts) > n:
                    neg_q = True
        else:
            if roots is not None:
                distinct_roots = []
                for r in roots:
                    if r not in distinct_roots:
                        distinct_roots.append(r)
                if len(distinct_roots) > n:
                    all_valid = True
                    for r in distinct_roots:
                        val = f.subs(var, r)
                        if hasattr(val, 'simplify'):
                            val = val.simplify()
                        if val != 0:
                            all_valid = False
                            break
                    if all_valid:
                        neg_q = True
            else:
                rts = sympy.roots(f, var)
                if len(rts) > n:
                    neg_q = True
                    
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: f(x) is a non-zero polynomial in the polynomial ring over R",
    "¬Q: f(x) has more than n distinct roots in R"
]

N_HYP = 2
NEG_Q_INDEX = 2