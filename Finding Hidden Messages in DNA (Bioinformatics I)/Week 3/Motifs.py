# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 20:44:20 2019

@author: hugo_
"""
"""
MotifEnumeration(Dna, k, d)
        Patterns ← an empty set
        for each k-mer Pattern in Dna
            for each k-mer Pattern’ differing from Pattern by at most d mismatches
                if Pattern' appears in each string from Dna with at most d mismatches
                    add Pattern' to Patterns
        remove duplicates from Patterns
        return Patterns
"""
def hammingDistance(p,q):
    min_len = len(p)
    q_len=len(q)
    if q_len<min_len:
        min_len=q_len
    distance=0
    for i in range(min_len):
        if p[i]!=q[i]:
            distance+=1
    return distance

def approximatePatternMatching(pattern, text, d):
    positions = []
    len_text=len(text)
    len_pattern=len(pattern)
    for i in range(len_text-len_pattern+1):
        qattern = text[i:i+len_pattern]
        if pattern == qattern or hammingDistance(pattern,qattern)<=d :
            positions.append(str(i))
    return positions
            
    
def approximatePatternCount(pattern, text, d):
    positions=approximatePatternMatching(pattern, text, d)
    return len(positions)

def neighbors(pattern, d):
        if d == 0:
            return pattern
        if len(pattern) == 1 :
            return ['A', 'C', 'G', 'T']
        neighborhood = []
        suffixNeighbors = neighbors(pattern[1:], d)
        for text in suffixNeighbors:
            if hammingDistance(pattern[1:], text) < d:
                for x in ['A', 'C', 'G', 'T']:
                    neighborhood.append(x + text) 
            else:
                neighborhood.append(pattern[0] + text)
        return neighborhood

    
def motifEnumeration(dna, k, d):
        patterns = set()
        for single_dna in dna:
            for i in range(len(single_dna)-k+1):
                pattern=single_dna[i:i+k]
                neighborhood=neighbors(pattern, d)
                for neighbor in neighborhood:
                    every_string=True
                    for single_dna_2 in dna:                
                        if approximatePatternCount(neighbor, single_dna_2, d)==0:
                            every_string=False
                    if every_string:
                        patterns.add(neighbor)
        return patterns
    
k=5
d=1
dna=['ATGTATACCGACCAGTACCAACATT','CGTCTTGTCCGCGCGATCAGAAAGT','AAGACACCACACCAGCTGACGGCCG','CATCTACCAGTGGATTGCAAATTGC','GCTTGATCCGCTGCATTTGTACCAG','ACCAGTGGCATCTCTATCTCATAGA']  
motifEnumeration(dna, k, d)

motifs = [
"TCGGGGGTTTTT",
"CCGGTGACTTAC",
"ACGGGGATTTTC",
"TTGGGGACTTTT",
"AAGGGGACTTCC",
"TTGGGGACTTCC",
"TCGGGGATTCAT",
"TCGGGGATTCCT",
"TAGGGGAACTAC",
"TCGGGTATAACC"
]
        
def nucleotideDic(motifs):
    dicList=[]
    for i in range(len(motifs[0])):
        dic = {'A':0,'C':0,'G':0,'T':0}
        dicList.append(dic)
    return dicList

def countMotifs(motifs):
    profiles_list= nucleotideDic(motifs)
    for motif in motifs:
        for i in range(len(motif)):
            nucleotide=motif[i]
            nucleotide_dic=profiles_list[i]
            nucleotide_dic[nucleotide]=nucleotide_dic[nucleotide]+1
            profiles_list[i]=nucleotide_dic
    return profiles_list

countMotifs(motifs)

def scoreMotifs(motifs):
    countDic=countMotifs(motifs)
    score=0
    for dic in countDic:
        max_val=sys.maxsize*-1
        for key in dic.keys():
            if dic[key] > max_val:
                max_val=dic[key]
        score+=10-max_val
    return score

scoreMotifs(motifs)

def profileMotifs(motifs):
    countDic=countMotifs(motifs)
    denominator=int(len(motifs))
    formattedDic={'A':[],'C':[],'G':[],'T':[]}
    for dic in countDic:
        for key in dic.keys():           
            formattedDic[key].append(dic[key]/denominator)
    return formattedDic

profileMotifs(motifs)

from math import log

def entropy(motifs):
    profile=profileMotifs(motifs)
    entropy=0
    entropy_list=[]
    for p in profile:
        score0=0
        for nucleotide in p.keys():
            score=p[nucleotide]
            if score > 0 and score<1:
                score0=score0+score*log(score,2)
                entropy=entropy-score*log(score,2)              
        entropy_list.append(score0*-1)
    return entropy

entropy(motifs)

"""
MedianString(Dna, k)
        distance ← ∞
        for each k-mer Pattern from AA…AA to TT…TT
            if distance > d(Pattern, Dna)
                 distance ← d(Pattern, Dna)
                 Median ← Pattern
        return Median
