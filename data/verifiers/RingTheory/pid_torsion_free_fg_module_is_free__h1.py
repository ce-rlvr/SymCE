import sympy
from sympy import groebner, Symbol, Expr
from sympy.abc import x, y, z, t, a, b, c
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard algebra objects
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: M is a finitely generated R-module",
    "H_2: M is a torsion-free module",
    "¬Q: M is not a free R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness is expected to represent an ideal in a polynomial ring over QQ,
    which serves as the module M over the ring R = QQ[variables].
    
    Accepted formats for witness:
      - A list of generators: [x, y]
      - A tuple of (variables, generators): ([x, y], [x, y])
      - A tuple of (PolyRing, generators): (QQ.old_poly_ring(x, y), [x, y])
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        variables = None
        generators = None
        
        # Try parsing as (variables/ring, generators)
        if isinstance(witness, tuple) and len(witness) == 2:
            v, g = witness
            if hasattr(v, 'gens') and isinstance(g, (list, tuple)):
                variables = list(v.gens)
                generators = [sympy.sympify(gen) for gen in g]
            elif isinstance(v, (list, tuple)) and isinstance(g, (list, tuple)):
                variables = list(v)
                generators = [sympy.sympify(gen) for gen in g]
                
        # Try parsing as just a list of generators
        if variables is None and isinstance(witness, (list, tuple)):
            try:
                sym_gens = [sympy.sympify(g) for g in witness]
                if all(isinstance(g, Expr) for g in sym_gens):
                    generators = sym_gens
                    vars_set = set()
                    for g in generators:
                        vars_set.update(g.free_symbols)
                    variables = sorted(list(vars_set), key=lambda sym: sym.name)
                    if not variables:
                        variables = [Symbol('x')]
            except Exception:
                pass
                
        if variables is None or generators is None:
            return [False, False, False]
            
        # H_1: M is a finitely generated R-module
        # True if we have a finite list of expression generators
        if isinstance(generators, (list, tuple)) and len(generators) > 0:
            h1 = all(isinstance(g, Expr) for g in generators)
            
        # H_2: M is a torsion-free module
        # An ideal in a polynomial ring over a field (integral domain) is always torsion-free
        if isinstance(variables, (list, tuple)) and len(variables) > 0:
            h2 = True
            
        # ¬Q: M is not a free R-module
        # An ideal in an integral domain is free iff it is principal.
        # It is principal iff its reduced Groebner basis has length <= 1.
        if h1 and h2:
            gb = groebner(generators, *variables, domain='QQ')
            polys = [p for p in list(gb) if p != 0]
            neg_q = len(polys) > 1
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]