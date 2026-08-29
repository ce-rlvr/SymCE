import itertools

# Top-level setup
# The witness is expected to be a dictionary representing a monomial ideal in a free algebra.
# Variables and generators should be represented as strings (e.g., 'x', 'xx', 'xy').
# Example witness:
# witness = {
#     'variables': ['x', 'y'],
#     'I_gens': ['xx', 'yy'],
#     'radical_gens': ['x', 'y']
# }

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, dict):
            return [False, False, False]
            
        variables = witness.get('variables', [])
        I_gens = witness.get('I_gens', [])
        radical_gens = witness.get('radical_gens', [])
        
        if not variables or not isinstance(variables, list):
            return [False, False, False]
            
        if not all(isinstance(v, str) and len(v) == 1 for v in variables):
            return [False, False, False]
            
        # H1: I is an ideal in R
        h1 = True
        if not isinstance(I_gens, list) or len(I_gens) == 0:
            h1 = False
        else:
            for g in I_gens:
                if not isinstance(g, str) or not all(c in variables for c in g):
                    h1 = False
                    break
                    
        # H2: \sqrt{I} is finitely generated
        h2 = False
        if isinstance(radical_gens, list) and set(radical_gens) == set(variables):
            h2 = True
            for v in variables:
                has_power = False
                for g in I_gens:
                    if len(g) > 0 and all(c == v for c in g):
                        has_power = True
                        break
                if not has_power:
                    h2 = False
                    break
                    
        # neg_Q: There is NO positive integer n such that (\sqrt{I})^n \subseteq I
        neg_q = False
        if h1 and h2:
            max_len = max((len(g) for g in I_gens), default=0)
            if max_len == 1:
                neg_q = any(v not in I_gens for v in variables)
            elif max_len > 1:
                states = []
                for p in itertools.product(variables, repeat=max_len - 1):
                    word = "".join(p)
                    if not any(g in word for g in I_gens):
                        states.append(word)
                        
                graph = {s: [] for s in states}
                for s in states:
                    for v in variables:
                        new_word = s + v
                        if not any(g in new_word for g in I_gens):
                            next_state = new_word[1:]
                            if next_state in graph:
                                graph[s].append(next_state)
                                
                visited = set()
                rec_stack = set()
                
                def dfs(node):
                    visited.add(node)
                    rec_stack.add(node)
                    for neighbor in graph.get(node, []):
                        if neighbor not in visited:
                            if dfs(neighbor):
                                return True
                        elif neighbor in rec_stack:
                            return True
                    rec_stack.remove(node)
                    return False
                    
                for s in states:
                    if s not in visited:
                        if dfs(s):
                            neg_q = True
                            break
                            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal in R",
    "H_2: The radical \\sqrt{I} is a finitely generated ideal",
    "¬Q: There is NO positive integer n such that (\\sqrt{I})^n \\subseteq I"
]

N_HYP = 2
NEG_Q_INDEX = 2