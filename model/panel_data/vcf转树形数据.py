from Bio import SeqIO
import json

tree = {}
tree['name'] = 'variant'
tree['children'] = list()
records = list(SeqIO.parse("60seed.vcf", "vcf"))
for record in records:
    node = {}
    node['name'] = record.id
    node['data'] = record.info

    child = list()
    for alternate in record.alts:
        alternate_node = {}
        alternate_node['name'] = alternate
        child.append(alternate_node)

    if len(child) > 0:
        node['children'] = child
    tree['children'].append(node)

# 将树结构转换为phylo json文件
with open('phylo.json', 'w') as f:
    json.dump(tree, f, indent=2)