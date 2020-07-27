from wordcloud import WordCloud
import matplotlib.pyplot as plt

from nltk.tokenize import TweetTokenizer
import tweepy
import nltk
import re



# consumer_key = 'xxx'
# consumer_secret = 'xxx'
# access_token = 'xxx'
# access_token_secret = 'xxx'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

perfil = 'user_name'

# função que lida com a paginação(cursor) e os possíveis erros retornados pela API
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError as e:
            print(e.reason)
            time.sleep(60*15)
            continue
        except tweepy.TweepError as e:
            if e.reason == "Not authorized.":
                print(e.reason)
                break
            else:
                print(e.reason)
                break
        except StopIteration:
            break

# recebe um user_name e a quantidade máxima de tweets desejada
# retorna dois parâmetros, primeiro uma lista com os tweets de um user e segundo a quantidade de tweets
def get_tweets_user(user, quantidade_maxima):
    tweets = []
    cont = 0
    for follower in limit_handled(tweepy.Cursor(api.user_timeline, screen_name=perfil, count=200, tweet_mode='extended').items()):
        tweets.append(follower.full_text)
        cont += 1
        if cont == quantidade_maxima:
            break
    return tweets, cont

# recebe uma lista de textos e retorna uma lista de textos limpos prontos para análise
def clean_data(texts):

    # lista que vai amazenar os textos limpos
    result = []

    for text in texts:

        # remove toda url | remove 'RT' | remove pontuação | remove \n | substitui onde tem dois espaços em branco por um só
        pattern = r'http\S+|RT @\S+|[^\w\s]|\n'
        clean_text = re.sub(pattern, ' ', text)
        clean_text = clean_text.lower()

        # remove stopwords

        # objeto que tokeniza os tweets
        # reduce_len=True -> reduz quanditade de caracteres duplicados
        # strip_handles=True -> remove menções a usuários do tweet
        # preserve_case=False -> deixa tudo em minúsculo
        tweet_tokenizer = TweetTokenizer(reduce_len=True)
        tokens = tweet_tokenizer.tokenize(clean_text)

        #Palavras que não agregam informações para serem tiradas
        stopwords = nltk.corpus.stopwords.words('portuguese')

        # filtra as stopwords
        tokens_without_sw = [word for word in tokens if not word in stopwords]
        clean_text = " ".join(tokens_without_sw)
        result.append(clean_text)

    return result


tweets, quantidade = get_tweets_user(perfil, 1000)

tweets_limpos = clean_data(tweets)
# print(tweets_limpos)


# Cria e exibe a nuvem de palavras
wordcloud = WordCloud(max_font_size=60, max_words=50, background_color="white").generate(" ".join(tweets_limpos))
# wordcloud.to_file(imagem_nuvem)
# Mostra a imagem gerada
plt.figure()
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
