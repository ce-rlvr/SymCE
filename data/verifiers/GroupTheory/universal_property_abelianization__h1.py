import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, A, f = witness
    except Exception:
        return [False, False, False]

    # H1: A is an abelian group
    try:
        h1 = False
        if isinstance(A, PermutationGroup):
            h1 = A.is_abelian
        else:
            elements_A = list(A.elements) if hasattr(A, 'elements') else list(A)
            
            A_is_group = True
            identity_A = None
            for e in elements_A:
                is_id = True
                for x in elements_A:
                    try:
                        xe = x * e
                        ex = e * x
                    except Exception:
                        xe = x + e
                        ex = e + x
                    if xe != x or ex != x:
                        is_id = False
                        break
                if is_id:
                    identity_A = e
                    break
            if identity_A is None:
                A_is_group = False
            else:
                for x in elements_A:
                    has_inv = False
                    for y in elements_A:
                        try:
                            xy = x * y
                            yx = y * x
                        except Exception:
                            xy = x + y
                            yx = y + x
                        if xy == identity_A and yx == identity_A:
                            has_inv = True
                            break
                    if not has_inv:
                        A_is_group = False
                        break
                        
            if A_is_group:
                is_abelian = True
                for x in elements_A:
                    for y in elements_A:
                        try:
                            xy = x * y
                            yx = y * x
                        except Exception:
                            xy = x + y
                            yx = y + x
                        if xy != yx:
                            is_abelian = False
                            break
                    if not is_abelian:
                        break
                h1 = is_abelian
    except Exception:
        h1 = False

    # H2: f is a group homomorphism from G to A
    try:
        if type(f).__name__ == 'Homomorphism':
            h2 = True
        else:
            elements_G = list(G.elements) if hasattr(G, 'elements') else list(G)
            elements_A = list(A.elements) if hasattr(A, 'elements') else list(A)
            
            h2 = True
            for x in elements_G:
                fx = f(x) if callable(f) else f[x]
                if fx not in elements_A:
                    h2 = False
                    break
                    
            if h2:
                for x in elements_G:
                    for y in elements_G:
                        fx = f(x) if callable(f) else f[x]
                        fy = f(y) if callable(f) else f[y]
                        try:
                            xy = x * y
                        except Exception:
                            xy = x + y
                        fxy = f(xy) if callable(f) else f[xy]
                        
                        try:
                            fxfy = fx * fy
                        except Exception:
                            fxfy = fx + fy
                            
                        if fxy != fxfy:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails
    try:
        neg_q = False
        
        G_is_group = True
        identity_G = None
        if isinstance(G, PermutationGroup):
            G_is_group = True
            identity_G = G.identity
        else:
            elements_G = list(G.elements) if hasattr(G, 'elements') else list(G)
            for e in elements_G:
                is_id = True
                for x in elements_G:
                    try:
                        xe = x * e
                        ex = e * x
                    except Exception:
                        xe = x + e
                        ex = e + x
                    if xe != x or ex != x:
                        is_id = False
                        break
                if is_id:
                    identity_G = e
                    break
            if identity_G is None:
                G_is_group = False
            else:
                for x in elements_G:
                    has_inv = False
                    for y in elements_G:
                        try:
                            xy = x * y
                            yx = y * x
                        except Exception:
                            xy = x + y
                            yx = y + x
                        if xy == identity_G and yx == identity_G:
                            has_inv = True
                            break
                    if not has_inv:
                        G_is_group = False
                        break
                        
        if not G_is_group:
            # If G is not a group, G/G' is undefined, so the conclusion fails
            neg_q = True
        else:
            commutators = []
            if hasattr(G, 'derived_subgroup'):
                commutators = G.derived_subgroup().generators
            else:
                for x in elements_G:
                    for y in elements_G:
                        try:
                            x_inv = None
                            y_inv = None
                            for z in elements_G:
                                try:
                                    xz = x * z
                                    zx = z * x
                                except Exception:
                                    xz = x + z
                                    zx = z + x
                                if xz == identity_G and zx == identity_G:
                                    x_inv = z
                                try:
                                    yz = y * z
                                    zy = z * y
                                except Exception:
                                    yz = y + z
                                    zy = z + y
                                if yz == identity_G and zy == identity_G:
                                    y_inv = z
                            try:
                                comm = x * y * x_inv * y_inv
                            except Exception:
                                comm = x + y + x_inv + y_inv
                            commutators.append(comm)
                        except Exception:
                            pass
                            
            identity_A = None
            if isinstance(A, PermutationGroup):
                identity_A = A.identity
            else:
                elements_A = list(A.elements) if hasattr(A, 'elements') else list(A)
                for e in elements_A:
                    is_id = True
                    for x in elements_A:
                        try:
                            xe = x * e
                            ex = e * x
                        except Exception:
                            xe = x + e
                            ex = e + x
                        if xe != x or ex != x:
                            is_id = False
                            break
                    if is_id:
                        identity_A = e
                        break
                    
            if identity_A is not None:
                for g in commutators:
                    fg = f(g) if callable(f) else f[g]
                    if fg != identity_A:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an abelian group",
    "H_2: f is a group homomorphism from G to A",
    "¬Q: There does not exist a unique group homomorphism \\tilde{f}: G/G' \\to A such that f = \\tilde{f} \\circ \\pi"
]

N_HYP = 2
NEG_Q_INDEX = 2