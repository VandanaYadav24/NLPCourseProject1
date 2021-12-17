from task1_textTiling import read_happy_go_lucky, read_war_of_the_worlds
from task2 import count_sentiment, count_paragraph_sentis, count_chapter_sentis
from textblob import TextBlob

import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

# identify no,no,none,niether in input text.
def count_negative_words(paragraph):
    negation_words_count=0
    tokens_para = word_tokenize(paragraph)
    lowercase_tokens_para = [t.lower() for t in tokens_para]
    counter_obj_para=Counter(lowercase_tokens_para)
    no_count=counter_obj_para['no']
    not_count=counter_obj_para['not']
    none_count=counter_obj_para['none']
    niether_count=counter_obj_para['niether']
    negation_words_count=no_count+not_count+none_count+niether_count
    return(negation_words_count)

#identify negative words which has prefix un,im,in,dis in input text.
def identify_prefix_negative_words(paragraph):
    prefixed_words_list=[]
    tokens = word_tokenize(paragraph)
    stop_words = set(stopwords.words('english'))
    tokens_updated = [w for w in tokens if not w in stop_words]
    i=0
    count_dis=0
    count_un=0
    count_in=0
    count_im=0
    for i in range(len(tokens_updated)):
        blob=TextBlob(tokens_updated[i])
        if(tokens_updated[i].startswith('dis') and blob.sentiment.polarity<0):
          prefixed_words_list.append(tokens_updated[i])
          count_dis+=1
        elif(tokens_updated[i].startswith('un') and blob.sentiment.polarity<0):
          prefixed_words_list.append(tokens_updated[i])
          count_un+=1
        elif(tokens_updated[i].startswith('in') and blob.sentiment.polarity<0):
          prefixed_words_list.append(tokens_updated[i])
          count_in+=1
        elif(tokens_updated[i].startswith('im') and blob.sentiment.polarity<0):
          prefixed_words_list.append(tokens_updated[i])
          count_im+=1
    #print(prefixed_words_list)
    negative_words_count=count_dis+count_un+count_in+count_im
    return(negative_words_count,prefixed_words_list)

#returns paragraph wise the occurance/count of negative words(no,no,none,niether & negative words which has prefix un,im,in,dis)
def count_total_negative_occurence(chapter_number,chapter_names,chapter_text,paragraph_text):
    total_count=[]
    specific_para_count=0
    total_list_of_prefix_words=[]
    i=0
    for paragraph in paragraph_text[chapter_number]:
        negation_words_count=count_negative_words(paragraph)
        negative_words_count,prefix_words_para_list=identify_prefix_negative_words(paragraph)
        specific_para_count=negation_words_count+negative_words_count
        total_count.append(specific_para_count)
        total_list_of_prefix_words.extend(prefix_words_para_list)
        #print("Count of prefix negation for chapter {}, '{}', paragraph {}: ".format(chapter_number, chapter_names[chapter_number], i), specific_para_count)
        i+=1
    return(total_count)

#chapter_names, chapter_text, paragraph_text = read_war_of_the_worlds() 
chapter_names, chapter_text, paragraph_text = read_happy_go_lucky()     # choose which book to analyze

list_negs=[]
for i in range(len(chapter_text)):  # for each chapter:
    list_negs.append(count_total_negative_occurence(i, chapter_names, chapter_text, paragraph_text))   # analyze paragraphwise

def plot_negation(paragraph_negation_list,book_name):
    plt.style.use('seaborn-ticks')
    plt.plot(paragraph_negation_list)
    plt.ylabel('Negations detected in the paragraph ')
    plt.xlabel('Paragraph Number')
    plt.title('Negations in a Paragraph: ' +'"'+ book_name + '"')
    plt.savefig(str(book_name)+' Negations', dpi=500)
    return None