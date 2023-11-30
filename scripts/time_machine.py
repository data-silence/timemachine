"""
The main class News is implemented here to process and store news for a certain date
Attributes and methods of the class allow to get any information that the bot is intended to provide on request
Handlers (handlers) pass the bot user's requests to News, and take the results of news processing from here.

Здесь реализован основной класс News по обработке и хранению новостей на определенную дату
Атрибуты и методы класса позволяют получить любую информацию, которую предназначен выдавать бот по запросу
Обработчики (хэндлеры) передают в News запросы пользователя бота, и забирают отсюда результаты обработки новостей
"""

from imports.imports import DataBaseMixin, AgglomerativeClustering, time_machine, dt, pd, Counter, sns, plt, model_class
from scripts.utils import news2emb, find_sim_news


class News(DataBaseMixin):
    """
    A class for collecting and storing user news on a date from the past
    Класс для сбора и хранения пользовательских новостей на дату из прошлого
    """

    def __init__(self, date: dt.datetime.date):
        self.categories = ['technology', 'science', 'economy', 'entertainment', 'sports', 'society']
        self.categories_dict = {
            'economy': {'russian_title': 'экономика', 'emoj': '💰'},
            'science': {'russian_title': 'наука', 'emoj': '🔬'},
            'sports': {'russian_title': 'спорт', 'emoj': '🏃'},
            'technology': {'russian_title': 'технологии', 'emoj': '📲'},
            'entertainment': {'russian_title': 'общество', 'emoj': '👻'},
            'society': {'russian_title': 'политика', 'emoj': '👲'}
        }
        self.date = date
        self.date_news = self.set_date_news()
        self.categories_news_dict = {category: self.get_labeled_news(category) for category in self.categories}

    def set_date_news(self) -> list[dict]:
        """
        Gets news on a given date from the past
        Получает новости на заданную дату из прошлого
        """
        q = f"SELECT * FROM news WHERE date::date = '{self.date}' and agency = 'newsru.com'"
        date_news = DataBaseMixin.get(q, time_machine)
        return date_news

    def get_labeled_news(self, category: str) -> list[dict]:
        """
        Identifies news clusters using agglomerative clustering, assigns a cluster label to each news item
        Определяет с помощью агломеративной кластеризации кластеры новостей, присвает лейбл кластера каждой новости
        """
        category_news = [dict(news) for news in self.date_news if news['category'] == category]
        emb_list = [news2emb(news['news']) for news in category_news]

        if len(category_news) > 1:  # кластеризацию возможно сделать только если количество новостей более одной
            model = AgglomerativeClustering(n_clusters=None, metric='cosine', linkage='complete',
                                            distance_threshold=0.3)
            labels = model.fit_predict(list(emb_list))
            for news_number in range(len(category_news)):
                category_news[news_number]['label'] = labels[news_number]
                category_news[news_number]['embeddings'] = emb_list[news_number]
        elif len(category_news) == 1:  # если новость одна - присваиваем ей лейбл = -1
            category_news[0]['label'] = -1
            category_news[0]['embeddings'] = emb_list[0]

        return category_news

    def __getitem__(self, category: str):
        """
        Gives the news of the required category
        Позволяет получить новости категории, обращаясь к экземпляру класса как со словарём
        """
        if category in self.categories_dict:
            return self.categories_news_dict[category]
        else:
            raise ValueError(f"Нет такой категории. Вот доступные: {[key for key in self.categories_dict.keys()]}")

    def get_top_cluster_news(self, category: str, amount_news: int) -> list[list]:
        """"
        Selects the top-k largest news clusters of a given category, gives it as a list
        Выбирает top-k самых крупных кластеров новостей заданной категории, отдаёт его в виде списка
        """
        final_cluster_news = []
        result_cluster_news = []
        category_news = self.get_labeled_news(category)
        if category_news:
            most_popular = Counter(news['label'] for news in category_news).most_common(amount_news)
            for label in range(len(most_popular)):
                claster_news = [news for news in category_news if news['label'] == most_popular[label][0]]
                final_cluster_news.append(claster_news)

            for label in range(len(most_popular)):
                links = set()
                for news in final_cluster_news[label]:
                    temp_links = set(news['links'].split(','))
                    links.add(news['url'])
                    links = links.union(temp_links)
                max_lenght = max({len(news['news']) for news in final_cluster_news[label]})
                claster_news = [news for news in final_cluster_news[label] if len(news['news']) == max_lenght]
                claster_news[0]['result_links'] = links
                result_cluster_news.append(claster_news)
        return result_cluster_news

    def get_category_digest(self, amount_news: int = 3) -> str:
        """
        Transforms a list of the most popular news in categories retrieved by get_top_cluster_news into a digest
        Трансформирует в дайджест список самых популярных новостей в категориях, полученных get_top_cluster_news
        """
        category_digest = f'<b>🏎   {self.date.strftime("%d %B %Y")}   {"💨" * 3} </b>\n'

        for category in self.categories:
            category_cluster_news = self.get_top_cluster_news(category=category,
                                                              amount_news=amount_news)
            if category_cluster_news:
                category_digest += (f'\n<b>{self.categories_dict[category]["emoj"]} '
                                    f'{self.categories_dict[category]["russian_title"].title()}:</b>')
                for i, news in enumerate(category_cluster_news):
                    for el in range(len(news)):
                        current_news = f'\n{i + 1}. <a href="{news[el]["url"]}">{news[el]["title"]}</a>'
                        category_digest += current_news
                category_digest += '\n'
        return category_digest

    def plot_categories(self) -> None:
        """
        Creates and saves a graph of news distribution by category
        Создаёт и сохраняет график распределения новостей в разрезе категорий
        """
        sns.set(style="darkgrid")
        df = pd.DataFrame(self.date_news)
        my_plot = sns.countplot(x=df.category, palette='tab10', hue=df.category.values, legend=False)
        my_plot.set_title(
            f"Распределение {len(df)} новостей по категориям на {self.date.strftime('%d %B %Y')}:", fontsize=12)
        my_plot.set_xlabel("", fontsize=8)
        my_plot.set_ylabel("", fontsize=8)
        plt.savefig('./graphs/cat_distr.png')

    def get_best_news(self, user_news: str) -> str:
        """
        :param user_news: search query for news from a user | поисковый запрос новости от пользователя
        :return: the news most similar to a user request | новость, наиболее похожая на пользовательский запрос
        """
        result_news_list = []
        best_category = model_class.predict(user_news)[0][0].split('__')[-1]

        df = pd.DataFrame(self.categories_news_dict[best_category])
        best_news = find_sim_news(df, user_news)
        date_time, title, resume, link = (best_news.date.iloc[0].strftime("%H:%m"), best_news.title.iloc[0],
                                          best_news.resume.iloc[0], best_news.url.iloc[0])
        result_news_list.append('Определили категорию: \n' + self.categories_dict[best_category]['emoj'] + ' ' +
                                self.categories_dict[best_category]['russian_title'] + '\n')
        result_news_list.append(f'Самая близкая новость\n⌚ опубликована в {date_time}:\n')
        result_news_list.append(f'<a href="{link}">{title}</a>\n')
        result_news_list.append(resume)
        result_news = '\n'.join(result_news_list)
        return result_news
