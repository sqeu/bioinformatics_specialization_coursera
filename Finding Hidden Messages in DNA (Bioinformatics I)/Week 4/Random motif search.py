# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 20:09:08 2019

@author: hugo_
"""

"""
RandomizedMotifSearch(Dna, k, t)
        randomly select k-mers Motifs = (Motif1, …, Motift) in each string from Dna
        BestMotifs ← Motifs
        while forever
            Profile ← Profile(Motifs)
            Motifs ← Motifs(Profile, Dna)
            if Score(Motifs) < Score(BestMotifs)
                BestMotifs ← Motifs
            else
                return BestMotifs
                
"""
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

import sys

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

def prProfile(consensus,profile):
    prob=1
    for i in range(len(consensus)):
        l=consensus[i]
        prob=prob*profile[l][i]
    return prob

def profileMostProbableKmer(text,k,profile):
    max_pattern=""
    max_val=sys.maxsize*-1
    for i in range(len(text)-k+1):
        pattern=text[i:i+k]
        prob=prProfile(pattern,profile)
        if prob > max_val:
            max_val=prob
            max_pattern=pattern
    return max_pattern


def profileMotifsLaplace(motifs):
    countDic=countMotifs(motifs)
    denominator=int(sum(countDic[0].values()))+4
    formattedDic={'A':[],'C':[],'G':[],'T':[]}
    for dic in countDic:
        for key in dic.keys():           
            formattedDic[key].append(dic[key]+1/denominator)
    return formattedDic

def greedyMotifSearchWithLaplace(dna, k, t):
        bestMotifs =[single_dna[0:k] for single_dna in dna]        
        for i in range(len(dna[0])-k+1):
            motifs=[dna[0][i:i+k]]
            for i in range(1,t):
                profile=profileMotifsLaplace(motifs)
                motifi=profileMostProbableKmer(dna[i],k,profile)
                motifs.append(motifi)
            if scoreMotifs(motifs) < scoreMotifs(bestMotifs):
                bestMotifs=motifs
        return bestMotifs

import random

def randomMotifs(dna,k):
    max_len=len(dna[0])-k
    motifs=[]
    for single_dna in dna:
        rand_idx=random.randint(0,max_len)
        motifs.append(single_dna[rand_idx:rand_idx+k])
    return motifs 
    
def randomizedMotifSearch(dna, k, t):
    motifs=randomMotifs(dna,k)
    bestMotifs=motifs      
    while True:       
        profile = profileMotifsLaplace(motifs)
        motifs=[]       
        for single_dna in dna:
            motifs.append(profileMostProbableKmer(single_dna,k,profile))
        if scoreMotifs(motifs) < scoreMotifs(bestMotifs):
            bestMotifs=motifs
        else:
            return bestMotifs
        motifs=randomMotifs(dna,k)

def randomizedMotifSearchLoop(dna, k, t):
    random.seed(0.5)
    motifs=randomizedMotifSearch(dna,k,t)
    forever = 1
    bestMotifs=motifs[:]    

    while forever<1000:        
        profile = profileMotifsLaplace(motifs)
        motifs=[]
        
        for single_dna in dna:
            motifs.append(profileMostProbableKmer(single_dna,k,profile))

        if scoreMotifs(motifs) < scoreMotifs(bestMotifs):
            bestMotifs=motifs[:]
                #print(bestMotifs) 
        motifs=randomizedMotifSearch(dna,k,t)
        forever+=1
        
    return bestMotifs
        
    

k=15
t=20
dna=[
'TACGTCAGTGCCTTCTACTACTTTTATTCATCCCCCGGGCCATCGCACTCAACAATACTGGCCCGTACACACCTGTGACCGTCGGAACAATGAAGTAGTCCACATACCCAGGTGACAACTATGCCATGCTAGTAGCATTTTGGCCTCACATAAGCACGTGTAGATACGTCAGCTTCCAGATAGGAGATAAACGCAATACGTCAGTGCCTTC',
'TACTACTTTTATTCATCCCGTGCGGAAGCGGTCCCCGGGCCATCGCACTCAACAATACTGGCCCGTACACACCTGTGACCGTCGGAACAATGAAGTAGTCCACATACCCAGGTGACAACTATGCCATGCTAGTAGCATTTTGGCCTCACATAAGCACGTGTAGATACGTCAGCTTCCAGATAGGAGATAAACGCAATACGTCAGTGCCTTC',
'TAGTTAGTTGCGGGGCTTCGCGACTGGTCCTCACAACGTAAGGGGGAACTATGGATGAATTAGTTCTTTTCAATCCTATGGGGCTAGTTTTCAGAGATGTCCATTCTCAGGTGTTGCACCCTTACAGCTCCGTGGATTCATGTTAAGCTCCGATCCGAGAACGTTATTTCGCGGTCAGCCCTTGAGAACAGACCAGTCAAGAATGATCGTC',
'CTCTTCGGCCTTGCCCAAGTTAGAAAGGTCGTTACATGTGAAGCAACGATGGAGTCCCAGTCGGACCGTTCGGGAAATAGAGCCCAACACGGTCGGAAACGTGCTGCAATGGAGGGACGCTGGCGCATGATCCGAGTGGATGCTCAGGATGAAATCCGGAGCTCGTTATGTTTCGGTCGTAGGCTATACGTACTGATGATATTCCAGTCCG',
'GGCTGACGCGGGCCCCCCGCAGAGCTACATCGCGGCGATTGTACCTGGCATTTGTCGAACCTGGGACCACATATGAAGCGGTCTAGGGATCGGCCGTGGGTTATTTCGTTGAGCGTATTCCATGACATATCAACCTGCTCAATCGGGCTAAAGTGCCTACGAGGGTCAAGGGGCCAGGGCGGGCCAAAATTGTTGTCAGTCGACGTAAGAC',
'AGGCCATGGTTATCCCCTGATTCAGCCACTAGAGGCTACGTGCGACGTTACAGAGCGGTCGGTCGTAGTTGGGATGGGTTGGAAATGTCTTCATTCAGCTTCGATGGCCCACAATTTGGAACCGTTACCTTGTAGCTCAGTCAACCTAGACCTCACCATACTGTCTGAGTAGATATGTTCGTCAGCCCGACCGAGGGGTTCAATCTGGTAC',
'GGACCGACTGTCAGGAGACGCCACTGCGTGAACACGATGGCGCACTGAGAGTCATCACAGGCACAGTCGCAGTGTACTGCCGGCGATGCGCATTAACTTGCCTCTGGGCTGCAGCCTCCCAGGCTTGCCTTCCGTCGCTAGGCGATACCCCCAATGCTGCATCAGGTATCAGGTAACTTATTAGTACATCGTTAGCTAGCGGTCGCGTAAG',
'AACCCCAAGGATTCACGTGGCATGAGGCCTTAACTGATATACGTTATACCGCGGTCGAGGGGTTGGGATCTCCGCCAATATCGAGGCGCTACGCCAGACAGATTGACCCTCAAGTACCTCCGCGGTCCCGAGACATGGCTAACAGTGCTAATGAGCTCTTCGAGCTCCGACTGTATTTCCTCCAAGATTTTCCGGCGAGCCTTGAGTTAAG',
'GTCGTCTGTGAGACAAGCTATAACATCAAAGTTACTAGAGGGCTCGGTGTCTCGCAAGATGAAAACCGCCTTACTGCCACACCGGGAATTAGACCTGCCAACATGATTGGAGTACTGGCCAGCAAGCATATCATTAACGTAGCCATGAAAGCCTTCGTGCGCGTTATGAAGCACCCGTTGCCAGATGGAGATACTCAAGAACACAGCACAC',
'CCCCCGGCAAGCGCAATTAACAAGTGGTCTCCTTGCTGTCTGGATAGCTCCAGGGCCTCTCGGCTTTCGTTGTCGCGGAAAAGTCCCTTCAGAGGGGTTCGAACACCTGCACGGGATAGGGGTATCGAAATGTAATCGTAAGCGTTCAAAAGCGGTCACACAGTTCTGAGCGGAAGTACCTACGCCTTCACTAAGCTACTCGGGGTAAGTT',
'GACACTGACACAGTAGGTATTCGCTGTAACGCAGAAGAACTCGTGATAATTTTATGAAGCGGTGCATTACGCGATCGTTACTTGGATTGCCTTAAACGGCCACGATCGGCATGATAGACTTACACTTATGGGAATTCATAGTGAATAGAGATTGGTAAAACCCGAGACAGAAATGTTATTGGTCTGAAGTTAGGGTACCTGATATGGAACT',
'TATGCGCTGGTGGGATATTAACGTTTACGAGAGTGGTCACATCGAGTGGTGCGCATGTGAGTTCAATCGTACGAATCATGTACAACCGTTATGAAGCGCCGTATCACTCATTTCAAAATCTAGGACTCGTCTACTTTCAAGAGCTTCGGAATCTCGATTAAGCGCGCTGTGGATACGTCAAAAGGACCTGTGGGGTAGAAGCCCACCCTGA',
'ATTCAAACTGGATTGAAATCGTCGTATTACCGCGGACGGATATTCTAATGGACTTATACGTAAGAGCGCTAAACGGATGGAGCACCACTCGGCGGTCATCGTATAGAAGCGGTCGGCTAGCAAGGCGGCGTTAGGTGCTGGCTTCCTACGTCGCGAGGTAAGCGCCGCTTCCACAACCAAGCAAAGCGGCAAAGTGGATATCTAAGGGATC',
'TGAACAGAACAAGGGGGCCCAATGCGGTGCAGGTGTATGAGTGGGCACAACGAACCATACCAACTGAAGATGTTACATGACGTCAGTTCACAGGATTGTACCTTCTTCGCCAGCCACCTAGGTTGTGCTAAGCACTCAGAGGCCAATTCACACCTCTTCGTTATGAAGTTTTCGTCCTCTTGGGCTGCCTAAAGGCATGGTAAAACTATCT',
'AAGCTATGCGCCTTACGCAGGTCTTCTCAAGACTGGGGTCCTTAAGATCGGTGGGGGCACTTCTCTAAATGAAGCGGTCTACCCCGATGTTGCGAGAGTTATCTGTTACGAATGGTAACCCGCAGGTGACAGCCTCTGGATCTTGCTGCCCAAGATCTAAAAAAGATGGCCGCCGGGTATTGACGCCCACTTGTAGTGTTTGGGCACCTCC',
'TGGGATAGGTTCCGAAGCTCCTGTGCTAGCACTGCATTAATCGGGATAGAAACGTAGAACACGTTCACTCTTGCCCCTATATCAAGGTGGGCTCAGCCATCGCCAGGTCGAGCTGTCACACTAGATCCCTGCAGCAGCGTCGGTCATCGTTATTTCACGTTATGAATGAGTCGTCTTTGACGTCACCAGGGAGTTAAGGCACCTTACCCCT',
'AGTATGATGCAAAGTCTGGTTATGAAGCGGATTTAGCGGATTAGAACAGGGTACCATTCATTCCCCTAGAAGAGCATCGCGGGTCTCCCTCCGGATCAGCACAACCGGGTGTAGACCACTTGTCAGAGACTGCTCGTAGCTGCACATGTTCCGACACATGATTATGACGTGGTCGCGATCTAATGCGCTGATTATTACTTCCGAGCGTGCG',
'TACGCGCGGTACTGCGTTTGCAAGCGGTCAGTACCACGAGGGGCCGCGTGCACAAGACTGCCACACTCCTTGCACACTGCCCAGTACCGATGAAATACGGAATCCTTGCCCGCGGCTTACCTCAAGATGAACCAGCTCACGGCACCAGCGGTTCCGAACATTCCACGCTTAACGCCCTGGCCCCTCGAAAGAAGGTGTGTTCTTTACGTGA',
'ACATATGGCGGGTCTCATTACATGGTCCGCCAGGGCAGGCCCTGAACAAAGCGATAGACGCAAACCACCCCATCCTTATTTTCGTTATGATCAGGTCAGAAAGAGTTATTGACCGACTCCAGTCTCGTAAGGATGTGTATCCTTCAGGCGGGGGATTTGTATGGACTCGGGCTGGTATTCATCTGTATCAGGTCTTCCCCCTTCCGACCCA',
'TATGACACGTGCGCTAGCGTGGACAACTCCGCGGTGAAGCGGTCCATTGGGCTGTCGCAGATGATTTCGTTATCTGTTAGACAAGGGTCGTTGGAATTGAAGTTTTGCCAGTGAAGTCTCACGCTGATACTGCGGTGTTGCCACACGGACCGAACTACAACGGAGGTTATTCCGCCCAAATAGGAAAGGGTTTCCACATTGTACTACGTCC'
    ]

random_list=randomizedMotifSearchLoop(dna,k,t)
for motif in random_list:
    print(motif)