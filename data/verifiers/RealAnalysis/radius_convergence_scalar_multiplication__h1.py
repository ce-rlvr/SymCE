import sympy as sp
import math

# Top-level setup
n = sp.Symbol('n', integer=True, positive=True)
x = sp.Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis was the one defining R as the radius of convergence of \sum a_n x^n.
    Without it, R is unconstrained, so \sum (c a_n) x^n will generally not have radius R.
    
    Expected witness format: a dictionary {'c': value, 'a_n': expression_in_n, 'R': value}
    or a tuple (c, a_n, R).
    """
    h1_ok = False
    neg_q_ok = False
    
    try:
        if isinstance(witness, dict):
            c = witness.get('c')
            a_n = witness.get('a_n')
            R = witness.get('R')
        elif isinstance(witness, tuple) and len(witness) >= 3:
            c = witness[0]
            a_n = witness[1]
            R = witness[2]
        else:
            c = witness
            a_n = None
            R = None
            
        # Check H1: Let c \neq 0 be a real constant
        if c is not None:
            if isinstance(c, (int, float)):
                h1_ok = (c != 0)
            elif isinstance(c, sp.Expr):
                h1_ok = c.is_constant() and (sp.simplify(c) != 0)
                if h1_ok and c.is_real is False:
                    h1_ok = False
            elif isinstance(c, complex):
                h1_ok = (c != 0) and (c.imag == 0)
            else:
                h1_ok = False
                
        # Check neg_Q: The power series \sum_{n=0}^{\infty} (c a_n) x^n does NOT have the same radius of convergence R
        if a_n is not None and R is not None and c is not None:
            n_sym = sp.Symbol('n', integer=True, positive=True)
            
            if callable(a_n):
                term = c * a_n(n_sym)
            elif isinstance(a_n, sp.Expr):
                free_ns = [s for s in a_n.free_symbols if s.name == 'n']
                if free_ns:
                    term = c * a_n.subs(free_ns[0], n_sym)
                else:
                    term = c * a_n
            else:
                term = c * a_n
                
            R_new = None
            
            if term == 0:
                R_new = sp.oo
            else:
                # Try ratio test
                try:
                    ratio = sp.simplify(sp.Abs(term / term.subs(n_sym, n_sym+1)))
                    L = sp.limit(ratio, n_sym, sp.oo)
                    if L == sp.oo:
                        R_new = sp.oo
                    elif L == 0:
                        R_new = 0
                    elif not L.has(sp.nan) and not L.has(sp.oo):
                        R_new = L
                except Exception:
                    pass
                    
                # Try root test if ratio test failed or gave nan
                if R_new is None:
                    try:
                        root = sp.Abs(term)**(1/n_sym)
                        L_root = sp.limit(root, n_sym, sp.oo)
                        if L_root == 0:
                            R_new = sp.oo
                        elif L_root == sp.oo:
                            R_new = 0
                        elif not L_root.has(sp.nan):
                            R_new = 1 / L_root
                    except Exception:
                        pass
            
            if R_new is not None:
                if R_new == sp.oo and R == sp.oo:
                    neg_q_ok = False
                elif R_new == sp.oo or R == sp.oo:
                    neg_q_ok = True
                else:
                    try:
                        diff = sp.simplify(R_new - R)
                        neg_q_ok = (diff != 0)
                    except Exception:
                        neg_q_ok = (R_new != R)
                        
    except Exception:
        pass
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Let c != 0 be a real constant",
    "¬Q: The power series \\sum_{n=0}^{\\infty} (c a_n) x^n does NOT have the same radius of convergence R"
]

N_HYP = 1
NEG_Q_INDEX = 1