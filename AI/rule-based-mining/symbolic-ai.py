import pandas as pd
from mlxtend.frequent_patterns import apriori, fpmax, fpgrowth
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder


### QUESTION 2:

# for both datasets
def read_dataset (d):
  if d == 0:
    return [['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
           ['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
           ['Milk', 'Apple', 'Kidney Beans', 'Eggs'],
           ['Milk', 'Unicorn', 'Corn', 'Kidney Beans', 'Yogurt'],
           ['Corn', 'Onion', 'Onion', 'Kidney Beans', 'Ice cream', 'Eggs']]
  elif d == 1:
    file_name = "credit-german.txt"
  elif d == 2:
    file_name = "habitudes_de_vie.csv"
  lines = [line.strip().split("\t") for line in open(file_name).readlines()]
  header = lines[0]
  return [ [header[i] + " " + val[i] for i in range(len(header)) ] for val in lines[1:]]


### file :  credit-german.txt 

# (0) example from mlxtend tutorial or (1) credit-german.txt or (2) habitudes_de_vie.csv
dataset = read_dataset(1)
########################################################
#Generating Frequent Itemsets
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
#Working with Sparse Representations
oht_ary = te.fit(dataset).transform(dataset, sparse=True)
sparse_df = pd.DataFrame.sparse.from_spmatrix(oht_ary, columns=te.columns_)
########################################################
# Generating Association Rules from Frequent Itemsets
frequent_itemsets = apriori(sparse_df, min_support=0.4, use_colnames=True)
new_itemsets = frequent_itemsets[(frequent_itemsets['itemsets'].apply(lambda x: len(x) == 1)) & frequent_itemsets['support'].apply(lambda x:  x > 0.9)]
# commande   : print(new_itemsets)
# it gives : foreign_worker yes  and other_parties none
# we should keep that in mind
rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.5)
#our goal is to give rules that give as a consequence a class good or bad 
rules_2 =  rules[(rules["consequents"] == {'class good'} )| (rules["consequents"] == {'class good'})]
# we filter what the rules using confidence and lift 
rules_3 = rules_2[(rules_2["confidence"] > 0.7) & (rules_2["lift"] > 1)]
# We get the following rules :
# command used : print(rules_3[["antecedents", "consequents"]])
"""
housing own - > class good
other_parties none - > class good
other_payment_plans none - > class good
housing own, foreign_worker yes - > class good
foreign_worker yes, other_payment_plans none - > class good
num_dependents one, other_parties none - > class good
num_dependents one, other_payment_plans none - >   class good
other_parties none, other_payment_plans none  - > class good
other_parties none, foreign_worker yes, other_parties none  - > class good


but the ones that make sense are :
housing own - > class good
num_dependents one, other_parties none - > class good
num_dependents one, other_payment_plans none - >   class good
other_parties none, other_payment_plans none  - > class good
"""




### file  : habitudes_de_vie.csv

dataset = read_dataset(2)
########################################################
#Generating Frequent Itemsets
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
#Working with Sparse Representations
oht_ary = te.fit(dataset).transform(dataset, sparse=True)
sparse_df = pd.DataFrame.sparse.from_spmatrix(oht_ary, columns=te.columns_)
########################################################
# Generating Association Rules from Frequent Itemsets
frequent_itemsets = apriori(sparse_df, min_support=0.2, use_colnames=True)
# By trying multiple values of the support , 0.2 seems reasonable 
rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.2)
# now we filter using confidence and lift 
rules_2 = rules[(rules['confidence'] > 0.5) & (rules['lift'] > 1)][["antecedents", "consequents"]]
print(rules_2)
"""
we get the following  rules :
ACTIVITESPORT DAILY - > HAB_BOISSON REGULAR
ACTIVITESPORT DAILY - > TYPELAIT 2%MILK
FUMER FORMER - > HAB_BOISSON REGULAR
FUMER FORMER - > TYPELAIT 2%MILK
TYPELAIT 2%MILK   - > HAB_BOISSON REGULAR
HAB_BOISSON REGULAR   - > TYPELAIT 2%MILK
SELALIMENT NONE  - > TYPELAIT 2%MILK
SELALIMENT VERYLITTLE   - > TYPELAIT 2%MILK
"""


