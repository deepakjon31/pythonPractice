import os
import re
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, abort
# from datetime import datetime, timedelta
from bokeh.resources import INLINE
from bokeh.plotting import figure
from bokeh.embed import components
# from bokeh.io import output_notebook, show, output_file
from bokeh.util.string import encode_utf8
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
from nltk.probability import FreqDist
from stop_words import get_stop_words
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from models import Query, get_feature_query


company_features = ['Jobs', 'Employees', 'Investors', 'Funding']
analysis_feature = ['Twitter', 'Facebook']
path = os.path.abspath(os.path.dirname(__file__))
images_name = ['static/images/most_tags.png', 'static/images/most_mentions.png', 'static/images/words_count.png']

app = Flask(__name__)

c = []
ana = []
p_tweetss = []
ne_tweetss = []
ng_tweetss = []


@app.route('/')
def index():
    query = Query()
    company = query.get_company()
    query.close()
    return render_template('home.html', data=enumerate(company))


@app.route('/company/<company>', methods=['GET', 'POST'])
def companydetail(company):
    feature = None
    header = []
    company_name = ''

    if isinstance(company, str):
        if '[' in company and ']' in company:
            start = company.index('[')
            end = company.index(']')
            company_name = company[start+2:end-1]
        if ',' in company:
            compani = company.replace('(', '').replace(')', '').replace(',', '').replace("'", '').split()
            print("com list", compani, len(compani))
            feature = compani[-1].strip()
        else:
            company_name = company
    c.clear()
    c.append(company_name)
    ana.append(company_name)
    print("Feature", feature, "company name", company_name, "list:", c)
    feature_query = ''
    if feature is not None:
        feature_query, header = get_feature_query(feature, company_name.lower())

    else:
        feature = ''
    for image in images_name:
        if os.path.exists(image):
            os.remove(image)
    print('Deepak', company)
    if '[' not in company or ',' not in company:
        try:
            company_name = company.lower()
            print(company_name)
            about_company = get_feature_query('about', company_name)

            feature_job, job_header = get_feature_query('job', company_name)
            feature_investor, investor_header = get_feature_query('investor', company_name)
            feature_fund, fund_header = get_feature_query('fund', company_name)
            feature_emp, emp_header = get_feature_query('employee', company_name)

            ########## Funds Plot #####################
            df_fund = pd.DataFrame(feature_fund, columns=fund_header[0])
            df_fund.iloc[:, 2] = (pd.to_datetime(df_fund.iloc[:, 2]))
            df_fund = df_fund.sort_values(by='fund_date')
            df_fund.iloc[:, 1] = df_fund.iloc[:, 1].apply(lambda x: x.replace('$', '').replace(',', ''))
            df_fund['fund_raised'] = pd.to_numeric(df_fund.fund_raised)
            fig_fund = figure(x_axis_type="datetime", plot_height=250, plot_width=300, toolbar_location=None, title='Funds')
            fig_fund.line(df_fund.iloc[:, 2], df_fund.iloc[:, 1], color='navy', alpha=0.5)
            fig_fund.toolbar.logo = None
            fig_fund.xgrid.grid_line_color = None
            fig_fund.yaxis.major_label_orientation = 1

            js_resources = INLINE.render_js()
            css_resources = INLINE.render_css()
            script, div = components(fig_fund)

        except Exception as e:
            print(e)
            return abort(404)

        else:
            html = render_template('company_d.html', feature_names=company_features, current_feature_name=feature,
                                   analysis_feature=analysis_feature, plot_script_f=script, plot_div_f=div,
                                   js_resources=js_resources, css_resources=css_resources, about=about_company[0])
            return encode_utf8(html)

    return render_template('company.html', feature_names=company_features, current_feature_name=feature,
                           feature_query=enumerate(feature_query), header=header, analysis_feature=analysis_feature)


