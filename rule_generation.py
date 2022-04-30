# Imitating a Naive Bayes ML Model For Probabilistic Prediction
import json
import numpy as np

META_DATA = {}

####### PRETTY PRINTING PURPOSES ##########
def pretty_print(array):
    for i in range(len(array)):
        for j in range(len(array[i])):
            print(array[i][j], end=" ")
        print("")

def pretty_print_array_dict(array_dict):
    for i in range(len(array_dict)):
        print(array_dict[i])

def pretty_print_dict(dict):
    for key, value in dict.items():
        print(key, value)


# assigns an index for fieldName 
def assign_index_based_on_field(field):
    if field in fieldName:
        return fieldName.index(field)
    else:
        print(f"UNKNOWN FIELDNAME ENCOUNTERED: {field}")
        exit(code=1)


# seperates targetValue, cdacFunction ... fieldPosition for calculation
# then calls for a corresponding baeysian frequency table
def segregate_attributes(field, attribute, value):
    row = assign_index_based_on_field(field)

    if attribute == "targetValue":
        value = value[0]
        targetValue[row].append(value)
        generate_bayesian_frequency_table(field, row, value, b_f_targetValue)

    elif attribute == "cdactionFunction":
        cdactionFunction[row].append(value)
        generate_bayesian_frequency_table(field, row, value, b_f_cdactionFunction)

    elif attribute == "matchingOperator":
        value = value["type"]
        matchingOperator[row].append(value)
        generate_bayesian_frequency_table(field, row, value, b_f_matchingOperator)

    elif attribute == "fieldLength":
        fieldLength[row].append(value)
        generate_bayesian_frequency_table(field, row, value, b_f_fieldLength)

    elif attribute == "direction":
        direction[row].append(value)
        generate_bayesian_frequency_table(field, row, value, b_f_direction)

    elif attribute == "fieldPosition":
        fieldPosition[row].append(value)
        generate_bayesian_frequency_table(field, row, value, b_f_fieldPosition)

    else:
        print(f"OUT OF CONTEXT ATTRIBUTE FOUND {attribute}")
        exit(code=1)


# generating bayesian frequency table
def generate_bayesian_frequency_table(field, row, value, b_f_table):
    if len(b_f_table[row]) == 0 or value not in b_f_table[row].keys():
        b_f_table[row][value] = 1
    else:
        increment_freq = b_f_table[row][value] + 1
        b_f_table[row].update({value: increment_freq})
    

# computes naive bayes probability per attribute from the bayesian freq table
# P(IP4_vERSION | targetVariable=4) .... P(IP4_vERSION | fieldPosition=1)
def compute_naive_bayes_probability(b_f_table):
    for index, field_wise_meta in enumerate(b_f_table):
        for key, value in field_wise_meta.items():
            prob_of_attribute = field_wise_meta[key] / META_DATA[f'{fieldName[index]}_NOS']
            prob_of_choosing_attribute_given_field_name = prob_of_attribute * (1/len(fieldName))
            field_wise_meta[key] = prob_of_choosing_attribute_given_field_name


# a helper function to sort the b_f_table according to their decreasing
# naive bayes probability
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
    
    return COMBINATION_MATRIX

# Parse the obtained Naive Bayes values into rules
def parse_predicted_rule(best_rule):
    RULE = []

    for i in range(len(fieldName)):
        dict = {"fieldName": fieldName[i]}
        RULE.append(dict)
    
    for row in range(len(best_rule)):
        for i in range(len(fieldName)):
            dict = {"fieldName": fieldName[i]}
            if row == 0:
                RULE[i]['targetValue'] = [best_rule[row][i]]
            elif row == 1:
                RULE[i]['cdactionFunction'] = best_rule[row][i]
            elif row == 2:
                RULE[i]['matchingOperator'] = parse_matching_operator(best_rule, row, i)
            elif row == 3:
                RULE[i]['fieldLength'] = best_rule[row][i]
            elif row == 4:
                RULE[i]['direction'] = best_rule[row][i]
            elif row == 5:
                RULE[i]['fieldPosition'] = best_rule[row][i]

            else:
                raise IndexError('Definitely, some problem with the parse logic')

    return RULE


