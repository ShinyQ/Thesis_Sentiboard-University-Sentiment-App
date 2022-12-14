from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count
from django.conf import settings

from sentiment.twitter import get_tweets
from sentiment.models import Sentiment

from transformers import AutoModelForSequenceClassification, Trainer
from transformers import AutoTokenizer

from wordcloud import WordCloud
from datetime import date
from os.path import exists

import matplotlib.pyplot as plt
import pandas as pd
import logging
import json
import re
import os

plt.switch_backend('Agg') 

db_logger = logging.getLogger('db')
file_exists = exists(f'{os.path.join(os.path.dirname(__file__))}/IndoBERT/pytorch_model.bin')

classifier = AutoModelForSequenceClassification.from_pretrained('ShinyQ/Sentiboard')
tokenizer = AutoTokenizer.from_pretrained("indobenchmark/indobert-base-p2")
model = Trainer(model=classifier)

def preprocessing(text):
    # Inisialisasi Dataset Stopword 
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()

    # Inisialisasi Dataset Kata Baku
    kata_baku = pd.read_csv(f'{os.path.join(os.path.dirname(__file__))}/kamus_baku.csv')
    kata_baku = kata_baku.set_index("kataAlay")["kataBaik"].to_dict()

    text = str(text)

    # Mengubah setiap kata menjadi lowercase
    text = text.lower()

    # Menghapus Link Dengan Pattern http/https dan www
    text = re.sub(r'http\S+', '', text)
    text = re.sub('(@\w+|#\w+)', '', text)

    # Menghapus Tag HTML
    text = re.sub('<.*?>', '', text)

    # Menghapus Karakter Selain Huruf a-z dan A-Z
    text = re.sub('[^a-zA-Z]', ' ', text)

    # Mengganti baris baru (enter) dengan spasi
    text = re.sub("\n", " ", text)

    # Menghapus Spasi Yang Lebih Dari Satu
    text = re.sub('(s{2,})', ' ', text)

    # Menghapus kata yang mengandung judul topik dan kata yang terdapat pada stopwords indonesia
    temp_text_split=[]
    final_text=[]
    text_split=text.split(' ')

    # Merubah setiap kata menjadi baku dan filter kata harus >= 2
    custom_word = ['ptn', 'telyu', 'telkom', 'university']

    for i in range(len(text_split)):
        if text_split[i] not in custom_word:
            if text_split[i] in kata_baku:
                text_split[i] = kata_baku[text_split[i]]

            if len(list(str(text_split[i]))) >= 2:  
                temp_text_split.append(str(text_split[i]))

    for i in range(len(temp_text_split)):
        final_text.append(str(temp_text_split[i]))
    
    text = ' '.join(final_text)
    text = stopword.remove(text)
    
    return str.lstrip(str.rstrip(text))


def generate_wordcloud(sentiments, title):
    if(len(sentiments) != 0):
        unique_string=(" ").join(sentiments)
        wordcloud = WordCloud(width = 1000, height = 500, background_color="white").generate(unique_string)

        plt.figure(figsize=(15,8))
        plt.imshow(wordcloud)
        plt.axis("off")

        plt.savefig(os.path.join(settings.BASE_DIR, f'./static/sentiment/Wordcloud/{title}.png'), bbox_inches='tight')


