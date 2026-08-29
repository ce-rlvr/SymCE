import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        if hasattr(witness, 'order') and witness.order() > 1000:
            return [False, False]
    except Exception:
        pass

    try:
        # H_1: G has a trivial center
        elements = list(witness.elements)
        gens = list(witness.generators)
        
        center_size = 0
        for g in elements:
            commutes = True
            for gen in gens:
                if g * gen != gen * g:
                    commutes = False
                    break
            if commutes:
                center_size += 1
        h1_ok = (center_size == 1)
    except Exception:
        h1_ok = False

    try:
        # neg_Q: Aut(G) is not isomorphic to G
        # For a group with a trivial center, G is isomorphic to Inn(G).
        # Thus, Aut(G) is isomorphic to G if and only if |Aut(G)| == |G|.
        elements = list(witness.elements)
        gens = list(witness.generators)
        
        identity = None
        for g in elements:
            if g * g == g:
                identity = g
                break
                
        if identity is None:
            neg_q_ok = False
        else:
            word_of = {}
            word_of[identity] = []
            queue = [identity]
            head = 0
            while head < len(queue):
                curr = queue[head]
                head += 1
                for i, gen in enumerate(gens):
                    nxt = curr * gen
                    if nxt not in word_of:
                        word_of[nxt] = word_of[curr] + [i]
                        queue.append(nxt)
                        
            mult_gen = {g: [g * gen for gen in gens] for g in elements}
            
            def get_order(g):
                p = g
                o = 1
                while p != identity:
                    p = p * g
                    o += 1
                return o
                
            gen_orders = [get_order(gen) for gen in gens]
            valid_imgs = [[g for g in elements if get_order(g) == o] for o in gen_orders]
            
            aut_count = 0
            for imgs in itertools.product(*valid_imgs):
                f = {}
                for g, word in word_of.items():
                    val = identity
                    for idx in word:
                        val = val * imgs[idx]
                    f[g] = val
                    
                if len(set(f.values())) != len(elements):
                    continue
                    
                is_homo = True
                for g in elements:
                    for i in range(len(gens)):
                        if f[mult_gen[g][i]] != f[g] * imgs[i]:
                            is_homo = False
                            break
                    if not is_homo:
                        break
                        
                if is_homo:
                    aut_count += 1
                    
            neg_q_ok = (aut_count != len(elements))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G has a trivial center",
    "¬Q: Aut(G) is not isomorphic to G"
]

N_HYP = 1
NEG_Q_INDEX = 1