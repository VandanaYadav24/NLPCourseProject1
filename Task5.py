from task1_textTiling import read_happy_go_lucky, read_war_of_the_worlds
from task2 import count_sentiment, count_paragraph_sentis, count_chapter_sentis
from Task4 import count_negative_words, identify_prefix_negative_words, count_total_negative_occurence, plot_negation

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns 

from scipy.stats import pearsonr
from scipy.stats import spearmanr

#Finding correlation between negation scope occurrence and sentiment score.
def correlation_between_negation_sentiment(x,y):
    corr, _ = pearsonr(x,y)
    #print(corr)
    a = spearmanr(x,y)
    #a.correlation
    return(corr)

def plot_negation_sentiment(book_name,chapter_names, chapter_text, paragraph_text):
    #Sentiment score of all paragraphs of the book.
    paragraph_senti_list=[]
    for i in range(len(chapter_text)):
        paragraph_sentis_i = count_paragraph_sentis(i, chapter_names, chapter_text, paragraph_text) 
        paragraph_senti_list.extend(paragraph_sentis_i)
        paragraph_senti = np.array(paragraph_senti_list)
        
    #Negation of all paragraphs of the book.
    paragraph_negation_list=[]
    for i in range(len(chapter_text)):
        paragraph_negation_i = count_total_negative_occurence(i, chapter_names, chapter_text, paragraph_text)
        paragraph_negation_list.extend(paragraph_negation_i)
        paragraph_negation = np.array(paragraph_negation_list)
       
    
    senti_score_per_negation = {}
    for neg in np.unique(paragraph_negation):
        senti_score_per_negation[neg] = []
       
    
    neg_senti_combined = list(zip(paragraph_negation_list, paragraph_senti_list))
    neg_senti_unique = list(set(neg_senti_combined))
    
    for item in neg_senti_unique:
        senti_score_per_negation[item[0]].append(item[1])
    senti_neg_df = pd.DataFrame(list(senti_score_per_negation.values()), index=senti_score_per_negation.keys()).T
    
    fig, axs = plt.subplots(len(senti_neg_df.columns),figsize=(8,20), sharex=True)
   

    a=0
    import seaborn as sns 
    for negs in senti_neg_df.columns:
        sns.distplot(senti_neg_df[negs],bins=10,ax=axs[a], vertical=False,kde=False, label=negs)
        std = np.std(senti_neg_df[negs])
        mean = np.mean(senti_neg_df[negs])
        analysis = 'No. of Negations: ' + str(negs) + '\n Standard deviation: ' + str(format(std, ".2g")) + '\n Mean: ' + str(format(mean, ".2g"))
        axs[a].set_ylabel('Num_Paras')
        axs[a].set_xlabel('Sentiment Score')
        axs[a].text(0.98,0.60,analysis,
        verticalalignment='bottom', horizontalalignment='right',
        transform=axs[a].transAxes,
        fontsize=10)
        a+=1
    plt.savefig('Negs_'+ str(book_name), dpi=500)
    
    cor = correlation_between_negation_sentiment(paragraph_negation_list, paragraph_senti_list)
    cor = 'Correlation: '+ str(format(cor, ".3g"))


    # Plot number of negation and overall sentiment score of the paragraphs.
    plt.figure(figsize=(8,9))
    plt.tight_layout()
    
    #plt.style.use('seaborn-ticks')
    plt.plot(paragraph_senti_list,paragraph_negation_list,'o',markersize=10, alpha=.4)
    plt.ylabel('Negations detected in the paragraph ',fontsize=20)
    plt.xlabel('Sentiment Score of the paragraphs',fontsize=20)
    plt.title('Negation vs Sentiment: '+'"' + book_name + '"', fontsize=20)
    plt.text(.3,6.5, cor, style='italic',
        bbox={'facecolor': 'blue', 'alpha': 0.5, 'pad': 10},fontsize=12)
    plt.savefig(str(book_name), dpi=500)
    plt.show()
       
    return(paragraph_negation_list,paragraph_senti_list)


chapter_names, chapter_text, paragraph_text = read_war_of_the_worlds()   # analyze 1st book
book_name = "The War of the Worlds"    
paragraph_negation_list,paragraph_senti_list=plot_negation_sentiment(book_name, chapter_names, chapter_text, paragraph_text)
plot_negation(paragraph_negation_list,book_name)

chapter_names, chapter_text, paragraph_text = read_happy_go_lucky()      # analyze 2nd book
book_name = "Happy go lucky"    
paragraph_negation_list,paragraph_senti_list=plot_negation_sentiment(book_name, chapter_names, chapter_text, paragraph_text)
plot_negation(paragraph_negation_list,book_name)

#to calculate sum of negations in chapter 6
chapter_names, chapter_text, paragraph_text = read_happy_go_lucky() 
no_negations_chapter6=count_total_negative_occurence(5,chapter_names,chapter_text,paragraph_text)
sum(no_negations_chapter6)

