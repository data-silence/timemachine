"""
Here you will find auxiliary functions that are used to operate the main classes and functions
Здесь находятся вспомогательные функции, которые используются для работы основных классов и функций
"""

from imports.imports import re, navec, np, dt, norm, pd
import logging


def get_clean_word(word: str) -> str:
    """
    Clearing words of unnecessary characters, bringing them to the requirements of the navec library
    Очистка слов от лишних символов, приведение к требованиям библиотеки navec
    """
    word = re.sub('[^a-zа-яё-]', '', word, flags=re.IGNORECASE)
    word = word.strip('-')
    return word


def news2emb(news: str) -> np.ndarray:
    """
    Sentence --> Embedding of sentence
    Getting sentence glove-embeddings using the Navec library of the Natasha project

    Получение эмбеддингов предложения с помощью библиотеки Navec проекта Natasha
    """
    news_clean = [get_clean_word(word) for word in news.split()]
    embeddings_list = []
    for word in news_clean:
        try:
            embeddings_list.append(navec[word.lower()])
        except KeyError:
            # Embedding the missing word is embedding unknown | если OOV, эмбеддинг = "unknown"
            embeddings_list.append(navec['<unk>'])
    news_emb = np.mean(embeddings_list, axis=0)
    return news_emb


def validate_user_date(user_date: str):
    try:
        final_date = dt.datetime.strptime(user_date, '%Y-%m-%d').date()
        if dt.datetime(2000, 8, 28) <= final_date <= dt.datetime(2021, 5, 31):
            return final_date
        else:
            logging.error(
                'Мы знаем новости за период с 28 августа 2000 года по 31 мая 2021, остальные нам не знакомы. '
                'Попробуйте ещё раз, пожалуйста')
    except ValueError:
        logging.error(
            'Мы понимаем дату в формате ГГГГ-ММ-ДД (например, "2015-06-20"). А вы где-то ошиблись, попробуйте ещё раз.')


def cos_simularity(a, b):
    cos_sim = np.dot(a, b) / (norm(a) * norm(b))
    return cos_sim


def find_sim_news(df: pd.DataFrame, user_sent: str):
    q_emb = news2emb(user_sent)
    df['sim'] = df['embeddings'].apply(lambda x: cos_simularity(q_emb, x))
    best_result = df[df.sim == df.sim.max()]
    return best_result

def pymorphy2_311_hotfix():
    from inspect import getfullargspec
    from pymorphy2.units.base import BaseAnalyzerUnit

    def _get_param_names_311(klass):
        if klass.__init__ is object.__init__:
            return []
        args = getfullargspec(klass.__init__).args
        return sorted(args[1:])

    setattr(BaseAnalyzerUnit, '_get_param_names', _get_param_names_311)