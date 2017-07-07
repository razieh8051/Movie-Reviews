
import nltk
from nltk.tree import *
import math
import os
import re
import sys

reload(sys)
lenofsen=0

class Sentimens:
    def sentimentBase(self,text):
        """
        Returns a float for sentiment strength based on the input text(Baseline).
        Positive values are positive valence, negative value are negative valence.
        """
        words = pattern_split.split(text.lower())
        sentiments = map(lambda word: afinn.get(word, 0), words)
        #print words sentiments
        print sentiments

        if sentiments:
            # How should you weight the individual word sentiments?
            # You could do N, sqrt(N) or 1 for example. Here we use sqrt(N)
            sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
        else:
            sentiment = 0
        return sentiment

    def new_sentiment(self,sen,oldValue, grammartype):
        """
        Returns a float for new sentiment strength based on the input text Using Feature Parser.
        Positive values are positive valence, negative value are negative valence.
        """
        LeavesTags=[]
        try:
                trees=parser.parse(sen.split())
                ftype = nltk.featstruct.Feature("type")
                counttree=0#specify to work with only first tree
                if(counttree<1):
                    for tree in trees:
                        #print tree
                        counttree=counttree+1
                        if(counttree==1):
                            sentiment=0

                            #Considering 9 differnt grammar types based on the features of grammars[[read the Report for more details
                            # on each type]]

                            if(grammartype==1):
                                #print tree
                                for s in tree.subtrees(lambda t: t.height() == 2):
                                    LeavesTags.append(s)
                                    if( s.label()[ftype] == 'RB'):
                                        if(LeavesTags[0].label()['SENT']=='neg'):
                                            sentiment =  (oldValue*(math.sqrt(senlen))) - 3.00

                            if(grammartype==2):
                                 if((tree[0][1]).label()['SENT']):
                                    for s in tree[0][1][1].subtrees(lambda t: t.height() == 2):#subtrees with 2 height
                                        LeavesTags.append(s)
                                    for x in range(0, len(LeavesTags)):
                                        if(LeavesTags[x].label()[ftype]=="NOUN"):
                                           sentiment=afinn.get(LeavesTags[x][0])
                                           if(LeavesTags[x-1].label()['SENT']=="pos"):
                                               sentiment=sentiment*2

                            if(grammartype==3):
                                if((tree[0][1]).label()['SENT']):
                                    for s in tree[0][1][1].subtrees(lambda t: t.height() == 2):#subtrees with 2 height
                                        LeavesTags.append(s)
                                    for x in range(0, len(LeavesTags)):
                                        if(LeavesTags[x].label()[ftype]=="JJ"):
                                           sentiment=afinn.get(LeavesTags[x][0])
                                           if(LeavesTags[x-1].label()[ftype]=="RB"):
                                               if(LeavesTags[x-1].label()['advtype']=="IntensifierStrong"):
                                                   sentiment=sentiment*2
                                                   if(LeavesTags[x-2].label()['advtype']=="Negative"):
                                                       sentiment=sentiment-3#Instaed of flipping I decreased it by 3 (instead of -1.33 I have 0.33)

                            if(grammartype==4):
                                  if((tree[0][1]).label()['SENT']):
                                     for s in tree[0][1][1].subtrees(lambda t: t.height() == 2):#subtrees with 2 height
                                         LeavesTags.append(s)
                                     for x in range(0, len(LeavesTags)):
                                         if(LeavesTags[x].label()[ftype]=="JJ"):
                                            sentiment=afinn.get(LeavesTags[x][0])
                                     #check the verbs for postivity or negativity
                                     if((tree[0][1][0]).label()['SENT']=="neg"):
                                         sentiment=-1*sentiment

                            if(grammartype==5):
                                if((tree[0][1]).label()['SENT']):
                                    for s in tree[0][1][1].subtrees(lambda t: t.height() == 2):#subtrees with 2 height
                                      LeavesTags.append(s)
                                    for x in range(0, len(LeavesTags)):
                                        if(LeavesTags[x].label()[ftype]=="JJ"):#positivity of JJ not important here
                                             sentiment=afinn.get(LeavesTags[x][0])
                                             if(LeavesTags[x-1].label()[ftype]=="quantifierComparative"):
                                                 if(LeavesTags[x].label()['SENT']=="pos"):
                                                     sentiment=sentiment*2

                            if(grammartype==6):
                                 if((tree[0][1]).label()['SENT']):
                                   for s in tree[0][1][1].subtrees(lambda t: t.height() == 2):#subtrees with 2 height
                                       LeavesTags.append(s)
                                   for x in range(0, len(LeavesTags)):
                                       if(LeavesTags[x].label()[ftype]=="JJ"):
                                          sentiment=afinn.get(LeavesTags[x][0])

                            if (grammartype==7) or (grammartype==8):
                                #print tree
                                if((tree[0][0]).label()['SENT']):
                                    for s in tree[0][0].subtrees(lambda t: t.height() == 2):#subtrees with 2 height
                                       LeavesTags.append(s)
                                    for x in range(0, len(LeavesTags)):
                                        if(LeavesTags[x].label()[ftype]=="JJ"):
                                            if (x==0):
                                               sentiment=afinn.get(LeavesTags[x][0]) #postive negative no matters
                                               sentiment=sentiment/2
                                            if (x==2):
                                                sentiment=afinn.get(LeavesTags[x][0]) #postive negative no matters
                                                sentiment=sentiment*2

                            if(grammartype==9):
                                if((tree[0]).label()['MOOD']=="wh"):
                                    sentiment =  (oldValue*(math.sqrt(senlen))) * -1


        except Exception:
                print '\n sentence cannot be parsed or fault calculation'
                pass
        return sentiment/(math.sqrt(senlen))

    #Few preprocessing steps
    def remove_brackets(self,sentence):
        """
        remove () [] from sentences
        """
        sentence = re.sub('[\(\)\[\]\{\}<>]', '', sentence)
        return sentence

    def remove_comma(self,sentence):
        """
        remove comma from sentences
        """
        sentence = sentence.replace(',','')
        return sentence

    def remove_verbApostrophe(self,sentence):
        """
        remove apostrophe from verbs
        """
        sentence = sentence.replace('it\'s','it is')
        return sentence

    def remove_quotation(self,sentence):
        """
        remove quotation from sentence
        """
        sentence = sentence.replace('\"','')
        return sentence
    def remove_dash(self,sentence):
        """
        remove quotation from sentence
        """
        sentence = sentence.replace('-','')
        return sentence