@app.route('/company/', methods=['GET', 'POST'])
def company():
    feature = request.args.get("company_detail")
    company_name = ''
    try:
        company_name = c[-1]
        # c.clear()
    except IndexError:
        return redirect(url_for('custom_error'))
    print(company_name)

    return redirect(url_for('companydetail', company=([company_name], feature)))


def clean_tweet(tweet):
    import re
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def analyze_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1


def common_words(data):
    tweets = data['status_text'].str.lower().str.cat(sep=' ')
    tweets = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweets).split())
    tweets_remove_pun = re.sub('[^A-Za-z]+', ' ', tweets)
    stop_words = list(get_stop_words('en'))
    nltk_words = list(stopwords.words('english'))
    stop_words.extend(nltk_words)

    word_tokens_tweets = word_tokenize(tweets_remove_pun)
    filtered_sentence_tweet = [w_tweet for w_tweet in word_tokens_tweets if w_tweet not in stop_words]

    without_single_chr_tweet = [word_tweet for word_tweet in filtered_sentence_tweet if len(word_tweet) > 2]

    cleaned_data_tweet = [word_tweet for word_tweet in without_single_chr_tweet if not word_tweet.isnumeric()]

    word_dist_tags = FreqDist(cleaned_data_tweet)
    rslt_tweet = pd.DataFrame(word_dist_tags.most_common(100), columns=['Word', 'Frequency'])
    # print(rslt_tweet)
    generate_wordcloud(cleaned_data_tweet, 'words_count')
    # wc(cleaned_data_tweet) # wordcloud image
    return rslt_tweet, word_dist_tags


def generate_wordcloud(data, filename):
    filename = f"static\images\{filename}.png"
    data = ' '.join(data)
    wc = WordCloud(background_color="white", height=250, max_words=10, max_font_size=50, stopwords=set(STOPWORDS)).generate(data)
    if os.path.exists(filename):
        os.remove(filename)
    wc.to_file(filename)


def hastags_mentions(df):
    tags = []
    for tag in df.hashtags:
        if ',' in tag:
            tag = tag.split(',')
            if len(tag) > 0:
                for i in tag:
                    if len(i) > 1:
                        tags.append(i.strip())
    generate_wordcloud(tags, 'most_tags')
    mentions = []
    for mention in df.mentions:
        if ',' in mention:
            mention = mention.split(',')
            if len(mention) > 0:
                for i in mention:
                    if len(i) > 1:
                        mentions.append(i.strip())
    generate_wordcloud(mentions, 'most_mentions')
    tags = FreqDist(tags)
    mentions = FreqDist(mentions)
    return tags, mentions


def plot_bar_chart(categorical, categorical_value):
    fig = figure(x_range=categorical, plot_height=250, plot_width=400, title="Word Counts", tools="")
    fig.xgrid.grid_line_color = None
    # fig.xaxis.axis_label = "Words"
    # fig.yaxis.axis_label = "Counts"
    fig.toolbar.logo = None
    fig.toolbar_location = None
    fig.y_range.start = 0
    fig.xaxis.major_label_orientation = 1
    fig.vbar(x=categorical, width=0.4, top=categorical_value, color='navy')
    return fig


def positive_tweets(df):
    return [tweet for i, tweet in enumerate(df.status_text) if df['SA'][i] > 0]


def neutral_tweets(df):
    return [tweet for i, tweet in enumerate(df.status_text) if df['SA'][i] == 0]


def negative_tweets(df):
    return [tweet for i, tweet in enumerate(df.status_text) if df['SA'][i] < 0]


def read_tweets(tweets, header_tweets):
    df = pd.DataFrame(tweets, columns=header_tweets[0])
    df['SA'] = np.array([analyze_sentiment(tweet) for tweet in df.status_text])
    return df


