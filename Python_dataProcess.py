#!/usr/bin/env python
# coding: utf-8

# In[4]:


#Import Required Libraries:
import pandas as pad
import networkx as net
import json

#Load Author Network Data
dta = pad.read_csv(r"https://raw.githubusercontent.com/umassdgithub/Fall-2023-DataViz/main/Week-8-ForceSimulator/data/data_scopus.csv")

nodes = dta['EID'].values
dta=dta.fillna(0)
dta.head(5)


# In[5]:


dta = dta.dropna(subset=['Author(s) ID','Year','Authors','Authors with affiliations'])

dta = dta.fillna(0)
grap = net.Graph()
nodes = {}

for _, row in dta.iterrows():
    # Extracting authors column
    author = row['Authors'].split(',')
    authorId = row['Author(s) ID'].split(';')
    Title=row['Title']
    Yrs=row['Year']
    Citation=row['Cited by']
    Publisher=row['Publisher']
    Authoraff=row['Authors with affiliations']


    for authors in range(len(author)):

        author_id= authorId[authors]
        anam= ';'.join(author)
        title=Title

        if(author_id!=""):
          
         nodes={'id':author_id,
          "Authors": anam,
          "Title": title,
          "Year": Yrs,
          "Citations": Citation,
          "Publisher": Publisher,
          "Author with affiliations":Authoraff
           }
         grap.add_node(author_id,**nodes)

print(grap)
from networkx.readwrite import json_graph
with open("NetworkGraph.json", "w") as nod:
    json.dump(json_graph.node_link_data(grap), nod)


# In[6]:


with open('NetworkGraph.json', 'r') as datafile:
    dta1 = json.load(datafile)
newnodes=[]

grap=net.Graph()

def get_author_country(authors_with_affiliations):
    first_affiliation = authors_with_affiliations.split(';')[0].strip()
    country = first_affiliation.split(',')[-1].strip()
    return country
for nodedta in dta1['nodes']:
    eid = nodedta.get('id')
    authors=nodedta.get('Authors')
    title = nodedta.get('Title')
    year = nodedta.get('Year')
    citations = nodedta.get('Citations')
    publisher = nodedta.get('Publisher')

    authors_with_affiliations = str(nodedta.get('Author with affiliations'))

    country = get_author_country(authors_with_affiliations)

    grap.add_node(eid,authors=authors, title=title, year=year, citations=citations, publisher=publisher,authors_with_affiliations=authors_with_affiliations, country=country)
# Generate clusters based on authors' countries
clusters = list(net.connected_components(grap))

# Assign classes to each cluster
class_mapping = {node: idx for idx, cluster in enumerate(clusters) for node in cluster}
net.set_node_attributes(grap, class_mapping, 'class')

# title = data["Title"]
# authors_info = data["Authors with affiliations"].split(';')

# Create a dictionary to store co-authorship relationships
coauthorship_dict = {}
for row in dta.iterrows():
    authors = row[1]['Author(s) ID'].split(';')
    for i in range(len(authors)):
      for j in range(i+1, len(authors)):
        if(authors[i]!="" and authors[j]!=""):
          grap.add_edge(authors[i], authors[j])


print(grap)
# print(edges)


# Save the data as a JSON file with proper character encoding
coAuthors_data_file = {'nodes': [{'id': node, **grap.nodes[node]} for node in grap.nodes()],'links': [{'source': source, 'target': target} for source, target in grap.edges()]}
#coauthorship_data = {'nodes': [{'id': node, **G.nodes[node]} for node in G.nodes()],'edges': edges}
with open('coAuthors.json', 'w', encoding='utf-8') as outfile:
    json.dump(coAuthors, outfile, ensure_ascii=False)


# In[ ]:




