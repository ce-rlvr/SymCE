import sympy
from sympy import Symbol, S, solveset, EmptySet, Piecewise, Interval, oo, sin, cos, exp
from sympy.calculus.util import continuous_domain

# Top-level setup
x = Symbol('x', real=True)
y = Symbol('y', real=True)
z = Symbol('z', real=True)

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: C(X, R) is the ring of continuous real-valued functions on X",
    "¬Q: The equivalence 'f is a unit in C(X, R) iff f(x) != 0 for all x' fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is that f must actually be an element of C(X, R) (i.e., continuous).
    Without it, a discontinuous nowhere-zero function satisfies the RHS but is not a unit in C(X, R).
    """
    # Extract f and X from the witness
    if isinstance(witness, dict):
        f = witness.get('f', witness)
        X = witness.get('X', S.Reals)
    else:
        f = witness
        X = S.Reals
        
    # The hypotheses about X and C(X, R) are definitions/context, inherently true for our setup
    h1 = True
    h2 = True
    
    try:
        if not isinstance(f, sympy.Expr):
            return [False, False, False]
            
        free_vars = f.free_symbols
        if len(free_vars) == 1:
            v = list(free_vars)[0]
        elif len(free_vars) == 0:
            v = Symbol('x', real=True)
        else:
            v = list(free_vars)[0]
            
        # Check if f is continuous on X (i.e., f is in C(X, R))
        try:
            cd_f = continuous_domain(f, v, X)
            f_is_continuous = (cd_f == X)
        except Exception:
            f_is_continuous = True
            for p in [0, 1, -1]:
                try:
                    if f.limit(v, p, dir='-') != f.limit(v, p, dir='+'):
                        f_is_continuous = False
                        break
                except Exception:
                    pass
                    
        # Check if 1/f is continuous on X (required for f to be a unit in C(X, R))
        try:
            cd_inv = continuous_domain(1/f, v, X)
            inv_is_continuous = (cd_inv == X)
        except Exception:
            inv_is_continuous = True
            for p in [0, 1, -1]:
                try:
                    if (1/f).limit(v, p, dir='-') != (1/f).limit(v, p, dir='+'):
                        inv_is_continuous = False
                        break
                except Exception:
                    pass
                    
        # f is a unit in C(X, R) iff both f and 1/f are in C(X, R)
        is_unit = f_is_continuous and inv_is_continuous
        
        # Check if f(x) != 0 for all x in X
        try:
            roots = solveset(f, v, domain=X)
            if roots == EmptySet:
                rhs = True
            elif roots.is_empty == False:
                rhs = False
            else:
                # Fallback if solveset returns a ConditionSet or is unsure
                rhs = True
                for val in range(-10, 11):
                    if f.subs(v, val) == 0:
                        rhs = False
                        break
        except Exception:
            rhs = True
            for val in range(-10, 11):
                if f.subs(v, val) == 0:
                    rhs = False
                    break
                    
        # The conclusion fails if the equivalence does not hold
        neg_q = (is_unit != rhs)
        
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]