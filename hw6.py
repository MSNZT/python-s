import json
pur_dict = {}
with open("purchase_log 2.txt", "r") as pur:
    for line in pur:
        line = line.strip()
        if line:
            pur_data = json.loads(line)
            user_id = pur_data["user_id"]
            category = pur_data["category"]
            pur_dict[user_id] = category

with open("visit_log__1_.csv", "r") as visit:
    with open("funnel.csv", "w") as funnel:
        funnel.write("user_id,source,category\n")
        next(visit)
        for line in visit:
            line = line.strip().split(",")
            user_id = line[0]
            source = line[1]
            if user_id in pur_dict:
                funnel.write(f"{user_id},{source},{pur_dict[user_id]}\n")
