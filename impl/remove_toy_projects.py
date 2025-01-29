import csv
import requests
import json
import os
import shutil


# get meta-deta of repositories
def get_stars(urls):
    with open(urls, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            url = row[0].rstrip()


            new_url = url.replace('github.com', 'api.github.com/repos')


            print(new_url)

            # add your github token to Bearer
            user_data = requests.get(new_url,
                                     headers={'Authorization': f'Bearer {os.getenv("TOKEN")}',
                                              'Accept': 'application/vnd.github.mercy-preview+json'}).json()
                                              
            if (user_data["stargazers_count"] >= 100):
                with open("out.txt", "a+") as outfile:
                    outfile.write(f"{user_data["name"]},{user_data["html_url"]}\n")

                # with open(file_path, 'w+', encoding='utf-8') as outfile:
                #     json.dump(user_data, outfile, ensure_ascii=False, indent=4)


# check if specific keywords are in the topics, description, or label of the repositories
def filter_toys():
    parent_dir = './helpers/topics/'
    keywords = ['example', 'demo', 'tutorial', 'playground', 'learn', 'teach', 'exercise', 'course', 'practice',
                'template', 'sample', 'workshop', 'lecture', 'study']
    remove_ids = set()
    for x in os.listdir(parent_dir):
        file_path = parent_dir + x
        file_id = x.split('.json')[0]
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                for keyword in keywords:
                    # if keyword is in the label of the repository
                    if keyword in file_id.split('_', 1)[1]:
                        remove_ids.update([file_id])
                    try:
                        if keyword in data['description']:
                            remove_ids.update([file_id])
                        if keyword in data['topics']:
                            remove_ids.update([file_id])
                    except TypeError:
                        pass
        except UnicodeDecodeError as ude:
            print(x + ' ude')

    wtr = csv.writer(open('remove_ids.csv', 'w'), delimiter=',', lineterminator='\n')
    wtr.writerow(['Project_id'])
    for i in remove_ids:
        wtr.writerow([i])


# remove projects by id
def remove_toy_projects(project_ids):
    parent_dir = './filtered_repos/'
    with open(project_ids, 'r') as file:
        rows = csv.reader(file)
        next(rows, None)
        for row in rows:
            repo_dir = parent_dir + row[0]
            print(repo_dir)
            if os.path.isdir(repo_dir):
                shutil.rmtree(repo_dir, ignore_errors=True)

# ----------------------------- MAIN --------------------------------------


get_stars('project_urls.csv')
filter_toys()
remove_toy_projects('remove_ids.csv')
