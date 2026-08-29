import sympy
from sympy import Poly, roots, primitive_element, Dummy, minpoly, Symbol
from sympy.abc import x
from sympy.ntheory import isprime
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    "H_1: F is a field of characteristic 0",
    "H_2: f(x) is an irreducible polynomial of prime degree p",
    "H_3: Galois group of f(x) is solvable",
    "¬Q: There exist two distinct roots of f(x) that do not generate the entire splitting field"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if hasattr(witness, 'free_symbols') and len(witness.free_symbols) == 1:
            var = list(witness.free_symbols)[0]
        else:
            var = x
        f = Poly(witness, var)
    except Exception:
        try:
            f = Poly(witness, x)
        except Exception:
            return [False, False, False, False]
            
    try:
        h1 = (f.domain.char == 0)
    except Exception:
        h1 = False
        
    try:
        deg = f.degree()
        h2 = isprime(deg) and f.is_irreducible
    except Exception:
        h2 = False
        
    h3 = False
    neg_q = False
    
    try:
        rts = roots(f, multiple=True)
        
        if len(rts) < deg:
            h3 = False
        else:
            def field_degree(gens):
                unique_gens = []
                for g in gens:
                    if g not in unique_gens:
                        unique_gens.append(g)
                if not unique_gens:
                    return 1
                if len(unique_gens) == 1:
                    return minpoly(unique_gens[0]).degree()
                d = Dummy('d')
                poly, _ = primitive_element(unique_gens, d, polys=True)
                return poly.degree()

            deg_E = field_degree(rts)
            
            if deg_E is not None:
                if deg <= 4:
                    h3 = True
                elif isprime(deg):
                    h3 = (deg_E % deg == 0) and ((deg * (deg - 1)) % deg_E == 0)
                else:
                    h3 = True
                
                generates_all = True
                for i in range(len(rts)):
                    for j in range(i + 1, len(rts)):
                        if rts[i] != rts[j]:
                            deg_pair = field_degree([rts[i], rts[j]])
                            if deg_pair is not None and deg_pair < deg_E:
                                generates_all = False
                                break
                    if not generates_all:
                        break
                
                neg_q = not generates_all
    except Exception:
        pass
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]