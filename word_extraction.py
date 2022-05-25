# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
#
# nltk.download('stopwords')
# stop_words = set(stopwords.words('english'))
# list=["is","i","I","always","the","for","to","by","in","he","she","his","her","their","him","can","could","would","it","be","they","are","was","is","that","this","thus","may","might","were","as","but","if","and","also","as well as", "moreover","furthermore",
# "besides","in addition","because","so","therefore","thus","consequently","as a result of","next","then","first","second","finally",
# "meanwhile","after","whereas","instead of","alternatively","otherwise","unlike","on the other hand","in contrast","however","notably",
# "most of all","for example","such as","for instance","as revealed by","in the case of","as shown by", "equally","in the same way","like","similarly'", "likewise","as with", "as compared with","all","a","such","suppose","with","very"]
#
#
# ss=word_tokenize("He/She is a very thoughtful teacher who puts a lot of thought into how he/she presents the material. His/Her lessons were engaging, useful, and he/she was very patient with everyone in class always encouraging his/her students to try. I would highly recommend him/her to anyone interested in learning")
# # print(ss)
# filtered_sentence = []
#
# for w in ss:
#     if w not in stop_words:
#         filtered_sentence.append(w)
#
# # print(ss)
# # print(filtered_sentence)
# ls=[]
# for i in filtered_sentence:
#     if i not in list:
#
#         ls.append(i)
#
# ls=ls.(".")
# print(ls)
#
#
from transformers import pipeline
data="He/She is a very thoughtful teacher who puts a lot of thought into how he/she presents the material. His/Her lessons were engaging, useful, and he/she was very patient with everyone in class always encouraging his/her students to try. I would highly recommend him/her to anyone interested in learning"
summ=pipeline("summarization")
summed=summ(data,min_length=75,max_length=300)
print(summed)