@app.route('/analysis', methods=['GET','POST'])
def sentanalysis():
    print('company name analysis:', ana[-1])

    if len(ana) > 1:
        temp = ana[-1]
        ana.clear()
        ana.append(temp)


    analysis_type = request.url
    if 'twitter' in analysis_type.lower():
        company_name = ana[-1]
        try:
            tweeter_user = get_feature_query('tweeter_url', company_name.lower())
            if 'twitter' in tweeter_user:
                tweeter_user = tweeter_user.split('/')[-1].strip().lower()
            tweets, header_tweets = get_feature_query('twittertweets', tweeter_user)
        except Exception as e:
            print(e)
            return redirect(url_for('custom_error'))
        else:
            df = read_tweets(tweets, header_tweets)
            p_tweets = positive_tweets(df)
            ne_tweets = neutral_tweets(df)
            ng_tweets = negative_tweets(df)
            tags, mentions = hastags_mentions(df)
            common, word_dist_tags = common_words(df)
            tweet_length = len(df['status_text'])
            pos_tweet = round(len(p_tweets) * 100 / tweet_length, 2)
            neu_tweet = round(len(ne_tweets) * 100 / tweet_length, 2)
            neg_tweet = round(len(ng_tweets) * 100 / tweet_length, 2)

            categorical = common.Word.values.tolist()[:10]
            categorical_value = common.Frequency.values.tolist()[:10]
            fig = plot_bar_chart(categorical, categorical_value)

            df_tag = pd.DataFrame(list(tags.items()), columns=['word', 'count'])
            df_tag = df_tag.sort_values(by='count', ascending=False)
            tags_cate = df_tag.word.values.tolist()[:10]
            tags_value = df_tag['count'].values.tolist()[:10]
            fig_tag = plot_bar_chart(tags_cate, tags_value)

            df_men = pd.DataFrame(list(mentions.items()), columns=['word', 'count'])
            df_men = df_men.sort_values(by='count', ascending=False)
            mention_cate = df_men.word.values.tolist()[:10]
            mention_value = df_men['count'].values.tolist()[:10]
            fig_men = plot_bar_chart(mention_cate, mention_value)

            js_resources = INLINE.render_js()
            css_resources = INLINE.render_css()

            script, div = components(fig)
            script_1, div_1 = components(fig_men)
            script_2, div_2 = components(fig_tag)
            p_tweetss.clear()
            ne_tweetss.clear()
            ng_tweetss.clear()
            p_tweetss.append(p_tweets)
            ne_tweetss.append(ne_tweets)
            ng_tweetss.append(ng_tweets)

            html = render_template('charts.html', pos_tweet=pos_tweet, neu_tweet=neu_tweet, neg_tweet=neg_tweet, tags=tags,
                                   mentions=mentions, word_dist_tags=word_dist_tags, js_resources=js_resources,
                                   css_resources=css_resources, plot_script=script, plot_div=div, plot_script_1=script_1,
                                   plot_div_1=div_1, plot_script_2=script_2, plot_div_2=div_2)
            return encode_utf8(html)

    if 'facebook' in analysis_type.lower():
        return redirect(url_for('custom_error'))


@app.route('/get_user_detail')
def get_user_detail():
    print("get_user_details", ana[-1])
    company_name = ana[-1]
    tweeter_user = get_feature_query('tweeter_url', company_name.lower())
    if 'twitter' in tweeter_user:
        tweeter_user = tweeter_user.split('/')[-1].strip().lower()
    user_detail = get_feature_query('twitteruser', tweeter_user)
    print(user_detail)
    return render_template('user_detail.html', user_detail=user_detail, user=company_name)


@app.route('/pos-tweets')
def pos_tweets():
    return render_template('pos_tweets.html', pos_tweets=enumerate(p_tweetss[0]))


@app.route('/neg-tweets')
def neg_tweets():
    return render_template('neg_tweets.html', neg_tweets=enumerate(ng_tweetss[0]))


@app.route('/neu-tweets')
def neu_tweets():
    return render_template('nue_tweets.html', neu_tweets=enumerate(ne_tweetss[0]))


@app.route('/error')
def custom_error():
    return render_template('custom_error.html', error='Something went wrong :(')


@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