@login_required
def dashboard(request):
    month = request.GET.get('month')
    year = request.GET.get('year') if request.GET.get('year') != None else str(date.today().year)

    # Query Dan Proses Untuk Mendapatkan Perhitungan Total Sentimen  Berdasarkan Tanggal
    counter = Sentiment.objects

    if month:
        counter = counter.filter(month=month)
    if year:
        counter = counter.filter(year=year)
    
    counter = counter.extra({
        'created_at': "date(created_at)"
    }).values('created_at').distinct().annotate(Count('created_at'))

    dates = []
    dates_counter = []

    for i in counter:
        dates.append(i['created_at'])
        dates_counter.append(i['created_at__count'])

    # Query Contoh Sentimen Setiap Label
    neg_sentiment = Sentiment.objects.filter(label = 2)
    neu_sentiment = Sentiment.objects.filter(label = 0)
    pos_sentiment = Sentiment.objects.filter(label = 1)

    if month:
        neg_sentiment = neg_sentiment.filter(month=month)
        pos_sentiment = pos_sentiment.filter(month=month)
        neu_sentiment = neu_sentiment.filter(month=month)
    if year:
        neg_sentiment = neg_sentiment.filter(year=year)
        pos_sentiment = pos_sentiment.filter(year=year)
        neu_sentiment = neu_sentiment.filter(year=year)
        

    # Query Mendapatkan Data Unik Bulan Dan Tahun
    months = list(Sentiment.objects.values_list('month', flat=True).distinct())
    years = list(Sentiment.objects.values_list('year', flat=True).distinct())

    # Query Untuk Word Cloud
    sentiments = Sentiment.objects
    full_sentiments = list(sentiments.values_list('preprocessing', flat=True)) 

    title = '/Word'

    if month:
        sentiments = sentiments.filter(month=month)
        title = title + '-' + month
    if year:
        sentiments = sentiments.filter(year=year)
        title = title + '-' + year
   
    sentiments = list(sentiments.values_list('preprocessing', flat=True))

    # Membuat Word Cloud Keseluruhan
    generate_wordcloud(full_sentiments, 'Word')

    # Membuat Word Cloud Berdasarkan Filter
    if month is None:
        generate_wordcloud(sentiments, title)
    elif month not in months:
        pass
    else:
        generate_wordcloud(sentiments, title)

    context = {}

    context['page_name'] = "Dashboard Sentiment"
    context['negative'] = neg_sentiment
    context['positive'] = pos_sentiment
    context['neutral'] =  neu_sentiment

    context['dates_counter'] = dates_counter
    context['dates'] = dates
    context['months'] = months
    context['years'] = years
    
    context['filter_year'] = year
    context['filter_month'] = month
    context['filter_wordcloud'] = '/sentiment/Wordcloud' + title + '.png'
    context['filter_wordcloud_check'] = os.path.exists('./static/' + context['filter_wordcloud'])

    if month:
        context['filter'] = True

    db_logger.info('load sentiment page')

    return render(request, "sentiment/sentiment.html", context)


@login_required
def manage(request):
    result = Sentiment.objects

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date') if request.GET.get('end_date') != '' else str(date.today())
    label = request.GET.get('label')

    if label != None and label != '':
        result = result.filter(label=label)

    if start_date == None and end_date == None:
        result = result.all()
    else:
        if start_date or end_date:
           if start_date == '':
             result = result.filter(created_at__lte=end_date)
           else:
             result = result.filter(created_at__range=[start_date, end_date])
           
    
    context = {}
    context['page_name'] = "Halaman Kelola Sentiment"
    context['results'] = result

    db_logger.info('load manage sentiment page')
    return render(request, "sentiment/kelola.html", context)


@login_required
def delete_sentiment(request): 
    if request.method == 'DELETE':
        data = json.loads(request.body)
        id = data.get('id')

        sentiment = Sentiment.objects.filter(pk=id) 
        sentiment.delete()
    else:
        return JsonResponse({
            'code': 404, 
            'status': 'not found',
        })

    return JsonResponse({
        'code': 200, 
        'status': 'success',
        'message': 'sukses menghapus data sentimen'
    })


@login_required
def crawl(request):
    context = {}
    context['page_name'] = "Halaman Crawl Sentimen Sosial Media"

    db_logger.info('load crawl sentiment page')
    return render(request, "sentiment/crawl.html", context)


@login_required
def crawl_tweets(request):
    data = None

    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query', None)
        data = get_tweets(query)
        
        for i in range(0, len(data)):
            data[i]['preprocessing'] = preprocessing(data[i]['text'])
            
            tokenize = tokenizer(data[i]['preprocessing'], padding='max_length', max_length=256)
            logits = model.predict([tokenize]).predictions
            predicted = logits.argmax(1)[0]
            
            data[i]['sentiment'] = int(predicted)

        return JsonResponse({
            'code': 200, 
            'status': 'success',
            'data': data
        }) 

    return JsonResponse({
        'code': 404, 
        'status': 'not found',
        'data': []
    }) 


@login_required
def crawl_save(request):
    if request.method == 'POST':
        dataset = json.loads(request.body)
        dataset = dataset.get('tweets')

        result = []

        for data in dataset:
            tweets = dataset.get(str(data))
            tweets = json.loads(tweets)
            
            if tweets['text'] != '' and tweets['preprocessing'] != '':
                obj_sentiment = Sentiment(
                    text=tweets['text'],
                    preprocessing=tweets['preprocessing'], 
                    label=tweets['sentiment'],
                    created_at=tweets['created_at'],
                    month=tweets['month'],
                    year=tweets['year']
                )

                result.append(obj_sentiment)

        Sentiment.objects.bulk_create(result, ignore_conflicts=True)

        return JsonResponse({
            'code': 200, 
            'status': 'success',
            'data': []
        }) 

    return JsonResponse({
        'code': 404, 
        'status': 'not found',
        'data': []
    })  