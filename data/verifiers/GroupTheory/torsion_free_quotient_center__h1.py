import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import Matrix, eye, zeros

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
    "H_1: G is a torsion-free group",
    "¬Q: The quotient group G/Z(G) is not torsion-free"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    # 1. Custom class with methods
    try:
        if hasattr(witness, 'is_torsion_free') and hasattr(witness, 'center_quotient_has_torsion'):
            h1 = bool(witness.is_torsion_free())
            neg_q = bool(witness.center_quotient_has_torsion())
            if h1 and neg_q:
                return [h1, neg_q]
    except Exception:
        pass

    # 2. FpGroup (Finitely Presented Group)
    try:
        if type(witness).__name__ == 'FpGroup':
            gens = witness.generators
            rels = witness.relators
            if len(gens) == 2 and len(rels) == 1:
                x, y = gens
                rel = rels[0]
                
                def word_len(w):
                    return sum(abs(power) for g, power in w.array_form)

                def exp_sum(w, gen):
                    return sum(power for g, power in w.array_form if g == gen)

                def get_letters(w):
                    letters = []
                    for g, power in w.array_form:
                        sign = 1 if power > 0 else -1
                        for _ in range(abs(power)):
                            letters.append((g, sign))
                    return letters

                def is_cyclic_perm(w1, w2):
                    l1 = get_letters(w1)
                    l2 = get_letters(w2)
                    if len(l1) != len(l2): return False
                    for i in range(len(l1)):
                        if l1 == l2[i:] + l2[:i]:
                            return True
                    return False

                # Case A: u^a v^b = 1 (Torus knot groups and similar amalgamated products)
                if len(rel.array_form) == 2:
                    (g1, a), (g2, b) = rel.array_form
                    if g1 != g2 and abs(a) >= 2 and abs(b) >= 2:
                        h1 = True
                        neg_q = True
                        return [h1, neg_q]
                        
                # Case B: x y x^-1 y = 1 (Klein bottle group)
                exp_x = exp_sum(rel, x)
                exp_y = exp_sum(rel, y)
                exps = sorted([abs(exp_x), abs(exp_y)])
                if exps == [0, 2] and word_len(rel) == 4:
                    h1 = True
                    neg_q = True
                    return [h1, neg_q]
                    
                # Case C: Braid group B3 (x y x y^-1 x^-1 y^-1 = 1)
                b3_word = x * y * x * y**-1 * x**-1 * y**-1
                if is_cyclic_perm(rel, b3_word) or is_cyclic_perm(rel**-1, b3_word):
                    h1 = True
                    neg_q = True
                    return [h1, neg_q]
    except Exception:
        pass

    # 3. Matrix group
    try:
        gens = None
        if hasattr(witness, 'generators'):
            gens = witness.generators
        elif isinstance(witness, (list, tuple)):
            gens = witness
            
        if gens is not None and len(gens) == 2:
            X, Y = gens
            if hasattr(X, 'inv') and hasattr(Y, 'inv') and X.shape == Y.shape:
                I = eye(X.shape[0])
                # Check Klein bottle relations
                rel1 = (X * Y * X.inv() == Y.inv())
                rel2 = (Y * X * Y.inv() == X.inv())
                if (rel1 or rel2) and (X * Y != Y * X):
                    torsion_free = True
                    for k in range(1, 15):
                        if X**k == I or Y**k == I:
                            torsion_free = False
                            break
                    if torsion_free:
                        h1 = True
                        neg_q = True
                        return [h1, neg_q]
    except Exception:
        pass

    return [h1, neg_q]