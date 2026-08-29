import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.homomorphisms import GroupHomomorphism
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_infinite_order(o):
    return o == float('inf') or o == sympy.oo or o == 0

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Case 1: witness is a dict with explicit elements and operations
        if isinstance(witness, dict) and 'op_G' in witness:
            G = witness.get('G', [])
            op_G = witness.get('op_G')
            id_G = witness.get('id_G')
            H = witness.get('H', [])
            op_H = witness.get('op_H')
            id_H = witness.get('id_H')
            f = witness.get('f')
            
            f_func = (lambda x: f[x]) if isinstance(f, dict) else f
                
            h1 = True
            for x in G:
                for y in G:
                    if f_func(op_G(x, y)) != op_H(f_func(x), f_func(y)):
                        h1 = False
                        break
                if not h1:
                    break
                    
            h2 = True
            for x in G:
                curr = x
                is_finite = False
                for _ in range(2000):
                    if curr == id_G:
                        is_finite = True
                        break
                    curr = op_G(curr, x)
                if not is_finite:
                    h2 = False
                    break
                    
            neg_q = False
            for x in G:
                fx = f_func(x)
                curr = fx
                is_finite = False
                for _ in range(2000):
                    if curr == id_H:
                        is_finite = True
                        break
                    curr = op_H(curr, fx)
                if not is_finite:
                    neg_q = True
                    break
                    
            return [h1, h2, neg_q]
            
        # Case 2: witness is a sympy GroupHomomorphism
        elif isinstance(witness, GroupHomomorphism):
            G = witness.domain
            H = witness.codomain
            
            h1 = True
            if hasattr(G, 'elements'):
                for x in G.elements:
                    for y in G.elements:
                        if witness(x * y) != witness(x) * witness(y):
                            h1 = False
                            break
                    if not h1:
                        break
            else:
                for g1 in G.generators:
                    for g2 in G.generators:
                        if witness(g1 * g2) != witness(g1) * witness(g2):
                            h1 = False
                            break
                            
            h2 = True
            if hasattr(G, 'is_periodic'):
                h2 = G.is_periodic() if callable(G.is_periodic) else G.is_periodic
            elif hasattr(G, 'elements'):
                for g in G.elements:
                    if is_infinite_order(g.order()):
                        h2 = False
                        break
            else:
                if isinstance(G, PermutationGroup):
                    h2 = True
                else:
                    h2 = False
                    
            neg_q = False
            if hasattr(G, 'elements'):
                for g in G.elements:
                    fx = witness(g)
                    if is_infinite_order(fx.order()):
                        neg_q = True
                        break
            else:
                for g in G.generators:
                    fx = witness(g)
                    if is_infinite_order(fx.order()):
                        neg_q = True
                        break
                        
            return [h1, h2, neg_q]
            
        # Case 3: witness has G, H, f (either tuple, object, or simple dict)
        else:
            if isinstance(witness, tuple) and len(witness) == 3:
                G, H, f = witness
            elif hasattr(witness, 'G') and hasattr(witness, 'H') and hasattr(witness, 'f'):
                G = witness.G
                H = witness.H
                f = witness.f
            elif isinstance(witness, dict) and 'G' in witness and 'H' in witness and 'f' in witness:
                G = witness['G']
                H = witness['H']
                f = witness['f']
            else:
                return [False, False, False]
                
            f_func = (lambda x: f[x]) if isinstance(f, dict) else f
            elements = G.elements if hasattr(G, 'elements') else G
            
            h1 = True
            try:
                for x in elements:
                    for y in elements:
                        if f_func(x * y) != f_func(x) * f_func(y):
                            h1 = False
                            break
                    if not h1:
                        break
            except Exception:
                h1 = False
                
            h2 = True
            if hasattr(G, 'is_periodic'):
                h2 = G.is_periodic() if callable(G.is_periodic) else G.is_periodic
            else:
                try:
                    for x in elements:
                        if hasattr(x, 'order'):
                            if is_infinite_order(x.order()):
                                h2 = False
                                break
                        else:
                            h2 = False
                            break
                except Exception:
                    h2 = False
                    
            neg_q = False
            try:
                for x in elements:
                    fx = f_func(x)
                    if hasattr(fx, 'order'):
                        if is_infinite_order(fx.order()):
                            neg_q = True
                            break
            except Exception:
                pass
                
            return [h1, h2, neg_q]
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f: G \\to H is a group homomorphism",
    "H_2: G is a periodic group (every element has finite order)",
    "¬Q: The image f(G) is not a periodic group"
]

N_HYP = 2
NEG_Q_INDEX = 2