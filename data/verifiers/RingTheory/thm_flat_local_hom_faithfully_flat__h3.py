import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z = sp.symbols('x y z')

class QuotientRingHomomorphism:
    """
    Represents a ring homomorphism f: R -> S, where:
      R = QQ[vars] / I_R
      S = QQ[vars] / I_S
    and f is the natural quotient map (requires I_R subset I_S).
    
    This is used to construct witnesses for the conjecture.
    """
    def __init__(self, vars, I_R, I_S):
        self.vars = vars
        self.I_R = I_R
        self.I_S = I_S

# Example of a valid counterexample witness:
# R = QQ[x] / (x^2), S = QQ[x] / (x)
# f is the natural quotient map.
# R and S are local rings, f is a local homomorphism.
# S is not faithfully flat over R.
witness_example = QuotientRingHomomorphism([x], [x**2], [x])

def conditions(witness) -> list[bool]:
    try:
        # Parse the witness
        if isinstance(witness, dict):
            vars = witness['vars']
            I_R = witness['I_R']
            I_S = witness['I_S']
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            vars, I_R, I_S = witness
        else:
            vars = witness.vars
            I_R = witness.I_R
            I_S = witness.I_S
            
        if not isinstance(vars, (list, tuple)):
            vars = [vars]
        if not isinstance(I_R, (list, tuple)):
            I_R = [I_R]
        if not isinstance(I_S, (list, tuple)):
            I_S = [I_S]
            
        def to_expr(p):
            if isinstance(p, sp.Eq):
                return p.lhs - p.rhs
            return p
            
        I_R = [to_expr(p) for p in I_R]
        I_S = [to_expr(p) for p in I_S]
        
    except Exception:
        return [False, False, False]

    try:
        # H_1: R and S are local rings
        # In our finite-dimensional quotient setup over QQ, a ring is local iff 
        # the variety of its ideal consists of exactly one point (the unique maximal ideal).
        roots_R = sp.solve(I_R, vars, dict=True)
        roots_S = sp.solve(I_S, vars, dict=True)
        
        R_is_local = False
        if len(roots_R) == 1:
            root = roots_R[0]
            # Ensure it's a single point (zero-dimensional) and not parameterized
            if len(root) == len(vars) and all(isinstance(v, (int, float)) or (hasattr(v, 'is_number') and v.is_number) for v in root.values()):
                R_is_local = True
                
        S_is_local = False
        if len(roots_S) == 1:
            root = roots_S[0]
            if len(root) == len(vars) and all(isinstance(v, (int, float)) or (hasattr(v, 'is_number') and v.is_number) for v in root.values()):
                S_is_local = True
                
        h1_ok = R_is_local and S_is_local
    except Exception:
        h1_ok = False

    try:
        # H_2: f: R -> S is a local ring homomorphism
        # f is well-defined if I_R is a subset of I_S
        I_S_clean = [p for p in I_S if sp.simplify(p) != 0]
        if not I_S_clean:
            I_R_subset_I_S = all(sp.simplify(p) == 0 for p in I_R)
        else:
            GB_S = list(sp.groebner(I_S_clean, vars))
            I_R_subset_I_S = all(sp.simplify(sp.reduced(p, GB_S, vars)[1]) == 0 for p in I_R)
            
        # f is a local homomorphism if the pullback of m_S is m_R.
        # Since both have exactly one maximal ideal, their roots must match.
        if h1_ok:
            local_hom = (roots_R[0] == roots_S[0])
        else:
            local_hom = False
            
        h2_ok = I_R_subset_I_S and local_hom
    except Exception:
        h2_ok = False

    try:
        # ¬Q: S is not a faithfully flat R-module
        # For Artinian local rings and a surjective homomorphism, S is flat over R 
        # iff f is an isomorphism (i.e., I_S is a subset of I_R).
        # A flat module over a local ring is faithfully flat iff it is non-zero.
        # Since S is local, it is non-zero. Thus S is faithfully flat iff I_S subset I_R.
        I_R_clean = [p for p in I_R if sp.simplify(p) != 0]
        if not I_R_clean:
            I_S_subset_I_R = all(sp.simplify(p) == 0 for p in I_S)
        else:
            GB_R = list(sp.groebner(I_R_clean, vars))
            I_S_subset_I_R = all(sp.simplify(sp.reduced(p, GB_R, vars)[1]) == 0 for p in I_S)
            
        neg_q_ok = not I_S_subset_I_R
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are local rings",
    "H_2: f: R -> S is a local ring homomorphism",
    "¬Q: S is not a faithfully flat R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2