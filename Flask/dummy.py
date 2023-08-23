import json
json = {
    "entries": [
        {
            "values": {
                "Incident Number": "INC000000024525",
                "Description": "Reported Asset Issue",
                "Detailed Decription": "Select an asset: OI-C8DFE446F78711ECA5890AC53BDB98EC\nWhat is the issue with your asset: It is not working anymore\nIP Address: 192.168.178.1\nHow urgent is your issue: 2-High\nError Logs: [AGGHE12CCOVBFARZWH76RZWH767LQR]\nRequest Summary: Reported Asset Issue\n",
                "Resolution": "",
                "Categorization Tier 1": "",
                "Categorization Tier 2": "",
                "Categorization Tier 3": "",
                "Product Categorization Tier 1": "",
                "Product Categorization Tier 2": "",
                "Product Categorization Tier 3": "",
                "Resolution Category": "",
                "Resolution Category Tier 2": "",
                "Resolution Category Tier 3": "",
                "Closure Product Category Tier1": "Hardware",
                "Closure Product Category Tier2": "Processing Unit",
                "Closure Product Category Tier3": "Laptop",
                "Generic Categorization Tier 1": "",
                "Generic Categorization Tier 2": "",
                "Generic Categorization Tier 3": ""
            },
            "_links": {
                "self": [
                    {
                        "href": "https://helixsjc814-demo-restapi.onbmc.com/api/arsys/v1/entry/HPD:Help%20Desk/INC000000003587"
                    }
                ]
            }
        }
    ],
    "_links": {
        "next": [
            {
                "href": "https://helixsjc814-demo-restapi.onbmc.com/api/arsys/v1/entry/HPD:Help%20Desk?offset=1&limit=1&fields=values%28Incident%20Number%2C%20Description%2C%20Detailed%20Decription%2CResolution%2C%20Categorization%20Tier%201%2C%20Categorization%20Tier%202%2C%20Categorization%20Tier%203%2C%20Product%20Categorization%20Tier%201%2C%20Product%20Categorization%20Tier%202%2C%20Product%20Categorization%20Tier%203%2C%20Resolution%20Category%2C%20Resolution%20Category%20Tier%202%2C%20Resolution%20Category%20Tier%203%2C%20Closure%20Product%20Category%20Tier1%2C%20Closure%20Product%20Category%20Tier2%2C%20Closure%20Product%20Category%20Tier3%2C%20Generic%20Categorization%20Tier%201%2C%20Generic%20Categorization%20Tier%202%2C%20Generic%20Categorization%20Tier%203%29"
            }
        ],
        "self": [
            {
                "href": "https://helixsjc814-demo-restapi.onbmc.com/api/arsys/v1/entry/HPD:Help%20Desk?fields=values%28Incident%20Number%2C%20Description%2C%20Detailed%20Decription%2CResolution%2C%20Categorization%20Tier%201%2C%20Categorization%20Tier%202%2C%20Categorization%20Tier%203%2C%20Product%20Categorization%20Tier%201%2C%20Product%20Categorization%20Tier%202%2C%20Product%20Categorization%20Tier%203%2C%20Resolution%20Category%2C%20Resolution%20Category%20Tier%202%2C%20Resolution%20Category%20Tier%203%2C%20Closure%20Product%20Category%20Tier1%2C%20Closure%20Product%20Category%20Tier2%2C%20Closure%20Product%20Category%20Tier3%2C%20Generic%20Categorization%20Tier%201%2C%20Generic%20Categorization%20Tier%202%2C%20Generic%20Categorization%20Tier%203%29&offset=0&limit=1"
            }
        ]
    }
}

entries_empty = len(json["entries"])
print(entries_empty)

#for entry in json['entries']:
    #print("counter")


search_string = "values"

occurrence_count = str(json).count(search_string)

#print(f"The search string '{search_string}' appears {occurrence_count} times in the text.")