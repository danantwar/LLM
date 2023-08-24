import json

# Provided JSON array of element names
json_array = [
    "Infrastructure Change ID",
    "Description",
    "Detailed Description",
    "Categorization Tier 1",
    "Categorization Tier 2",
    "Categorization Tier 3",
    "Product Cat Tier 1",
    "Product Cat Tier 2",
    "Product Cat Tier 3"
]

# Generate the formatted strings for each element
formatted_strings = [
    f"{element} : {json_array[element]}"
    for element in json_array
]

# Print the formatted strings
for formatted_string in formatted_strings:
    print(formatted_string)