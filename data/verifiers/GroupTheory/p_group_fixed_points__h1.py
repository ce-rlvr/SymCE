import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def parse_witness(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            action_gens = witness.get('action_gens')
            n = witness.get('n')
            if G is None or p is None or action_gens is None or n is None:
                return None
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                G, p, action_gens, n = witness
            elif len(witness) == 2:
                G, p = witness
                action_gens = G.generators
                n = G.degree
            else:
                return None
        else:
            return None
            
        parsed_action_gens = []
        for g in action_gens:
            if isinstance(g, Permutation):
                parsed_action_gens.append(g)
            else:
                parsed_action_gens.append(Permutation(g))
            
        return G, int(p), parsed_action_gens, int(n)
    except Exception:
        return None

def check_action(G, action_gens, n):
    try:
        if len(G.generators) != len(action_gens): 
            return False
        
        # Ensure permutations do not move elements outside the set X of size n
        for g in action_gens:
            if g.size > n:
                for i in range(n, g.size):
                    if g(i) != i:
                        return False
                        
        # Normalize permutations to exactly size n
        norm_gens = [Permutation([g(i) for i in range(n)]) for g in action_gens]
        
        id_X = Permutation([], size=n)
        action_map = {G.identity: id_X}
        queue = [G.identity]
        gens = G.generators
        
        max_order = int(G.order())
        
        # BFS to build and verify the homomorphism from G to Sym(X)
        while queue:
            curr = queue.pop(0)
            curr_act = action_map[curr]
            for g, g_act in zip(gens, norm_gens):
                nxt = curr * g
                nxt_act = curr_act * g_act
                if nxt not in action_map:
                    action_map[nxt] = nxt_act
                    queue.append(nxt)
                    if len(action_map) > max_order:
                        return False
                else:
                    if action_map[nxt] != nxt_act:
                        return False
                        
        return len(action_map) == max_order
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        parsed = parse_witness(witness)
        if parsed is None:
            return [False, False, False, False, False]
        G, p, action_gens, n = parsed
    except Exception:
        return [False, False, False, False, False]
        
    # H_1: G is a finite p-group
    try:
        if p <= 1:
            h1 = False
        else:
            order = int(G.order())
            if order == 1:
                h1 = True
            else:
                while order % p == 0:
                    order //= p
                h1 = (order == 1)
    except Exception:
        h1 = False
        
    # H_2: X is a finite set
    try:
        h2 = isinstance(n, int) and n >= 0
    except Exception:
        h2 = False
        
    # H_3: G acts on X
    try:
        h3 = check_action(G, action_gens, n)
    except Exception:
        h3 = False
        
    # H_4: X^G is the set of all elements in X fixed by every element of G
    # This is a definitional hypothesis, inherently true if the setup is valid.
    h4 = True
    
    # ¬Q: |X^G| is not congruent to |X| modulo p
    try:
        fixed_count = 0
        for x in range(n):
            is_fixed = True
            for g_act in action_gens:
                if g_act(x) != x:
                    is_fixed = False
                    break
            if is_fixed:
                fixed_count += 1
        neg_q = (fixed_count % p) != (n % p)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite p-group",
    "H_2: X is a finite set",
    "H_3: G acts on X",
    "H_4: X^G is the set of all elements in X fixed by every element of G",
    "¬Q: |X^G| is not congruent to |X| modulo p"
]

N_HYP = 4
NEG_Q_INDEX = 4