# AFINN-111 is as of June 2011 the most recent version of AFINN
"""Creating AFINN Dictionary"""
filenameAFINN = 'AFINN/AFINN-111.txt'
afinn = dict(map(lambda (w, s): (w, int(s)), [ 
            ws.strip().split('\t') for ws in open(filenameAFINN) ]))
# Word splitter pattern
pattern_split = re.compile(r"\W+")
   
"""Parser"""    
grammar = nltk.data.load('grammars/large_grammars/SenGrammar.fcfg')
parser = nltk.parse.FeatureEarleyChartParser(grammar)

"""Reading and Preprocessing Sentence""" 
grammarnumber=0
sentences = []
ins = open( "sentences.txt", "r" )
for line in ins:
    sentences.append( line )
ins.close()

senobj=Sentimens();

for sentence in sentences:
    grammarnumber=grammarnumber+1
    sentence=senobj.remove_comma(sentence)
    sentence=senobj.remove_verbApostrophe(sentence)
    sentence=senobj.remove_brackets(sentence)
    sentence=senobj.remove_quotation(sentence)
    sentence=senobj.remove_dash(sentence)
    print "sentence: ",sentence

    #sentiment length
    senlen=len(sentence.split())

    """Comparing the Results of SSAP with Our tool"""
    oldSentiment=senobj.sentimentBase(sentence)
    print("SSAP rating: %6.2f" % (oldSentiment))
    print("New rating: %6.2f" % (senobj.new_sentiment(sentence,oldSentiment,grammarnumber)))
    print("-------------------------")

