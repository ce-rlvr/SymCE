import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z

# Top-level setup
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

def is_equicontinuous(family, domain):
    if not family:
        return True
    
    from sympy import Symbol, sympify, S
    from sympy.calculus.util import continuous_domain
    
    vars = set()
    for f in family:
        f = sympify(f)
        vars.update(f.free_symbols)
    
    vars = {v for v in vars if v.is_Symbol}
    
    if not vars:
        var = Symbol('x')
    elif len(vars) == 1:
        var = list(vars)[0]
    else:
        var_names = {v.name: v for v in vars}
        if 'x' in var_names:
            var = var_names['x']
        else:
            var = list(vars)[0]
        
    for f in family:
        f = sympify(f)
        if var not in f.free_symbols:
            continue
        try:
            cd = continuous_domain(f, var, S.Reals)
            if not domain.is_subset(cd):
                return False
        except Exception:
            return False
    return True

def conditions(witness) -> list[bool]:
    try:
        domain = witness['domain']
        F = witness['F']
        c = witness['c']
        G = witness['G']
        
        from sympy import Set, sympify
        
        # H1: X is a metric space
        h1 = isinstance(domain, Set)
        
        # H2: F is an equicontinuous family of functions from X to R
        h2 = is_equicontinuous(F, domain)
        
        # H3: c is a real number
        c_sym = sympify(c)
        h3 = c_sym.is_real == True
        
        # neg_Q: sums and multiples are equicontinuous
        sums = []
        for f in F:
            for g in G:
                sums.append(sympify(f) + sympify(g))
                
        multiples = []
        for f in F:
            multiples.append(c_sym * sympify(f))
            
        q = is_equicontinuous(sums, domain) and is_equicontinuous(multiples, domain)
        neg_q = not q
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: F is an equicontinuous family of functions from X to R",
    "H_3: c is a real number",
    "¬Q: The family of sums and the family of scalar multiples are not both equicontinuous"
]

N_HYP = 3
NEG_Q_INDEX = 3