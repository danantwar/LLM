import json

# Provided JSON
json_data = {
    "entries": [
        {
            "values": {
                "Ticket Number": "000000024525",
                "Description": "Issue",
                "Detailed Description": "abcd",
                "Closure Product Category Tier1": "a",
                "Closure Product Category Tier2": "b",
                "Closure Product Category Tier3": "c"
            },
            "_links": {
                "self": [
                    {
                        "href": "https://abc.com"
                    }
                ]
            }
        }
    ],
    "_links": {
        "next": [
            {
                "href": "https://abc.com"
            }
        ],
        "self": [
            {
                "href": "https://abc.com"
            }
        ]
    }
}

# Extract values from the JSON
entries = json_data.get("entries", [])
result_text = ""

# Iterate through entries and their values
for entry in entries:
    values = entry.get("values", {})
    for key, value in values.items():
        result_text += f"{key}: {value},\n"

# Print the generated text output
print(result_text)
