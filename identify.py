import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from nltk.tokenize import WhitespaceTokenizer
from nltk.probability import FreqDist

tokenizer = WhitespaceTokenizer()
stop_words = stopwords.words('english')

FILE = r'C:\Users\kumadee\Desktop\assignment1-find_top_keywords\NewsArticles_Top10Keywords.csv'
df = pd.read_csv(FILE)

articles = []
for article in range(df.shape[0]):
    raw_article = re.sub('[^a-zA-Z]', ' ', df.title[article] + ' ' + df.content[article]) #Eliminating other than alphabet
    articles.append(raw_article)

raw_tokens = tokenizer.tokenize(' '.join(articles))
bigram_finder = BigramCollocationFinder.from_words(raw_tokens)
bigrams = bigram_finder.nbest(BigramAssocMeasures.likelihood_ratio, 1000)
for bigram_tuple in bigrams:
    x = "%s %s" % bigram_tuple
    raw_tokens.append(x)

tokens = []
for t in raw_tokens:
    if t.lower() not in stop_words and len(t) > 2:
        tokens.append(t.lower()) 

text = nltk.Text(tokens)
dist = FreqDist(text)
top_ten = dist.most_common(10)



















import pandas as pd
import nltk
import re
# from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

FILE = r'C:\Users\kumadee\Desktop\assignment1-find_top_keywords\NewsArticles_Top10Keywords.csv'

df = pd.read_csv(FILE)

# news_article = df.iloc[:, 1].values + df.iloc[:, 2].values

corpus = []
ps = PorterStemmer()

# =============================================================================
# for i in range(df.shape[0]):
#     news_article = re.sub('[^a-zA-Z]', ' ', df.title[i] + ' ' + df.content[i])
#     news_article = news_article.lower()
#     news_article = news_article.split()
#     stopword_set = set(stopwords.words('english'))
#     news_article = [ps.stem(word) for word in news_article if not word in stopword_set]
#     news_article = ' '.join(news_article)
#     corpus.append(news_article)
# =============================================================================
    

from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from nltk.tokenize import WhitespaceTokenizer
from nltk.probability import FreqDist

tokenizer = WhitespaceTokenizer()
stopwords = set(nltk.corpus.stopwords.words('english'))

def tokeniz(string):
    tokens = tokenizer.tokenize(string)
    bigram_finder = BigramCollocationFinder.from_words(tokens)
    bigrams = bigram_finder.nbest(BigramAssocMeasures.likelihood_ratio, 1000)

    for bigram_tuple in bigrams:
        x = "%s %s" % bigram_tuple
        tokens.append(x)
    for t in tokens:
        if t not in stopwords and len(t) > 1:
            corpus.append(t)


for article in range(df.shape[0]):
    raw_article = re.sub('[^a-zA-Z]', ' ', df.title[article] + ' ' + df.content[article])
    # raw_article = df.title[article] + ' ' + df.content[article]
    tokeniz(raw_article.lower())







articles = []
for article in range(df.shape[0]):
    raw_article = re.sub('[^a-zA-Z]', ' ', df.title[article] + ' ' + df.content[article])
    # raw_article = df.title[article] + ' ' + df.content[article]
    articles.append(raw_article)

news_articles = ' '.join(articles)

raw_tokens = tokenizer.tokenize(' '.join(articles))

bigram_finder = BigramCollocationFinder.from_words(news_articles)
bigrams = bigram_finder.nbest(BigramAssocMeasures.likelihood_ratio, 1000)

for bigram_tuple in bigrams:
    x = "%s %s" % bigram_tuple
    raw_tokens.append(x)
    

ar = df.title[0] + ' ' + df.content[0]

ar = re.sub('[^a-zA-Z]', ' ', ar)
tok = tokenizer.tokenize(ar)

bigram_finder = BigramCollocationFinder.from_words(tok)
bigrams = bigram_finder.nbest(BigramAssocMeasures.likelihood_ratio, 1000)

for bigram_tuple in bigrams:
    x = "%s %s" % bigram_tuple
    tok.append(x)








print(raw_article)
print(type(raw_article))

tokens = []
raw_tokens = WhitespaceTokenizer().tokenize(raw_article)


stopwords = nltk.corpus.stopwords.words('english')
for t in raw_tokens:
    if t.lower() not in stopwords:
        tokens.append(t.lower())

raw_text = nltk.Text(raw_tokens)
text = nltk.Text(tokens) 
vocab = sorted(set(text))
dist = FreqDist(text)


bigram_messures = BigramAssocMeasures()
bigram_collection = BigramCollocationFinder.from_words(raw_article)
# bigram_collection.apply_freq_filter(3)
bigrams = bigram_collection.nbest(bigram_messures.likelihood_ratio, 1000)

deepak = []

for x in bigrams:
    # print(' '.join(x))
    print('%s %s' % x)
    raw_tokens.append(' '.join(x))
    
dist1 = FreqDist(nltk.Text(deepak))

dd = tokens + deepak
