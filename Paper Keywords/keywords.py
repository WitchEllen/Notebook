# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import re
import os
from tqdm import tqdm
import nltk

from nltk.corpus import stopwords
from collections import Counter

nltk.download('stopwords')

stopwords_deep_learning = set([
    'without', 'with', 'using', 'via', 'to', 'toward', 'towards', 'beyond',
    'based', 'method', 'methods', 'approach', 'model', 'models', 'modeling',
    'algorithm', 'algorithms', 'function', 'functions', 'policy', 'framework',
    'structure', 'structured', 'architecture', 'system', 'machine', 'visual',
    'image', 'images', 'label', 'labels', 'data', 'feature', 'features',
    'aware', 'object', 'effect', 'learning', 'training', 'evaluation',
    'prediction', 'analysis', 'inference', 'process', 'processes', 'problems',
    'deep', 'nerual', 'neural', 'network', 'networks', 'deep neural',
    'neural network', 'deep neural network'
])

stopwords_set = set(stopwords.words('english')) | stopwords_deep_learning


def keyWordVis(file_name, output, num_keyword=0):

    title_list = []
    with open(file_name, 'r', encoding='UTF-8') as f:
        for line in tqdm(f):
            line = line.strip()
            if line:
                title_list.append(line)

    print("The number of total accepted paper titles : ", len(title_list))
    keyword_list = []

    for title in title_list:
        # split '?' ':' ' '
        word_list = re.split('[\?: ]', title)
        word_list = list(filter(lambda x: x, word_list))

        # split '-' and extend
        for word in word_list:
            words = word.split('-')
            if len(words) > 1:
                word_list.extend(words)

        # remove stopwords
        for word in word_list:
            word = word.lower()
            if word not in stopwords_set:
                keyword_list.append(word)

    keyword_counter = Counter(keyword_list)
    print(keyword_counter)

    print('{} different keywords before merging'.format(len(keyword_counter)))

    # Merge duplicates s
    duplicates = set()
    for k in keyword_counter:
        if k + 's' in keyword_counter:
            duplicates.add(k)
    for k in duplicates:
        keyword_counter[k] += keyword_counter[k + 's']
        del keyword_counter[k + 's']

    print('{} different keywords after merging'.format(len(keyword_counter)))
    print(duplicates)
    with open(output + '.txt', 'a', encoding='utf-8') as key_info:
        key_info.write(str(keyword_counter))

    # Show N most common keywords and their frequencies
    if num_keyword == 0:
        num_keyword = 50  # FIXME
    keywords_counter_vis = keyword_counter.most_common(num_keyword)

    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(10, 10), dpi=150)

    key = [k[0] for k in keywords_counter_vis]
    value = [k[1] for k in keywords_counter_vis]
    y_pos = np.arange(len(key))
    ax.barh(y_pos,
            value,
            align='center',
            color='green',
            ecolor='black',
            log=True)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(key, rotation=0, fontsize=10)
    ax.invert_yaxis()
    for i, v in enumerate(value):
        ax.text(v + 2, i + 0.5, str(v), color='black', fontsize=10)
    ax.set_xlabel('Frequency')
    ax.set_title(output.split('/')[-1] + ' Top {}'.format(num_keyword))
    # plt.show()
    plt.savefig(output + '.png')

    return keyword_counter


if __name__ == '__main__':
    for file_name in os.listdir('./list'):
        output = file_name.split('.')[0] + '-keywords'
        keyWordVis('./list/' + file_name, './keywords/' + output)
