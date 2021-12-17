from task1_textTiling import read_happy_go_lucky, read_war_of_the_worlds
from task7 import LDA_for_book
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.corpus import stopwords
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation, strip_numeric
from collections import Counter


#For a given topic represented by its 30 to 40 words identified by the LDA, check each individual chapter, 
#and select the chapter that contains the highest number of occurrence of these words. 
#Then in the next round, repeat this process for the wording of next topic when the matching is performed over all chapter 
#except the one that has already been assigned. 

#method for counting keywords of specific topic for individual chapter
def check_individual_chapter(chapter, topic_num, lda_topics):
    tokens = word_tokenize(chapter)
    stop_words = set(stopwords.words('english'))
    tokens_updated = [w for w in tokens if not w in stop_words]
    counter_obj=Counter(tokens_updated)
    temp=0
    topics = []
    filters = [lambda x: x.lower(), strip_punctuation, strip_numeric]
    for topic in lda_topics:
        topics.append(preprocess_string(topic[1], filters))
    for j in range(35):
        chapter_count=counter_obj[topics[topic_num][j]]
        chapter_count=chapter_count+temp
        temp=chapter_count
    return(chapter_count)

#this method returns the list containing chapter number for each topic
def identify_chapter_num_for_topics(chapter_names, chapter_text, lda_topics):
    topic_chapter_list=[]
    #chapter_wise count for a specific topic
    chapter_wise=[]
    max_count_index_list=[]
    max_count_index=70 #chosen greater than numner of chapters in both book
    #check that chapter is assigned to a topic already
    for num in range(len(lda_topics)):
        chapter_wise.clear()
        for i in range(len(chapter_names)):
            if(not(i in max_count_index_list)):
                chapter_count=check_individual_chapter(chapter_text[i], num, lda_topics)
                chapter_wise.append(chapter_count)
            else:
                chapter_wise.append(0) 
        #print(chapter_wise)
        max_count=max(chapter_wise)
        max_count_index=chapter_wise.index(max_count)
        max_count_index_list.append(max_count_index)
        #append max_count_index+1(chapter number) to topic_chapter_list which defines topics with their corresponding chapter numbers
        topic_chapter_list.append(max_count_index+1)
    return(topic_chapter_list)

chapter_names, chapter_text, paragraph_text = read_war_of_the_worlds() 
lda_topics=LDA_for_book(chapter_names, chapter_text, paragraph_text, "The War of the Worlds")
topic_chapter_list_book1=identify_chapter_num_for_topics(chapter_names, chapter_text, lda_topics)
print("\nChapter number for each topic:")
print(topic_chapter_list_book1)

chapter_names, chapter_text, paragraph_text = read_happy_go_lucky()
lda_topics=LDA_for_book(chapter_names, chapter_text, paragraph_text, "Happy go lucky")
topic_chapter_list_book2=identify_chapter_num_for_topics(chapter_names, chapter_text, lda_topics)
print("\nChapter number for each topic:")
print(topic_chapter_list_book2)

