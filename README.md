# SCHC Rule Generation With Naive Bayes
###### Generating a Static Context Header Compression Rule from Naive Bayes Probabiilty.

### *What is Naive Bayes?*
Naive Bayes is branched off of the famous Bayes Theorem. It assumes independence among each attributes. Also, the calculations are super simplified as compared to Bayes, hence it is highly computationally efficient.

![Naive Base Fromula](https://i.imgur.com/3cl5oDz.png)

### *Why Naive Bayes for SCHC Rule Generation?*
Over any IOT network, it is highly expected that packet traces repeat. Therefore, rule generation over here is a highly probabilistic task since any recurrent task has certain probabilities associated with it. Also, it is no good to draw a correlation between each attributes since each rule attributes are independent of each other. For this reason, Bayes is outed for Naive Bayes. 

Naive Bayes specializes in probabilistic prediction and is widely used for such tasks. It is known to predict recurrent patterns with a high probabilstic accuracy. Although Naive Bayes is used for classification purposes, but the underlying principle can be modified to suit any patterns which favours probability. Rule generation is one such task.

## The Methodology
The Rule Generation is briefly dissected into 6 parts:
- JSON Walk
- Segregation
- Generate Bayesian Frequency Table
- Compute Naive Bayes for Each Rule Attribute
- Generate the Rule

### *JSON Walk*
Here, we walk the JSON file and pick up the desired attributes from the entire Static Header Context.

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
