from github.PaginatedList import PaginatedList
from github.Repository import Repository
from github.Issue import Issue
from github import Github
import logging
import json
import sys

logging.basicConfig(level=logging.INFO)

# 获取 GitHub token
ACCESS_TOKEN = sys.argv[1]

# 连接到 GitHub API
github = Github(ACCESS_TOKEN)

# 获取存储库
repo: Repository = github.get_repo('YangRucheng/XTU-Health-Submit')

# 获取所有开放的问题
issues: PaginatedList = repo.get_issues(state='open')


# 处理Issue
with open('roster.json', 'r', encoding='utf-8')as fr:
    roster: list[dict] = json.load(fr)

for index, issue in enumerate(issues):
    issue: Issue = issue
    try:
        logging.info(f"{index+1}. {issue.title}\n{issue.body}")
        lines = issue.body.splitlines()
        assert (
            len(lines) >= 3
            and issue.title.strip() == lines[0].strip()
            and lines[0].isdigit()
            and len(lines[1].strip()) > 0
            and len(lines[2].strip()) > 0
            and lines[2].isdigit()
        ), "Issue格式错误"
        assert (
            len([x for x in roster if x.get('stId') == lines[0].strip()]) == 0
        ), "学号重复"
        stId = issue.title.strip()
        stName = lines[1].strip()
        stMobile = lines[2].strip()
    except Exception as e:
        logging.error(f"Error! {e}")
        issue.create_comment(f"Error! {e}\n已关闭Issue, 你可以修改后重新打开此Issue!")
    else:
        roster.append({
            "stId": stId,
            "stName": stName,
            "stMobile": stMobile
        })
        logging.info(f"Success!")
        issue.create_comment(f"Success! 成功添加到名单! 自动锁定Issue!")
        issue.lock("resolved")
    finally:
        issue.edit(state="closed")

with open("roster.json", 'w') as fw:
    json.dump(roster, fw, indent=4, ensure_ascii=False)
