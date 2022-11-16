
import os
import pandas as pd

def main():

    # -----------------------------------------------
    # 1.1

    print("\n\n1.1\n\n-----------------------------------------------")

    movie_data = pd.read_csv(os.path.dirname(__file__) + r"/movie_metadata.csv")

    #-----------------------------------------------
    # 1.2

    print("\n\n1.2\n\n-----------------------------------------------")

    print(movie_data.isna().sum())

    # "duration" has 15 missing values

    # -----------------------------------------------
    # 1.3

    print("\n\n1.3\n\n-----------------------------------------------")

    duration_median = movie_data['duration'].median()
    print(duration_median) # = 103.0

    movie_data = movie_data.fillna({"duration":duration_median})

    # -----------------------------------------------
    # 1.4

    print("\n\n1.4\n\n-----------------------------------------------")

    duration_mean = round(movie_data['duration'].mean(), 2)
    print(duration_mean) # = 107.18857822724569, or 107.19

    # -----------------------------------------------
    # 1.5

    print("\n\n1.5\n\n-----------------------------------------------")

    categories_column = []

    for index, row in movie_data.iterrows():

        current_duration = float(row["duration"])

        if current_duration < 90:
            categories_column.append("1. <90")

        elif current_duration >= 90 and current_duration <= 120:
            categories_column.append("2. 90–120")

        # current_duration > 120
        else:
            categories_column.append("3. >120")

    movie_data["movie_duration_category"] = categories_column

    print(movie_data) # there it is! :)

    # -----------------------------------------------
    # 1.6

    print("\n\n1.6\n\n-----------------------------------------------")

    movie_data_2000 = movie_data
    print(movie_data)

    movie_data_2000 = movie_data_2000[movie_data_2000["title_year"] >= 2000]
    print(movie_data)

    movie_data_2000 = movie_data_2000[["title_year", "movie_duration_category"]]

    movie_data_2000.groupby(by=["title_year"]).sum()

    print(movie_data_2000)

    years = movie_data_2000["title_year"].unique()
    print(years)

    categories_count = []

    for i in range(len(years)):
        categories_count.append([0, 0, 0])

    for index, row in movie_data_2000.iterrows():

        current_year = row['title_year']
        category = row['movie_duration_category']

        for i in range(len(years)):

            if str(current_year) == str(years[i]):

                if category == "1. <90":
                    categories_count[i][0] = categories_count[i][0] + 1
                elif category == "2. 90–120":
                    categories_count[i][1] = categories_count[i][1] + 1
                else:
                    categories_count[i][2] = categories_count[i][2] + 1

    # rows = "years" list
    # columns = "1. <90", "2. 90–120", "3. >120"

    for i in range(0, len(years)):
        years[i] = str(years[i])

    print(years)
    summary_dataframe = pd.DataFrame(categories_count, index=years, columns=["1. <90", "2. 90–120", "3. >120"])

    print(summary_dataframe)

    # -----------------------------------------------
    # 1.7

    print("\n\n1.7\n\n-----------------------------------------------")

    movies_cat2_2008 = summary_dataframe['2. 90–120'][2008]
    print(movies_cat2_2008) # = 160

    # -----------------------------------------------
    # 1.8

    print("\n\n1.8\n\n-----------------------------------------------")

    plot_type = []

    for index, row in movie_data.iterrows():

        current_plot = str(row["plot_keywords"]).replace("|", " ")

        if ("love" in current_plot) and ("death" in current_plot):
            plot_type.append("love_and_death")
        elif ("love" in current_plot):
            plot_type.append("love")
        elif ("death" in current_plot):
            plot_type.append("death")
        else:
            plot_type.append("other")

    movie_data["movie_plot_category"] = plot_type

    print(movie_data)

    # -----------------------------------------------
    # 1.9

    print("\n\n1.9\n\n-----------------------------------------------")

    count_love = 0
    count_death = 0
    count_love_and_death = 0
    count_others = 0

    sum_love = 0
    sum_death = 0
    sum_love_and_death = 0
    sum_others = 0


    for index, row in movie_data.iterrows():
        category = str(row["movie_plot_category"])
        score = float(row["imdb_score"])

        if category == "love_and_death":
            count_love_and_death = count_love_and_death + 1
            sum_love_and_death = sum_love_and_death + score

        elif category == "love":
            count_love = count_love + 1
            sum_love = sum_love + score

        elif category == "death":
            count_death = count_death + 1
            sum_death = sum_death + score

        else:
            count_others = count_others + 1
            sum_others = sum_others + score

    avg_love_death = sum_love_and_death/count_love_and_death
    avg_death = sum_death/count_death
    avg_love = sum_love/count_love
    avg_others = sum_others/count_others

    '''
                        avg_rating
    "love_and_death"        x
    "love"                  y
    "death"                 z
    "other"                 k
    
    '''

    summary_dataframe2 = pd.DataFrame([avg_love_death, avg_death, avg_love, avg_others], index=["love_and_death", "death", "love", "other"], columns=["average_imdb_score"])
    print(summary_dataframe2)

    # -----------------------------------------------
    # 1.10

    print("\n\n1.10\n\n-----------------------------------------------")

    avg_love_end = round(float(summary_dataframe2["average_imdb_score"]["love"]), 2)
    print(avg_love_end) # = 6.58

    # -----------------------------------------------
    # 1.11

    print("\n\n1.11\n\n-----------------------------------------------")

    print(movie_data['budget'])

    movie_data["budget"] = movie_data["budget"].apply(lambda budget: budget[:-3])

    print(movie_data['budget'])

    movie_data['budget'] = movie_data['budget'].astype('int64')

    budget_median = int(movie_data['budget'].median())
    print(budget_median) # = 15000000

    # -----------------------------------------------


if __name__ == '__main__':
    main()

