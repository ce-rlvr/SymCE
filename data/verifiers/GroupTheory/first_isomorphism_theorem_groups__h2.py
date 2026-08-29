import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation

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
        G, H, phi = witness
    except Exception:
        return [False, False]

    # H_1: G and H are groups and phi is a map from G to H
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
        if h1:
            if isinstance(phi, dict):
                domain_ok = set(phi.keys()) == set(G.elements)
                codomain_ok = all(v in H.elements for v in phi.values())
                h1 = domain_ok and codomain_ok
            elif callable(phi):
                codomain_ok = all(phi(g) in H.elements for g in G.elements)
                h1 = codomain_ok
            else:
                h1 = False
    except Exception:
        h1 = False

    # neg_Q: The quotient group G/ker(phi) is not isomorphic to the subgroup phi(G) of H
    try:
        def eval_phi(g):
            if isinstance(phi, dict):
                return phi[g]
            return phi(g)

        G_elements = list(G.elements)
        H_elements = list(H.elements)
        e_H = H.identity

        ker_phi = [g for g in G_elements if eval_phi(g) == e_H]

        def is_subgroup(subset, group):
            if not subset: return False
            if group.identity not in subset: return False
            subset_set = set(subset)
            for a in subset:
                for b in subset:
                    if a * b not in subset_set:
                        return False
            return True

        def is_normal_subgroup(subset, group):
            if not is_subgroup(subset, group): return False
            subset_set = set(subset)
            for h in subset:
                for g in G_elements:
                    if g * h * (~g) not in subset_set:
                        return False
            return True

        if not is_normal_subgroup(ker_phi, G):
            neg_q = True
        else:
            im_phi = list(set(eval_phi(g) for g in G_elements))
            if not is_subgroup(im_phi, H):
                neg_q = True
            else:
                if len(G_elements) // len(ker_phi) != len(im_phi):
                    neg_q = True
                else:
                    im_phi.remove(e_H)
                    im_phi = [e_H] + im_phi

                    def op_im(x, y):
                        return x * y

                    cosets = []
                    for g in G_elements:
                        coset = frozenset(g * k for k in ker_phi)
                        if coset not in cosets:
                            cosets.append(coset)

                    id_coset = frozenset(ker_phi)
                    cosets.remove(id_coset)
                    cosets = [id_coset] + cosets

                    def op_coset(c1, c2):
                        g1 = next(iter(c1))
                        g2 = next(iter(c2))
                        prod = g1 * g2
                        return frozenset(prod * k for k in ker_phi)

                    def get_mult_table(elements, op):
                        n = len(elements)
                        table = []
                        for i in range(n):
                            row = []
                            for j in range(n):
                                prod = op(elements[i], elements[j])
                                row.append(elements.index(prod))
                            table.append(row)
                        return table

                    table_im = get_mult_table(im_phi, op_im)
                    table_coset = get_mult_table(cosets, op_coset)

                    def get_orders(table):
                        n = len(table)
                        orders = []
                        for i in range(n):
                            curr = i
                            order = 1
                            while curr != 0:
                                curr = table[curr][i]
                                order += 1
                            orders.append(order)
                        return orders

                    orders_im = get_orders(table_im)
                    orders_coset = get_orders(table_coset)

                    def are_isomorphic(table1, table2, orders1, orders2):
                        n = len(table1)
                        if n != len(table2): return False
                        if sorted(orders1) != sorted(orders2): return False

                        valid_targets = []
                        for i in range(n):
                            valid_targets.append([j for j in range(n) if orders2[j] == orders1[i]])

                        mapping = {}
                        used = set()

                        def backtrack(i):
                            if i == n:
                                return True
                            for j in valid_targets[i]:
                                if j in used:
                                    continue
                                mapping[i] = j
                                ok = True
                                for x in range(i + 1):
                                    for y in range(i + 1):
                                        prod1 = table1[x][y]
                                        if prod1 <= i:
                                            if table2[mapping[x]][mapping[y]] != mapping[prod1]:
                                                ok = False
                                                break
                                    if not ok:
                                        break
                                if ok:
                                    used.add(j)
                                    if backtrack(i + 1):
                                        return True
                                    used.remove(j)
                                del mapping[i]
                            return False

                        return backtrack(0)

                    neg_q = not are_isomorphic(table_coset, table_im, orders_coset, orders_im)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups and phi is a map from G to H",
    "¬Q: The quotient group G/ker(phi) is not isomorphic to the subgroup phi(G) of H"
]

N_HYP = 1
NEG_Q_INDEX = 1