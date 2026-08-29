import sympy
from sympy import Poly, Symbol
from sympy.abc import x, y, z
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools

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
    "H_1: R is a commutative ring",
    "¬Q: The set of all leading coefficients of polynomials in I, together with 0, does not form an ideal in R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)):
            return [False, False]
            
        if not witness:
            return [False, False]

        # Find a variable to use for polynomials
        symbols = set()
        for w in witness:
            if hasattr(w, 'free_symbols'):
                symbols.update(w.free_symbols)
                
        if not symbols:
            poly_var = Symbol('x')
        else:
            # Sort to be deterministic
            poly_var = sorted(list(symbols), key=lambda s: s.name)[0]
            
        # H_1: R is a commutative ring
        # We verify that all symbols involved are commutative.
        # SymPy's standard polynomial domains (ZZ, QQ, RR, CC, GF, EX) are all commutative rings.
        h1_ok = True
        for w in witness:
            if hasattr(w, 'free_symbols'):
                for sym in w.free_symbols:
                    if not getattr(sym, 'is_commutative', True):
                        h1_ok = False
                        break
            if not h1_ok:
                break
                
        if not h1_ok:
            return [False, False]
                
        # Convert all witness elements to Poly objects
        polys = []
        for w in witness:
            if isinstance(w, Poly):
                polys.append(w)
            else:
                polys.append(Poly(w, poly_var))
                
        # Unify domains to find the common ring R
        domain = polys[0].domain
        for p in polys[1:]:
            domain = domain.unify(p.domain)
            
        # Extract the set of leading coefficients L, together with 0
        L = {domain.zero}
        for p in polys:
            p_unif = p.set_domain(domain)
            if not p_unif.is_zero:
                L.add(p_unif.LC())
                
        # Check if L forms an ideal in R
        is_ideal = True
        
        # 1. Closed under addition
        for a in L:
            for b in L:
                if domain.add(a, b) not in L:
                    is_ideal = False
                    break
            if not is_ideal:
                break
                
        # 2. Closed under scalar multiplication by elements of R
        if is_ideal:
            if hasattr(domain, 'is_FiniteField') and domain.is_FiniteField:
                # For finite fields, check multiplication by all elements
                for a in L:
                    for r in range(domain.order):
                        r_dom = domain.from_sympy(sympy.Integer(r))
                        if domain.mul(r_dom, a) not in L:
                            is_ideal = False
                            break
                    if not is_ideal:
                        break
            else:
                # For infinite domains (like ZZ, QQ, ZZ[y]), a finite set L 
                # can only be an ideal if it is exactly {0}.
                if any(a != domain.zero for a in L):
                    is_ideal = False
                    
        neg_q = not is_ideal
        
        return [h1_ok, neg_q]
    except Exception:
        return [False, False]