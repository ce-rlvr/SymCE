import sympy
from sympy import Dummy, groebner, Poly, expand
import itertools

# Top-level setup: named object bindings that the witness expression may reference.
# We provide standard variables for polynomial rings.
x, y, z, w, u, v = sympy.symbols('x y z w u v')

def is_zero_divisor(I, f, gens, gb_I):
    """
    Checks if f is a zero-divisor in Q[gens]/I.
    Computes the ideal quotient I : f by finding I \cap (f) using elimination.
    """
    t = Dummy('t')
    J = [expand(t * p) for p in I] + [expand((1 - t) * f)]
    gb = groebner(J, t, *gens, order='lex')
    intersection_gens = [p.as_expr() for p in gb if not p.has(t)]
    
    for p in intersection_gens:
        q, r = Poly(p, *gens, domain='QQ').div(Poly(f, *gens, domain='QQ'))
        if r.is_zero:
            _, rem_g = q.reduce(gb_I)
            if not rem_g.is_zero:
                return True
    return False

def krull_dimension(I, gens):
    """
    Computes the Krull dimension of Q[gens]/I at the origin.
    Uses the maximum size of an independent set of variables modulo the initial ideal.
    """
    if not gens:
        return 0
    if not I:
        return len(gens)
        
    gb = groebner(I, *gens, order='grevlex')
    lms = []
    for p in gb:
        if p != 0:
            lms.append(Poly(p, *gens, domain='QQ').lead_monom())
            
    if not lms:
        return len(gens)
        
    for k in range(len(gens), -1, -1):
        for subset in itertools.combinations(gens, k):
            independent = True
            for lm in lms:
                if lm.free_symbols.issubset(set(subset)):
                    independent = False
                    break
            if independent:
                return k
    return 0

def depth(I, gens):
    """
    Computes the depth of Q[gens]/I localized at the origin.
    Finds the length of a maximal regular sequence in the maximal ideal (gens).
    """
    if not gens:
        return 0
    if not I:
        return len(gens)
    
    current_I = [p for p in I if p != 0]
    d = 0
    
    # Generate a deterministic set of candidate linear combinations
    candidates = []
    for g in gens:
        candidates.append(g)
    for g1, g2 in itertools.combinations(gens, 2):
        candidates.append(g1 + g2)
        candidates.append(g1 - g2)
    for subset in itertools.combinations(gens, 3):
        candidates.append(sum(subset))
        candidates.append(subset[0] - subset[1] - subset[2])
    if len(gens) > 1:
        candidates.append(sum((i+1)*g for i, g in enumerate(gens)))
        candidates.append(sum((i+1)**2 * g for i, g in enumerate(gens)))
        candidates.append(sum((i+2)*g for i, g in enumerate(gens)))
        
    while True:
        found_regular = False
        if not current_I:
            gb_current = []
        else:
            gb_current = groebner(current_I, *gens)
            
        for f in candidates:
            if not gb_current:
                rem = Poly(f, *gens, domain='QQ')
            else:
                _, rem = Poly(f, *gens, domain='QQ').reduce(gb_current)
                
            if rem.is_zero:
                continue
            
            if not is_zero_divisor(current_I, f, gens, gb_current):
                current_I = current_I + [f]
                d += 1
                found_regular = True
                break
                
        if not found_regular:
            break
            
    return d

def conditions(witness):
    """
    Evaluates the remaining hypotheses and the negated conclusion.
    The witness is expected to be a list of SymPy expressions generating an ideal I.
    The local ring is R = (Q[gens]/I)_m where m is the maximal ideal at the origin.
    """
    try:
        if not isinstance(witness, list):
            return [False, False]
            
        gens_set = set()
        for p in witness:
            if not hasattr(p, 'free_symbols'):
                return [False, False]
            gens_set.update(p.free_symbols)
        gens = sorted(list(gens_set), key=lambda s: s.name)
        
        # H_1: (R, m) is a commutative Noetherian local ring
        # This holds if the ideal is contained in the maximal ideal at the origin.
        h1_ok = True
        for p in witness:
            if p.subs({g: 0 for g in gens}) != 0:
                h1_ok = False
                break
                
        if not h1_ok:
            return [False, False]
            
        if not gens:
            # The ring is just Q, which is a field and hence Cohen-Macaulay.
            return [True, False]
            
        dim = krull_dimension(witness, gens)
        dep = depth(witness, gens)
        
        # ¬Q: R is NOT a Cohen-Macaulay ring
        # A local ring is Cohen-Macaulay iff its Krull dimension equals its depth.
        neg_q = (dim != dep)
        
        return [h1_ok, neg_q]
        
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: (R, m) is a commutative Noetherian local ring",
    "¬Q: R is not a Cohen-Macaulay ring"
]

N_HYP = 1
NEG_Q_INDEX = 1