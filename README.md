# SCHC Rule Generation With Naive Bayes
###### Generating a Static Context Header Compression Rule from Naive Bayes Probabiilty.

### *What is Naive Bayes?*
Naive Bayes is branched off of the famous **Bayes Theorem**. It assumes independence among each attributes. Also, the calculations are super simplified as compared to Bayes, hence it is highly **computationally efficient**.

![Naive Base Fromula](https://i.imgur.com/3cl5oDz.png)

### *Why Naive Bayes for SCHC Rule Generation?*
Over any IOT network, it is highly expected that **packet traces repeat**. Therefore, rule generation over here is a **highly probabilistic task** since any recurrent task has certain probabilities associated with it. Also, it is not good to draw a correlation between each attributes since each rule attributes are independent of each other. For this reason, Bayes is outed for Naive Bayes. 

Naive Bayes specializes in probabilistic prediction and is widely used for such tasks. It is known to predict recurrent patterns with a high probabilstic accuracy. Although Naive Bayes is used for classification purposes, but the underlying principle can be modified to suit any patterns which favours probability. Rule generation is one such task.

## The Methodology
The Rule Generation is briefly dissected into 5 parts:
- **_JSON Walk_**
- **_Segregation_**
- **_Generate Bayesian Frequency Table_**
- **_Compute Naive Bayes for Each Rule Attribute_**
- **_Generate the Rule_**

### *JSON Walk*
Here, we walk the JSON file and pick up the desired attributes from the entire Static Header Context. Then call a `segregate_attribute` API for each field and its respective attribute.

```python
# Walk the json file and collect the fieldname and the corresponding attributes
for rule in data["rules"]:
    for flow in rule["flows"]:
        for entry in flow["ruleEntries"]:
            if not entry["fieldName"].lower().startswith("coap"):
                field = entry["fieldName"]
                META_DATA[f'{field}_NOS'] += 1
                for attribute, value in entry.items():
                    if attribute != "fieldName":
                        segregate_attributes(field, attribute, value)
```

### *Segregation*
Each attribute is segregated on the basis of the fields. Example: **`IP4_ADDRESS`** attributes are: *`fieldLength, cdactionFunction .. fieldPosition`*

```python
# then calls for a corresponding baeysian frequency table
def segregate_attributes(field, attribute, value):
    row = assign_index_based_on_field(field)

    if attribute == "targetValue":
        value = value[0]
        targetValue[row].append(value)
        generate_bayesian_frequency_table(field, row, value, b_f_targetValue)

    elif attribute == "cdactionFunction":
    # .
    # .
    # .
```
Then for each attribute, it triggers the `generate_bayesian_frequencey_table`.

### *Generate Bayesian Frequency Table*
The `generate_bayesian_frequencey_table` computes the frequency table by keeping a track of all the occurence of the attribute values. These tables will be highly useful while computing Naive Bayes Probability.

```python
# generating bayesian frequency table
def generate_bayesian_frequency_table(field, row, value, b_f_table):
    if len(b_f_table[row]) == 0 or value not in b_f_table[row].keys():
        b_f_table[row][value] = 1
    else:
        increment_freq = b_f_table[row][value] + 1
        b_f_table[row].update({value: increment_freq})
```

### *Compute Naive Bayes*
This function computes the NB probability from the data obtained from `generate_bayesian_frequency_table` and certain `METADATA` collected about the rules while Walking JSON

```python
# computes naive bayes probability per attribute from the bayesian freq table
# P(IP4_vERSION | targetVariable=4) .... P(IP4_vERSION | fieldPosition=1)
def compute_naive_bayes_probability(b_f_table):
    for index, field_wise_meta in enumerate(b_f_table):
        for key, value in field_wise_meta.items():
            prob_of_attribute = field_wise_meta[key] / META_DATA[f'{fieldName[index]}_NOS']
            prob_of_choosing_attribute_given_field_name = prob_of_attribute * (1/len(fieldName))
            field_wise_meta[key] = prob_of_choosing_attribute_given_field_name
```

### *Generate Rule*
The rule is finally generated by sorting out the best probable attributes per fieldName. This is done with the help of a helper function `sort_b_f_table_by_probability`

```python
# generates the best rule from naive bayes probabilites.
# after sorting the b_f_table, pick up the first element
# from each attribute. This is the element with highest probability.
def generate_rule_by_naive_bayesian_combinations(B_F_TABLES):
    for b_f_table in B_F_TABLES:
        sort_b_f_table_by_probability(b_f_table)
    
    COMBINATION_MATRIX = [ [] for i in range(len(B_F_TABLES)) ]
    
    # TODO: CREATE A COMBINATION OF BAYESIAN PROBABILITES
    for i in range(len(B_F_TABLES)):
        for element in B_F_TABLES[i]:
            for key, value in element.items():
                COMBINATION_MATRIX[i].append(key)
                break
    
    # print the rules
    print(COMBINATION_MATRIX)
```

The helper function used:
```python
def sort_b_f_table_by_probability(b_f_table):
    for i in range(len(b_f_table)):
        dict = b_f_table[i]

        sorted_values = sorted(dict.values(), reverse=True)
        new_dict = {}

        for value in sorted_values:
            for key, values in dict.items():
                if dict[key] == value:
                    new_dict[key] = dict[key]
                    break
        b_f_table[i] = new_dict
```
The scope here is that we can generate multiple rules based on decreasing probability. This can lead to much diverse rule generation. As it is evident that, all the `COMBINATION_MATRIX` is doing right now, is generating the best probable rule from the rules it learnt.
