import miney

mt = miney.Minetest()

for node_type in mt.node.type:
    if "gold" in node_type:
        print(node_type)
