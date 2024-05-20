# %%
import hashlib

import pandas
import requests
from pypinyin import Style, lazy_pinyin, pinyin

# %%
df = pandas.read_csv('./s.csv')
session = requests.session()
# 此处配置您的班级（API数据）
KLASS = {
    "name": "八五班",
    "description": "测试用途",
    "id": "664067094280280a6fbd0b10"
}
# 此处配置您的Token
TOKEN = ""
# %%


def generate_username(name: str) -> str:
    return ''.join(lazy_pinyin(name))


def generate_password(name: str) -> str:
    return ''.join([x[0] for x in pinyin(name, style=Style.FIRST_LETTER)])


# %%
for idx, ser in df.iterrows():
    name = ser['name']
    email = str(ser['qq']) + '@qq.com'

    # 创建对应用户
    user = session.post('http://asmre.api.xycode.club/user/register', json={
        'username': generate_username(name),
        'nickname': name,
        'avatar': f'https://cravatar.cn/avatar/{hashlib.md5(email.encode("utf-8")).hexdigest()}',
        'password': hashlib.sha1(generate_password(name).encode('utf-8')).hexdigest(),
    }).json()

    print(user)

    # 绑定学生
    student = session.post('http://asmre.api.xycode.club/student/', json={
        'name': name,
        'school_class': KLASS,
        'user': user
    }, cookies={
        'xyuan-token': TOKEN
    }).json()

    print(student)

# %%
