import sympy
from sympy import Poly, eye, zeros, Symbol, sympify
from sympy.matrices import MatrixBase
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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

def conditions(witness) -> list[bool]:
    try:
        # Extract the primary object if a collection is provided
        if isinstance(witness, (tuple, list)):
            witness = witness[0]

        # Determine the polynomial p(x)
        if isinstance(witness, Poly):
            p = witness
        elif isinstance(witness, MatrixBase):
            var = Symbol('x')
            p_expr = witness.minimal_polynomial(var)
            p = Poly(p_expr, var)
        else:
            expr = sympify(witness)
            symbols = expr.free_symbols
            if len(symbols) == 1:
                var = list(symbols)[0]
            elif len(symbols) == 0:
                var = Symbol('x')
            else:
                var = Symbol('x') if Symbol('x') in symbols else list(symbols)[0]
            p = Poly(expr, var)
            
        # If the domain is not a field (e.g., ZZ), lift it to its field of fractions (e.g., QQ)
        if not p.domain.is_Field:
            try:
                p = p.set_domain(p.domain.get_field())
            except Exception:
                pass
                
        # H_1: F is a field
        h1 = p.domain.is_Field
        
        # H_2: p(x) is the minimal polynomial of alpha over F
        # A minimal polynomial must be monic and have degree >= 1
        h2 = p.degree() >= 1 and p.LC() == 1
        
        # H_3: E is a splitting field of p(x) over F
        # A splitting field always exists for any polynomial over a field
        h3 = True
        
        # ¬Q: Not every root of p(x) in E has the same multiplicity
        # sqf_list() groups square-free factors by their multiplicity.
        # If there is more than one group, there are roots with different multiplicities.
        sqf = p.sqf_list()[1]
        neg_q = len(sqf) > 1
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: p(x) is the minimal polynomial of alpha over F",
    "H_3: E is a splitting field of p(x) over F",
    "¬Q: Not every root of p(x) in E has the same multiplicity"
]

N_HYP = 3
NEG_Q_INDEX = 3