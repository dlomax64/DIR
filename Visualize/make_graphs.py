import os
from matplotlib import scale
import numpy as np
from numpy.core.fromnumeric import size
import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sbn
sbn.set()

# Common languages between the datasets.
languages = [
    "c",
    "c++",
    "java",
    "javascript",
    "java",
    "python",
    "php",
    "ruby",
    "r",
    "swift",
    "scala",
    "kotlin"
]

# JS frameworks to be counted as js. 
frameworks = [
    'angular',
    'react',
    'nodejs',
    'express'
]

def clean_languages(array):
    ''' Clean the timeline data to fit with the jobs data 

        Parameter: 
        array: np.array to be cleaned.

        Returns:
        Dataframe with shape {language, count}
    '''

    languages_dict = {l: 0 for l in languages}
    languages_dict['c/c++'] = 0

    languages_dict.pop('c', None)
    languages_dict.pop('c++', None)


    ret = {
        "Languages":[],
        "Count": []
    } 

    for data in array:
        if data == 'C/C++':
            languages_dict['c/c++']+=1
        else:
            words = data.lower().split(' ')
            
            for w in words:
                if w in languages_dict:
                    languages_dict[w]+=1
    
    for key, value in languages_dict.items():
        ret["Languages"].append(key)
        ret["Count"].append(value) 

    return pd.DataFrame.from_dict(ret)