"""
import itertools

def createDictionary(k):
    dic={}
    nucleotides = 'ACGT'
    for perm in itertools.product(nucleotides,repeat=k):
        dic[''.join(perm)]=0
    return dic

def d(pattern, dna):
    k= int(len(pattern))
    dic = {}
    for single_dna in dna:
        min_val=sys.maxsize
        for i in range(len(single_dna)-k+1):
            distance=hammingDistance(pattern,single_dna[i:i+k])
            if min_val > distance:
                min_val=distance
        dic[single_dna]=min_val   
    return sum(list(dic.values()))

d("AAA", dna)

import sys

def medianString(dna, k):
        distance = sys.maxsize
        dictionary=createDictionary(k)
        median=""
        for pattern in dictionary:
            hamming_d=d(pattern, dna)
            if distance > hamming_d:
                 distance = hamming_d
                 median =pattern
        return median
        
k=6
dna=['CTCAACGTGCTAATTCAGATGAGCGTATATACGATCTCTATT',
'ATGTATAGTGCTGTATAGAGGAAACCATCAACACATGTAGCT',
'AGGTTCTCAACAGAAGTAATAGCCGTATAATGAGCAAAGGGA',
'GCAGGTTGATGGGTATAGGTTGTGGTGACGCGCCAATTCTGG',
'ATTCCAATGTCTGTATATTGCGCGTCTCCGTTTCGCCATTCT',
'TCGCTCGAGATAGTATAGGCGAGTTGAGAACGTAGGTCTTCA',
'TCGGATGTATAGTACCCATCTGAGGTGCATTTTTACCACGAA',
'TAGACATACATAAATGCCTATACTGGCGTGTCACGGGTATAG',
'GTATAGAGTACATGCACTTTCACTACGGTGTTGTAGCAGGCA',
'ATATCCGTATAGTGCTCTAGTTGAACAACCAAAGTGCCCTTG']
medianString(dna, k)        

def prProfile(consensus,profile):
    prob=1
    for i in range(len(consensus)):
        l=consensus[i]
        #print(profile[l][i])
        prob=prob*profile[l][i]
    return prob
    
consensus='TCGTGGATTTCC'   
profile = {
    'A': [0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.9, 0.1, 0.1, 0.1, 0.3, 0.0],
    'C': [0.1, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.1, 0.2, 0.4, 0.6],
    'G': [0.0, 0.0, 1.0, 1.0, 0.9, 0.9, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0],
    'T': [0.7, 0.2, 0.0, 0.0, 0.1, 0.1, 0.0, 0.5, 0.8, 0.7, 0.3, 0.4]
}   
prProfile(consensus,profile) 

def profileMostProbableKmer(text,k,profile):
    #minDic={}
    max_pattern=""
    max_val=sys.maxsize*-1
    for i in range(len(text)-k+1):
        pattern=text[i:i+k]
        prob=prProfile(pattern,profile)
        if prob > max_val:
            max_val=prob
            max_pattern=pattern
    return max_pattern

text='CTTTGCATAAAACGCTCGATTGGTCTGATGCGTCCGCTGCACCTTTGATAAATGTACCCCCCGTAAGTAATCCTTTGCCGCGGCCTCCATGATGCACCCGCGACAGCCGTAATGAAGCAGCTAGGTAAAGGAACTAACCACCAGAAGACTCCGCCACTTCTCGTTCATTGGGAACTGATAGCTGGGGTGCACTATGCTGCAACTATTTCTCACGCATCGCTGTCTTCTGTACTCGCCCTCCTTCACGCATGCGGCGTATCCAGATTTGTCGAAAACACATCCGGCGTTGCATCCCATTCGAACATGGTGTCATGAGGACGGAGCGTCATCAGATTGGAGGTTCCGCCCTGCGAATCTTGCGTGAGACACTCTATTCGAACTGCTTTGGCAACCCCATTACATTACGCTCCATCGGAACTTCGTTCTGGCATAGCACCCCGGAGTTTCGAGTCATGACGCGCCTAAGAGAAGTCCCCGAGTGTCACCAGGCCTAGGCGAATGACCGCAATAACTTGTTGGTTGAAAGTTTACTAAGGATTGTGGAACAAAAATACATATGTTGGCCGTCGGTAGGGAAGAAAAAATAGCGAAAGGGGGTTTGGGTGCATCCTTGCTATTAGGTCTTTCCGAGAAATCATGTGACATAATTCGCAACATGTTTCCTTACCTCTTGGTAAATCGTTCTACATGTATGACATATCTTTCGCGACCCTTGGACAGCTGCTGTACGGCCTGTCGACCAAGTGTAATGTCTTAGCGCGTATAGCCTTTGATATCGCCAGCGTGAGACAATACATACGAGGATACGAAGAGGTGGACAGGGTGTGCCAAATGCGTCATTAATTCTACTCAAAGTTCCCGGGCAACACTAGGCTGACTGACGGACGATCAGACAATAACTTACCCCTCAGCCTAACACATCACAAAGATCCACCTTTGCTGGGCCTTTTAGGCGAAAAAGCCAGCCCCATGAACCAAATTACGTGCCAATAGGTTGTCG'
k=13
profile={'A':[0.197,0.276,0.224,0.289,0.211,0.289,0.276,0.303,0.276,0.263,0.224,0.263,0.184],
'C':[0.303,0.368,0.171,0.158,0.289,0.316,0.289,0.237,0.263,0.289,0.237,0.211,0.355],
'G':[0.211,0.211,0.303,0.263,0.211,0.211,0.263,0.224,0.237,0.197,0.237,0.276,0.211],
'T':[0.289,0.145,0.303,0.289,0.289,0.184,0.171,0.237,0.224,0.25,0.303,0.25,0.25]}
    
profileMostProbableKmer(text,k,profile)

"""
GreedyMotifSearch(Dna, k, t)
        BestMotifs ← motif matrix formed by first k-mers in each string from Dna
        for each k-mer Motif in the first string from Dna
            Motif1 ← Motif
            for i = 2 to t
                form Profile from motifs Motif1, …, Motifi - 1
                Motifi ← Profile-most probable k-mer in the i-th string in Dna
            Motifs ← (Motif1, …, Motift)
            if Score(Motifs) < Score(BestMotifs)
                BestMotifs ← Motifs
        return BestMotifs
