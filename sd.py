import yake
def extractkeywords(text,numOfKeywords=5):
    language = "en"
    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    # numOfKeywords = 5
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)
    summary=""
    ks=[]

    for kw in keywords:
        sd=0
        for m in ks:
            if kw[0] in m:
                sd=sd+1
        if sd==0:
            ks.append(kw[0])
            summary=summary+" "+kw[0]+"."

    print(summary)

    return summary