if __name__ == "__main__":
    plot_dir = os.path.abspath(os.path.dirname(__file__)) + '/plots/'

    job_data_dir = os.path.abspath(os.path.dirname(
        __file__)) + "/../JobSearchScraping/data/"
    total_keywords_cities = "total_keywords_cities.csv"
    total_keywords_states = "total_keywords_states.csv"

    states_keyword_df = pd.read_csv(
        f"{job_data_dir}{total_keywords_states}", sep=',')
    cities_keyword_df = pd.read_csv(
        f"{job_data_dir}{total_keywords_cities}", sep=',')

    sorted_states_languages = states_keyword_df.loc[states_keyword_df["TOP KEYWORDS OVERALL (41074 JOBS)"].isin(
        languages)].sort_values("COUNT")
    sorted_cities_languages = cities_keyword_df.loc[cities_keyword_df["TOP KEYWORDS OVERALL (27242 JOBS)"].isin(
        languages)].sort_values("COUNT")

    # Add framework counts to javascript counts. 
    states_frameworks = states_keyword_df.loc[states_keyword_df["TOP KEYWORDS OVERALL (41074 JOBS)"].isin(
        frameworks)].sort_values("COUNT")
    cities_frameworks = cities_keyword_df.loc[cities_keyword_df["TOP KEYWORDS OVERALL (27242 JOBS)"].isin(
        frameworks)].sort_values("COUNT")

    old_js = sorted_states_languages.loc[sorted_states_languages["TOP KEYWORDS OVERALL (41074 JOBS)"] == 'javascript', 'COUNT']
    new_js = old_js + states_frameworks['COUNT'].sum()

    sorted_states_languages.loc[sorted_states_languages["TOP KEYWORDS OVERALL (41074 JOBS)"] == 'javascript', 'COUNT'] = new_js
    sorted_states_languages = sorted_states_languages.sort_values("COUNT")

    author_data_dir = os.path.abspath(
        os.path.dirname(__file__)) + "/../Authors/"
    timeline = "timeline.txt.gz"

    timeline_df = pd.read_csv(
        f"{author_data_dir}{timeline}", compression='gzip')

    earliest_languages = clean_languages(timeline_df["Earliest Language"]).sort_values("Count")
    latest_languages = clean_languages(timeline_df["Latest Language"]).sort_values("Count")

    # Make Charts.
    jobs_languages = sorted_states_languages["TOP KEYWORDS OVERALL (41074 JOBS)"].to_numpy()
    jobs_y = sorted_states_languages["COUNT"].to_numpy()

    earliest_x = earliest_languages["Languages"].to_numpy()
    earliest_y = earliest_languages["Count"].to_numpy()

    latest_x = latest_languages["Languages"].to_numpy()
    latest_y = latest_languages["Count"].to_numpy()

    plt.figure(figsize=(10, 8))
    plt.bar([x for x in range(len(jobs_languages))], jobs_y)
    plt.xticks([x for x in range(len(jobs_languages))], jobs_languages, rotation=75)
    plt.title("Keywords for Languages in Job Postings")
    plt.ylabel("Number of appearances in job postings")
    plt.savefig(f"{plot_dir}jobs_bar.png")

    plt.clf()
    plt.figure(figsize=(10, 8))
    plt.bar([x for x in range(len(earliest_x))], earliest_y, color='purple')
    plt.xticks([x for x in range(len(earliest_x))], earliest_x, rotation=75)
    plt.title("Language Appearance in First Commit")
    plt.ylabel("Number of Appearances")
    plt.savefig(f"{plot_dir}earliest_bar.png")

    plt.clf()
    plt.figure(figsize=(10, 8))
    plt.bar([x for x in range(len(latest_x))], latest_y, color='orange')
    plt.xticks([x for x in range(len(latest_x))], latest_x, rotation=75)
    plt.title("Language Appearance in Latest Commit")
    plt.ylabel("Number of Appearances")
    plt.savefig(f"{plot_dir}latest_bar.png")

    plt.clf()
    plt.figure(figsize=(10, 8))
    plt.bar([x for x in range(len(earliest_x))], earliest_y, color='purple', label='Earliest', alpha=.5)
    plt.bar([x for x in range(len(latest_x))], latest_y, color='orange', label='Latest', )
    plt.legend(prop={'size': 20})
    plt.xticks([x for x in range(len(latest_x))], latest_x, rotation=75)
    plt.title("Language Appearance in Latest Commit")
    plt.ylabel("Number of Appearances")
    plt.savefig(f"{plot_dir}overlaid_bar.png")

    # Pie Time. I like pie.
    jobs_labels = sorted_states_languages["TOP KEYWORDS OVERALL (41074 JOBS)"].to_numpy()[-5:]
    jobs_sizes = sorted_states_languages["COUNT"].to_numpy()[-5:]
    jobs_sizes = np.true_divide(jobs_sizes, jobs_sizes.sum(keepdims=True))*100

    earliest_labels = earliest_languages["Languages"].to_numpy()[-5:]
    earliest_sizes = earliest_languages["Count"].to_numpy()[-5:]
    earliest_sizes = np.true_divide(earliest_sizes, earliest_sizes.sum(keepdims=True))*100

    latest_labels = latest_languages["Languages"].to_numpy()[-5:]
    latest_sizes = latest_languages["Count"].to_numpy()[-5:]
    latest_sizes = np.true_divide(latest_sizes, latest_sizes.sum(keepdims=True))*100

    plt.clf()
    plt.figure(figsize=(10, 8))
    plt.pie(jobs_sizes, labels=jobs_labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 16})
    plt.title("Job Keywords", fontsize=20)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(f"{plot_dir}jobs_pie.png")

    plt.clf()
    plt.figure(figsize=(10, 8))
    plt.pie(earliest_sizes, labels=earliest_labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 16})
    plt.title("Earliest Commits", fontsize=20)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(f"{plot_dir}earliest_pie.png")

    plt.clf()
    plt.figure(figsize=(10, 8))
    plt.pie(latest_sizes, labels=latest_labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 16})
    plt.title("Latest Commits", fontsize=20)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(f"{plot_dir}latest_pie.png")

    plt.clf()
    plt.cla()
    plt.close()

    java_jobs = [.2, .2, 0, 0, 0]
    java_timeline = [.2, .2, 0, 0, 0]

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(10, 8)

    _, j_labels, j_percents = ax1.pie(jobs_sizes, labels=jobs_labels, autopct='%1.1f%%', startangle=90, explode=java_jobs, textprops={'fontsize': 16})
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.title.set_text("Keywords")
    ax1.title.set_size(20)

    _, e_labels, e_percents = ax2.pie(earliest_sizes, labels=earliest_labels, autopct='%1.1f%%', startangle=90, explode=java_timeline, textprops={'fontsize': 16})
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax2.title.set_text("Commits")
    ax2.title.set_size(20)

    j_percents[0].set_visible(False)
    j_percents[1].set_visible(False)
    j_percents[2].set_visible(False)
    j_percents[3].set_visible(False)
    j_percents[4].set_visible(False)
    j_labels[3].set_visible(False)
    j_labels[4].set_visible(False)

    e_percents[0].set_visible(False)
    e_percents[1].set_visible(False)
    e_percents[2].set_visible(False)
    e_percents[3].set_visible(False)
    e_percents[4].set_visible(False)
    e_labels[3].set_visible(False)
    e_labels[4].set_visible(False)

    fig.tight_layout(pad=3.0)
    plt.savefig(f"{plot_dir}other_languages.png")

    js_jobs = [0, 0, 0, .2, .2]
    js_timeline = [0, 0, 0, .2, .2]

    ax1.clear()
    ax2.clear()

    _, j_labels, j_percents = ax1.pie(jobs_sizes, labels=jobs_labels, autopct='%1.1f%%', startangle=90, explode=js_jobs, textprops={'fontsize': 20})
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.title.set_text("Keywords")
    ax1.title.set_size(20)

    _, e_labels, e_percents = ax2.pie(earliest_sizes, labels=earliest_labels, autopct='%1.1f%%', startangle=90, explode=js_timeline, textprops={'fontsize': 20})
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax2.title.set_text("Commits")
    ax2.title.set_size(20)

    e_percents[0].set_visible(False)
    e_percents[1].set_visible(False)
    e_percents[2].set_visible(False)
    e_labels[0].set_visible(False)
    e_labels[1].set_visible(False)
    e_labels[2].set_visible(False)

    j_percents[0].set_visible(False)
    j_percents[1].set_visible(False)
    j_percents[2].set_visible(False)
    j_labels[0].set_visible(False)
    j_labels[1].set_visible(False)
    j_labels[2].set_visible(False)

    fig.tight_layout(pad=3.0)
    plt.savefig(f"{plot_dir}js_vs_java.png")