"""

def greedyMotifSearch(dna, k, t):
        bestMotifs =[single_dna[0:k] for single_dna in dna]        
        for i in range(len(dna[0])-k+1):
            motifs=[dna[0][i:i+k]]
            for i in range(1,t):
                profile=profileMotifs(motifs)
                motifi=profileMostProbableKmer(dna[i],k,profile)
                motifs.append(motifi)
            if scoreMotifs(motifs) < scoreMotifs(bestMotifs):
                bestMotifs=motifs
        return bestMotifs

dna=['TGGTTGCATTGACGGCAATGCCTTTGGACATCAGAGTTGTTAGGCAACAAAGCGACGTACTACCGTCTGACTGGTAGGCTCTCTCACAGTGCCGAACCTTTGCGGCTAAGCAAGGAGCATTGGATAGATATCAACCGCGAGTGCGTAGTTGACAGC',
'AAGCTAAGACCAGGTCGATAGAGTTGTTCGAACTATTGGTTTCAGTGAATCCGCACTAAGCAGGGCTAAGAGGTGGCCATACCACACTACATAGGTCTTAAACCGCTTGGTTAACTTACGGACGTCAGCCAGCGCGGGTTTGTCCCGCTCGATCTG',
'TACCCTCATGATGTCCTGTGGCTTGATGATCGTCGAGTGCCGAGGAAGACTCTAAGATAAACTCCTGTAGTAACCAAATCAGACCTAACCGCTAGAGAACGCTGAGACCTACCACCGGTCAGGTTGCACTGACGACCCCAATCGGTTCCCAATACT',
'GGATCGACGTGAGAGATTTCTTGATAGGTTGTTACTAGGTGCCACGACCGGTTACACCGATCGCCTATACGGTGCGAGCCTACTCTCGGACTGAGTATAATTCGCGACCCCCCCATGTTTCGGTCGCGTTTCCCTTCGACCGTGTCAACCGAGCAT',
'CTGAGTGAAACGAGGTTGCATAGAGCTGCTGCGATAGGTCAATTCGCACCCTGCAGGTTACTGTTCATATGAAGTTTCTTATTGCCGAGGCTGCCGCGGACCACTGCACCAGAGCCGGGATTGAGATACTGCCACCACGAAAGCCAACCACGGTTC',
'AATGGACGAATGGCTCTGTGAAACTGGTTCCAACGAACGGCAGGGAGTGCAGGCAATTGTTCCCGGGACGACCCTCTCGGCCGCAAATGTACATCTCCTCACGTTAGTGAAGCTTAAGGGGTTCTTCTTGGGACAAGCAACAGGGGAATACAACCT',
'AGAGCAATTAGCTTTATACGTGTTGCTGCAGTCCGGAGCGGTATGATTTCGAGATGACGATAGTGATACGTGAGTGTAGTGTTCTGGTTCCAACGAACGCTCCATAGGGTATTTAGGCTCCGGAGAGATGGGCCACCCCATAGGGTGGTGCTAATA',
'TGGCATCAATCATATGGATGCCGGCCCTGATCCTGACAAGACTGGATAAGGTTCCATCGACCGGCATGAGCCTAAAAGGCCAACTCCCGTCCTGACTGTTGCTTTCTTCCCCTGACTACGCACATTTGGGGCCAATGAGCAGGGCTTGAGAGTAGT',
'CAAATTGGCCGCCGATGGATAAATACAAGACTATGTTAAAGTGCAGATCTAAGAAGCCCTAAGCCCAGAACTTCTATGGATGCGAAGTACGCCCCTTCAGAATCATTGCAAAGTCATCCATGGTTACAGCGAGACCTCGTGCCGTTTCAGTCTATA',
'TCGAGAGCCCCACTGGCTGGTGAGCTGCAAGCACGTACCCAACCTCGAGACGATTCGCTGGAACTTTGGAATCTGGCGATCTCCAGCATTCATTCCCCTAAGTTTGAACGGTTTCATAGACGCATAGCTCTGCCGGAGTCAGCATCAACGAGGCGC',
'TATAAGAGTGTTTCTTATGCTTCTGCGGAGTAGCCGGAGGCCCTCCGAGCATGTTGCCTTCATACTGGATGGCAGCAAGGGGACACTGTAGCTACAAGCAGTTGTGCTCGGTTTCAGAGACAGCGGCAGTTCTTTCTATTTCTTGGACACCTCGGC',
'GGTCCGTCGTGACGCACCACCTGGCGGTTTCATCGATAGGGCCGCATCCTTGTTAGTACCTCCATTCGCAAGAAGTATCTCCTCACCGTCCTCCCTACAATTGTGATCCGTGAAAAAAATGGATGCACAGAATTAAGGGTTGCGTGTACCCGAGAG',
'GGCAAAGTCTATCAAGAAATGTTGGGGTTACATGGACACGAATACTCCCTGCCGAGTCGGTAGGCAATTACACGGTGAATAGTTGCGCAGTTTGTACCAAGTGACCAAGCTTACGGCACGGGCCCTTGATTAAGGCCCGGGTTAAAATTCACATGT',
'ATCACAATGCTTAGCTCAATGAATGCGCCGTGCGTAGGGTTCCAATGATTGCAGGCAAGTCGCCGAAAACCTGCGGGGGATCATAGCAAATATTTTTATACGGCTTTCATAGGTACGGACTCACGCCATATAGAAGTACGTCTAACTCGCCCCTGT',
'AAAGTAACTTAGGGAATAAACACGTGAATCAAGGAAGCTTCTCGTCTTAAGCCTATATTAAGGTTGCATTGATAGCGAGAAAGCGGAACTCTGGAAGGGGATTTTTCAGAAGTACAGTCCCCTGACTCCATTGTCATTGTGCATGCCTCATGGAGC',
'CCAAACGTTTACCCTCAGAGCTGCACATGTCGGCATAGATAGTGCATTCGGGGGGCGGCGACGCGTGGGTGACCAGTTTCAGGCTGAACGAGGGGGCGGTTGCAAGGACCAAGGGTAACCTCGCCCTCGGGCAGAAGGGTTCCTTACCAACTCTCG',
'CGCTATGGCACGCACGATGGGGGGCCAAGGGGAATTCTTATCCCGAAAACACCACTTAAAGCGCATTGCTACGGGTTTCAGTGATTCGAGACAACAGGGTGCTATCTTCTGTCCTCCTCCCTCTGGCGCAAATACAACAGTAGGTATAAGCCGGCA',
'GCGCGCTTTGGCGGGCGCGCCGCCTAAAAGAACGGGTGGTTTCATAGACTCTGCACCCGACCAGCAAGGGTCAGCGCCCCCCGAGCAGACTGAGCTCTGGGCAGACATGCATGTTGAACCAATCACGAGCTGGTAATCTTTGGGTAGTTTCATGTC',
'AGTTGCAGGAAATGCATGGAAGAAGCCGGGGAACATTGGTTACATTGAGTATTCACGAACGTGACAGCGGGACTATGTAGCGGGTGAACTTCCTAGAGCTTGCGTACGGAGGGGTTGCTCCGACGGGCGGCGCTTCTCAGAGATTAGAACGCTCGG',
'ATCATTATATCTCTCGGAGAATCGTAACATGGTGTGCGGCAGCAGAAGGGGTTGCACAGATACTAGCCGTCTGCATAGTAACTTGCTCGTCCAGTCGTCTCTGTCGAGGAAGACACCTGTTAGGGTCCTTGGCCACTAGGGTTTGACGACGCCGTG',
'GAGGATATGCCCACGGCTGGGCCATTCTTACAAGTTGGGTTGCATTGATCTTCTCCGACGTCCATGACGATCATAATCAATTGTGACAAGGTGGCAGGTGCTACCTAATTAATAAACCAACAACCCACACATTACTTGATACTGGGGGGAATATGT',
'GCGAAACGCATCTGAAAGTCCACAAGGTTGCATAGAACGCGGACTGAGGCGCGGATCCCCAGCGATGGAATATAAGTAGGCGGCAAATGCCTGTCGGGCGCTTAAAACAAGGATGAGCAGATCACGAACCGGAAAAAGGCCGTCCTTTTCGAGTTG',
'TCACTAGGCCCATATGGTGATGGGGGCAACGCTTGACAAGGGGAGACGAGCAGTAACCGGGTAAGTTATGTGGTCTCGCGAATACGGCTAAGCTACAAGGCAGAGTAATAGCTGAGTGATTGACACGTCCACGGGTTGCATCGAAATTTACGAGGA',
'CCCATTAGAACCTTGCGGCCTAGAAGGTTACAAGGACTGTGTACGCTGAAATAATAATCGACTGACAAGGTGTCTTATGCCCCGTTGTCGGGCCTAAATCCACCTCGAGTAGATCTCGGGAAGCCTAGCGTGGTGACGTTCATTCCACCTCGCAGC',
'ATCACGCCTGGGCTAGTACAGTCTTGGTCTGCTTCTCCTATCGAGACGGCCAGCGGCAGTTTATACTTCTATCTAGGACCGACACGGTGTGGTCGGATAGAGGACAGTCCCACGGGTCGAATTGAAGTATTTAGACAAGAAAGCCGGTTTCAATGA']
k=12
t=25
' '.join(greedyMotifSearch(dna, k, t))