import sympy
from sympy.combinatorics.homomorphisms import GroupHomomorphism
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics import PermutationGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: f is a group homomorphism from G to H",
    "H_2: the image f(G) is a finite group",
    "¬Q: the domain group G is not finite"
]

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, GroupHomomorphism):
            h1 = True
            G = witness.domain
            H = witness.codomain
            
            try:
                img = witness.image()
                if isinstance(img, PermutationGroup):
                    h2 = True
                elif hasattr(img, 'order') and img.order() != sympy.oo:
                    h2 = True
                elif hasattr(img, 'is_finite') and img.is_finite:
                    h2 = True
            except Exception:
                if isinstance(H, PermutationGroup):
                    h2 = True
                elif hasattr(H, 'order') and H.order() != sympy.oo:
                    h2 = True
                elif hasattr(H, 'is_finite') and H.is_finite:
                    h2 = True
                    
            if isinstance(G, FreeGroup):
                neg_q = True
            elif hasattr(G, 'order') and G.order() == sympy.oo:
                neg_q = True
            elif hasattr(G, 'is_finite') and not G.is_finite:
                neg_q = True
                
        elif isinstance(witness, tuple) and len(witness) == 3:
            G, H, f = witness
            
            if isinstance(f, GroupHomomorphism):
                h1 = True
                try:
                    img = f.image()
                    if isinstance(img, PermutationGroup):
                        h2 = True
                    elif hasattr(img, 'order') and img.order() != sympy.oo:
                        h2 = True
                    elif hasattr(img, 'is_finite') and img.is_finite:
                        h2 = True
                except Exception:
                    if isinstance(H, PermutationGroup):
                        h2 = True
                    elif hasattr(H, 'order') and H.order() != sympy.oo:
                        h2 = True
                    elif hasattr(H, 'is_finite') and H.is_finite:
                        h2 = True
                        
                if isinstance(G, FreeGroup):
                    neg_q = True
                elif hasattr(G, 'order') and G.order() == sympy.oo:
                    neg_q = True
                elif hasattr(G, 'is_finite') and not G.is_finite:
                    neg_q = True
                    
            elif G == sympy.S.Integers or G is int:
                test_vals = [-10, -5, -1, 0, 1, 5, 10]
                is_hom = True
                for x in test_vals:
                    for y in test_vals:
                        try:
                            val1 = f(x + y)
                            if H == sympy.S.Integers or H is int:
                                val2 = f(x) + f(y)
                            else:
                                val2 = f(x) * f(y)
                            if val1 != val2:
                                is_hom = False
                                break
                        except Exception:
                            is_hom = False
                            break
                    if not is_hom:
                        break
                h1 = is_hom
                
                try:
                    id_val = f(0)
                    is_finite_img = False
                    for k in range(1, 101):
                        if f(k) == id_val:
                            is_finite_img = True
                            break
                    if is_finite_img:
                        h2 = True
                    elif isinstance(H, PermutationGroup):
                        h2 = True
                    elif hasattr(H, 'order') and H.order() != sympy.oo:
                        h2 = True
                    elif hasattr(H, 'is_finite') and H.is_finite:
                        h2 = True
                except Exception:
                    pass
                    
                neg_q = True
                
            elif isinstance(G, FreeGroup):
                try:
                    gens = G.generators
                    if gens:
                        g1 = gens[0]
                        g2 = gens[0]**2
                        g3 = gens[-1]
                        test_words = [G.identity, g1, g2, g3, g1*g3, g3*g1]
                        is_hom = True
                        for x in test_words:
                            for y in test_words:
                                if f(x * y) != f(x) * f(y):
                                    is_hom = False
                                    break
                            if not is_hom:
                                break
                        h1 = is_hom
                    else:
                        h1 = True
                except Exception:
                    pass
                
                try:
                    if isinstance(H, PermutationGroup):
                        h2 = True
                    elif hasattr(H, 'order') and H.order() != sympy.oo:
                        h2 = True
                    elif hasattr(H, 'is_finite') and H.is_finite:
                        h2 = True
                except Exception:
                    pass
                
                neg_q = True
                
            elif hasattr(G, 'generators') or hasattr(G, 'elements'):
                try:
                    elems = []
                    if hasattr(G, 'identity'):
                        elems.append(G.identity)
                    if hasattr(G, 'generators'):
                        gens = list(G.generators)
                        elems.extend(gens)
                        if len(gens) >= 2:
                            elems.append(gens[0]*gens[1])
                            elems.append(gens[1]*gens[0])
                        if len(gens) >= 1:
                            elems.append(gens[0]**2)
                    elif hasattr(G, 'elements'):
                        for i, e in enumerate(G.elements):
                            elems.append(e)
                            if i > 20:
                                break
                                
                    is_hom = True
                    for x in elems:
                        for y in elems:
                            if f(x * y) != f(x) * f(y):
                                is_hom = False
                                break
                        if not is_hom:
                            break
                    h1 = is_hom
                except Exception:
                    pass
                
                try:
                    if isinstance(H, PermutationGroup):
                        h2 = True
                    elif hasattr(H, 'order') and H.order() != sympy.oo:
                        h2 = True
                    elif hasattr(H, 'is_finite') and H.is_finite:
                        h2 = True
                except Exception:
                    pass
                
                try:
                    if isinstance(G, FpGroup):
                        pass # Unsafe to call order() on FpGroup as it may hang
                    elif hasattr(G, 'order') and G.order() == sympy.oo:
                        neg_q = True
                    elif hasattr(G, 'is_finite') and not G.is_finite:
                        neg_q = True
                except Exception:
                    pass

    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]