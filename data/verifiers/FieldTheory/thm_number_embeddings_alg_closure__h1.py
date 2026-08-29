import sympy
from sympy import Poly
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: L is a finite separable field extension of K of degree n",
    "H_2: E is an algebraically closed field containing K",
    "¬Q: There are not exactly n distinct field homomorphisms from L to E that fix K pointwise"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # If the witness is a permutation group representing the Galois group of the extension
        if hasattr(witness, 'is_transitive'):
            h1 = bool(witness.is_transitive())
            h2 = True
            neg_q = False
            return [h1, h2, neg_q]
            
        if isinstance(witness, (tuple, list)) and hasattr(witness[0], 'is_transitive'):
            h1 = bool(witness[0].is_transitive())
            h2 = True
            neg_q = False
            return [h1, h2, neg_q]

        # If the witness is a polynomial or an algebraic field element representing L = K[x]/(f)
        if hasattr(witness, 'minpoly'):
            f = Poly(witness.minpoly)
        else:
            if isinstance(witness, (tuple, list)):
                f = Poly(witness[0])
            else:
                f = Poly(witness)
                
        domain = f.domain
        # Default integer polynomials to the rational field for field extension context
        if domain == sympy.ZZ:
            f = f.set_domain(sympy.QQ)
            domain = sympy.QQ
            
        n = f.degree()
        is_field = getattr(domain, 'is_Field', True)
        
        # Check irreducibility (L is a field)
        is_irred = f.is_irreducible
        if is_irred is None:
            try:
                factors = f.factor_list()
                is_irred = (len(factors[1]) == 1 and factors[1][0][1] == 1)
            except Exception:
                is_irred = True
                
        # Check separability (no repeated roots in the algebraic closure)
        is_sep = f.is_squarefree
        
        h1 = bool(is_field and is_irred and is_sep and n > 0)
        
        # E is an algebraically closed field containing K (theoretical setup, always holds)
        h2 = True
        
        # The number of distinct field homomorphisms from L to E is the number of distinct roots 
        # of the minimal polynomial in the algebraically closed field E.
        # This equals the degree of the square-free part of f.
        sqf_deg = f.sqf_part().degree()
        neg_q = bool(sqf_deg != n)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]