from github import Github
from typing import Union
import os

# 获取 GitHub token
ACCESS_TOKEN: Union[str, None] = os.environ.get('ACCESS_TOKEN')

# 连接到 GitHub API
g = Github(ACCESS_TOKEN)

# 获取存储库
repo = g.get_repo('YangRucheng/XTU-Health-Submit')

# 获取所有开放的问题
issues = repo.get_issues(state='open')

# 处理每个问题
for issue in issues:
    # 在控制台打印问题标题和网址
    print(f'Title: {issue.title}')
    print(f'URL: {issue.html_url}')
