import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings that the witness expression may reference.
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

x, y, z = sympy.symbols('x y z', commutative=False)

def conditions(witness):
    try:
        G, u, v = witness
    except Exception:
        return [False, False]
        
    def get_letters(w):
        if w == 1:
            return []
        letters = []
        if isinstance(w, sympy.Mul):
            args = w.args
        else:
            args = [w]
        for arg in args:
            if isinstance(arg, sympy.Pow):
                base, exp = arg.base, arg.exp
                if exp > 0:
                    letters.extend([base] * int(exp))
                else:
                    letters.extend([base**-1] * int(-exp))
            elif isinstance(arg, sympy.Symbol):
                letters.append(arg)
            else:
                raise ValueError("Invalid word")
        return letters

    def is_cyclically_reduced(w):
        try:
            letters = get_letters(w)
            if len(letters) <= 1:
                return True
            first = letters[0]
            last = letters[-1]
            if first * last == 1:
                return False
            return True
        except Exception:
            return False
        
    try:
        h1_ok = is_cyclically_reduced(u) and is_cyclically_reduced(v)
    except Exception:
        h1_ok = False
        
    try:
        if not isinstance(G, PermutationGroup):
            neg_q_ok = False
        elif G.order() > 10000:
            neg_q_ok = False
        else:
            gens = G.generators
            sym_to_idx = {x: 0, y: 1, z: 2}
            
            def eval_word(w):
                if not gens:
                    return Permutation()
                p = gens[0] ** 0
                
                letters = get_letters(w)
                for let in letters:
                    if isinstance(let, sympy.Pow):
                        base = let.base
                        exp = -1
                    else:
                        base = let
                        exp = 1
                        
                    if base not in sym_to_idx:
                        return None
                    idx = sym_to_idx[base]
                    if idx >= len(gens):
                        return None
                        
                    g = gens[idx]
                    if exp == -1:
                        g = ~g
                        
                    p = p * g
                return p
                
            u_val = eval_word(u)
            v_val = eval_word(v)
            
            if u_val is None or v_val is None:
                neg_q_ok = False
            else:
                are_conjugate = False
                for g in G.elements:
                    if ~g * u_val * g == v_val:
                        are_conjugate = True
                        break
                        
                u_let = get_letters(u)
                v_let = get_letters(v)
                
                is_cyclic = False
                if len(u_let) == len(v_let):
                    if len(u_let) == 0:
                        is_cyclic = True
                    else:
                        n = len(u_let)
                        for i in range(n):
                            if u_let[i:] + u_let[:i] == v_let:
                                is_cyclic = True
                                break
                                
                neg_q_ok = (are_conjugate != is_cyclic)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: u and v are cyclically reduced words in F",
    "¬Q: u and v are conjugate in F iff u is a cyclic permutation of v (fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1