def parse_matching_operator(best_rule, row, i):
    return {"type": best_rule[row][i]}


fieldName = [
    "IP4_VERSION",
    "IP4_IHL", 
    "IP4_TOS", 
    "IP4_LENGTH", 
    "IP4_ID", 
    "IP4_FLAGS", 
    "IP4_FRAG_OFFSET", 
    "IP4_TTL", 
    "IP4_PROTOCOL", 
    "IP4_CHECKSUM", 
    "IP4_DEV_IP", 
    "IP4_APP_IP", 
    "UDP_DEV_PORT", 
    "UDP_APP_PORT", 
    "UDP_LENGTH", 
    "UDP_CHECKSUM", 
    ]

# collecting some METADATA about the fields like: Number of IP4_VERSION fields
# we will require METADATA to calculate the Naive Bayes Probability.
for field in fieldName:
    META_DATA[f'{field}_NOS'] = 0

# attribute tables
targetValue = [ [] for i in fieldName]
cdactionFunction = [ [] for i in fieldName]
matchingOperator = [ [] for i in fieldName]
fieldLength = [ [] for i in fieldName]
direction = [ [] for i in fieldName]
fieldPosition = [ [] for i in fieldName]

# bayesian frequency tables
b_f_targetValue = [ {} for i in fieldName]
b_f_cdactionFunction = [ {} for i in fieldName]
b_f_matchingOperator = [ {} for i in fieldName]
b_f_fieldLength = [ {} for i in fieldName]
b_f_direction = [ {} for i in fieldName]
b_f_fieldPosition = [ {} for i in fieldName]

# combination of b_f_tables. would be highly helpful while parsing our own
# rules from the rule attributes.
B_F_TABLES = [
    b_f_targetValue,
    b_f_cdactionFunction,
    b_f_matchingOperator,
    b_f_fieldLength,
    b_f_direction,
    b_f_fieldPosition
      ]


################# ENTRY-POINT OF THE PROGRAM ###################

# opening the json file in read mode. 
with open('SCHC\\config_rules-SCHCnoSec-v06-comments.json', 'r') as f:
    data = json.load(f)

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


# We now have a bayesian frequency table generated.
# Lets update the table with the NAIVE-BAYESIAN PROBABILITY:
# NOTE: BAYESIAN PROB = P(A|B,C) = P(B|A)*P(C|A)*P(A)
# Therefore: P(IP4_VERSION|T_V=4) = P(T_V=4|IP4_VERSION)*P(IP4_VERSION)
# To maintain the equally likelihood theorem, we hold the assumption that

for b_f_table in B_F_TABLES:
    compute_naive_bayes_probability(b_f_table)


# Producing the most apt combinations:
best_rule = generate_rule_by_naive_bayesian_combinations(B_F_TABLES)

# Parse the rule 
parsed_rule = parse_predicted_rule(best_rule)

# JSONIFY the rule and write it out to a file
json_pretty_rule = json.dumps(parsed_rule, indent=3)
print(json_pretty_rule)

##################### END OF PROGRAM (DEBUGGING STUFFS) #####################

# TABLE STRUCTURE:
# [   ATTRIBUTES -->      TARGET_VARIABLE,    CDACFUNCTION,   ... FIELDPOSITION
#     FIELDNAMES   
#         | (IP4_VERSION)      4                  NotSent               1
#         V (IP4_IHL)          0                  Ignore                1
#                 .
#                 .
#                 .
# ]


# pretty_print(matchingOperator)
# pretty_print_array_dict(b_f_targetValue)

# print(b_f_targetValue)
# print(b_f_cdactionFunction)

# pretty_print_array_dict(b_f_targetValue)
