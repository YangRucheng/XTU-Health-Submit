import logging
import asyncio
import random
import httpx
import json
import sys

logging.basicConfig(level=logging.INFO)

USER_ID_STR = sys.argv[1]
USER_ID: list = json.loads(USER_ID_STR)


async def main(roster: list[dict]) -> list:
    """ 健康打卡 """
    taskList = []
    async with httpx.AsyncClient(http2=True, verify=False) as client:
        for human in roster:
            task = asyncio.create_task(post(human, client))
            taskList.append(task)
        return await asyncio.gather(*taskList)


async def post(data: dict, client: httpx.AsyncClient) -> None:
    """ 提交POST请求 """
    url = "https://app.xiaoyuan.ccb.com/channelManage/outbreak/addOutbreak"
    default = {
        "schoolId": "10530",
        "userId": random.choice(USER_ID),
        "isFever": "0",
        "nowStatus": "5",
        "nowArea": "The People's Republic of China",
        "remarks": "Auto Health Submit By GitHub https://github.com/YangRucheng/XTU-Health-Submit",
        "isVaccinate": "1",
        "vaccineType": "2",
        "injectTimes": "3",
        "stMobile": str(random.randint(1000, 9999))
    }
    name: str = data.get('stId')
    try:
        resp = await client.post(url, json=default | data, cookies={'Powered By': 'YRC'})
        res: dict = resp.json()
        assert res.get('status') in [0], res.get('msg')
    except (Exception, BaseException) as e:
        logging.warning(f"{name} 打卡失败 {e}")
    else:
        logging.info(f"{name} 打卡成功 {res.get('msg')}")


if __name__ == "__main__":
    with open('roster.json', 'r', encoding='utf-8')as fr:
        roster = json.load(fr)
    asyncio.run(main(roster))
