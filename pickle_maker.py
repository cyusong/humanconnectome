# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 21:58:11 2023

@author: marek
"""
import os
import collections
import pickle

types = []
for i in os.listdir('D:/GPT_annotator_Melissa/annotations/'):
    try:
        a = open('D:/GPT_annotator_Melissa/annotations/'+i,'r').read()
        pmid, abstract, pubdate, journal, doi, main = eval(a.split('\n')[0])
        findings = a.split('\n\n')[1].split(' \n')
        for j in findings:
            if j.count('!')==2:
                types.append(j.split('!')[1])

    except:
        pass
'''
interactions_count = collections.Counter(types)
top_studied = dict(interactions_count.most_common(100))

I made interaction_types from top 100 types
'''
'''
types2type = {}

for i in open('D:/GPT_annotator/interaction_types.txt','r').readlines():
    if ':' not in i:
        types2type[i.rstrip()] = i.rstrip()
    else:
        splitta = i.rstrip().split(':')
        types2type[splitta[0].rstrip()] = splitta[0].rstrip()
        for j in splitta[1].split(','):
            types2type[j.strip()] = splitta[0].rstrip()
'''

good, bad = 0,0

agent2agents = {}
uniqueEdges = []
for i in os.listdir('D:/GPT_annotator_Melissa/annotations/'):
    try:
        a = open('D:/GPT_annotator_Melissa/annotations/'+i,'r').read()
        
        findings = a.split('\n\n')[1].split('\n')
        
        for j in findings:
            if j.count('!')==2:
                splitta = j.split('!')
    
                agentA, _, agentB = splitta
                agentA = agentA.split(':')[0].upper()
                agentB = agentB.strip().upper()
                edge = (agentA, splitta[1].strip(), agentB, i.split('.')[0])
                
                
                #if agent absent
                if agentA not in agent2agents:
                    agent2agents[agentA] = []
                if agentB not in agent2agents:
                    agent2agents[agentB] = []
                
                #the problem is here: rsw1 synthesized cellulose, cellulose synthesized rsw1
                agent2agents[agentA] += [edge]
                agent2agents[agentB] += [edge]
                uniqueEdges.append(edge)

    except:
        print(i, 'wonky')
    

with open('allDic', 'wb') as file:
    pickle.dump(agent2agents, file)
    
save = []
for i in list(set(uniqueEdges)):
    save.append(i[0]+'\t'+i[2]+'\n')
    
try:
    v = open('edges.txt','w')
    v.writelines(save)
    v.close()
except:
    print('count not save')