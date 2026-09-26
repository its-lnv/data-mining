import pandas as pd

# -------------------------------------------------
# TRANSACTIONAL DATASET
# -------------------------------------------------

transactions = [
    ['Laptop', 'Mouse', 'Laptop Bag'],
    ['Laptop', 'Keyboard', 'Mouse'],
    ['Mobile', 'Charger', 'Earphones'],
    ['Laptop', 'Mouse', 'Keyboard', 'Laptop Bag'],
    ['Mobile', 'Charger', 'Screen Guard'],
    ['Laptop', 'Laptop Bag', 'Mouse'],
    ['Mobile', 'Earphones', 'Screen Guard'],
    ['Laptop', 'Keyboard', 'Mouse', 'Mouse Pad'],
    ['Mobile', 'Charger', 'Earphones', 'Screen Guard'],
    ['Laptop', 'Mouse', 'Mouse Pad']
]


# -------------------------------------------------
# GIVEN ITEMSETS
# -------------------------------------------------

itemsets = [
    {'Laptop'},
    {'Mouse'},
    {'Mobile'},
    {'Laptop', 'Mouse'},
    {'Mobile', 'Charger'},
    {'Laptop', 'Mouse', 'Keyboard'}
]


# -------------------------------------------------
# GIVEN ASSOCIATION RULES
# -------------------------------------------------

rules = [
    ({'Laptop'}, {'Mouse'}),
    ({'Mobile'}, {'Charger'}),
    ({'Laptop', 'Mouse'}, {'Keyboard'}),
    ({'Charger'}, {'Mobile'})
]


# -------------------------------------------------
# FUNCTION TO CALCULATE SUPPORT
# -------------------------------------------------

def support(itemset):
    count = 0

    for transaction in transactions:
        if itemset.issubset(set(transaction)):
            count += 1

    return count / len(transactions) * 100


# -------------------------------------------------
# Q1. SUPPORT OF ALL ITEMSETS
# -------------------------------------------------

itemset_results = []

for itemset in itemsets:

    count = 0

    for transaction in transactions:
        if itemset.issubset(set(transaction)):
            count += 1

    sup = count / len(transactions) * 100

    itemset_results.append([
        ', '.join(sorted(itemset)),
        count,
        round(sup, 2)
    ])


itemset_table = pd.DataFrame(
    itemset_results,
    columns=[
        'Itemset',
        'Transaction Count',
        'Support (%)'
    ]
)


print("\n==========================================")
print("Q1. SUPPORT OF ALL ITEMSETS")
print("==========================================")

print(itemset_table.to_string(index=False))


# -------------------------------------------------
# Q2. SUPPORT AND CONFIDENCE OF RULES
# -------------------------------------------------

rule_results = []

for antecedent, consequent in rules:

    # Support of antecedent
    antecedent_support = support(antecedent)

    # Support of consequent
    consequent_support = support(consequent)

    # Support of combined itemset
    combined = antecedent.union(consequent)
    combined_support = support(combined)

    # Confidence = Support(A U B) / Support(A)
    confidence = (
        combined_support / antecedent_support
    ) * 100

    rule_results.append([
        ', '.join(sorted(antecedent)),
        ', '.join(sorted(consequent)),
        round(combined_support, 2),
        round(confidence, 2)
    ])


rule_table = pd.DataFrame(
    rule_results,
    columns=[
        'Antecedent',
        'Consequent',
        'Support (%)',
        'Confidence (%)'
    ]
)


print("\n==========================================")
print("Q2. SUPPORT AND CONFIDENCE OF RULES")
print("==========================================")

print(rule_table.to_string(index=False))