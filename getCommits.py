import sys, subprocess, os, time
from github import Github
import pandas as pd

'''
Usage: ./getCommits.py <repo_name> <repo_path>
'''
repo_name = 'mongodb/mongo'
repo_path = '../../../Documents/GitHub/mongo'

print(os.path.abspath(repo_path))

# repo_name = sys.argv[1]
# repo_path = sys.argv[2]
g = Github("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")

df = pd.DataFrame(columns=['SHA', 'Message', 'Committer_date', 'Patch_path'])
#print(dir)

# Search for commits that have "fix" in the message, meaning this commit fixed an issue
# Note that we use different years to bypass the rate limit
year = 2020
while (year < 2021):
    year += 1
    commits = g.search_commits(
        query='repo:mongodb/mongo committer-date:' + str(year) + '-01-01..' + str(year) + '-12-31',
        sort='committer-date', order='asc')
    counter = 0
    for commit in commits:
        counter += 1
        if g.get_rate_limit().search.remaining < 2:
            print(g.get_rate_limit().search.remaining)
            time.sleep(10)
        message = commit.commit.message
        #print("+++" + message)
        sha = commit.sha
        print(sha)
        committer_date = commit.commit.committer.date

        dir = os.getcwd()
        patch_path = dir + '/Patches/mongo/' + sha + '.patch'
        print(sha)
        print(patch_path)

        # Output the patch in a separate file
        command = 'cd ' + repo_path + ' && ' + 'git diff ' + sha + '~1 ' + sha + ' > ' + patch_path
        subprocess.check_output(command, shell=True).decode("utf-8")

        # subprocess.check_output('cd ' + repo_path, shell=True).decode("utf-8")
        # subprocess.check_output('git diff ' + sha + '~1 ' + sha + ' > ' + patch_path, shell=True).decode("utf-8")
        # subprocess.check_output('cd -', shell=True).decode("utf-8")

        new_df = pd.DataFrame(
            [{'SHA': sha, 'Message': message, 'Committer_date': committer_date, 'Patch_path': patch_path}])
        df = pd.concat([df, new_df], ignore_index=True)
print(df)
#df.to_csv('../summerThing/tables/commits_2019_APACHE.csv')
