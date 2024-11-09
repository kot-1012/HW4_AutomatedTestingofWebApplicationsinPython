import pytest
import requests
import yaml
import logging

S = requests.Session()

with open("testdata.yaml", encoding='utf-8') as f:
    data = yaml.safe_load(f)
title = data.get("title")
description = data.get("description")
content = data.get("content")
addr_post = data.get("address_post")
url_post = data.get("url_post")
not_me_title = data.get("not_me_title")

def test_check_not_me_post(login):
    logging.info("Test check not me post started")
    res = S.get(url=url_post, headers={'X-Auth-Token': login}, params={'owner': 'notMe'}).json()['data']
    logging.debug(f"get request return: {res}")
    result_title = [i['title'] for i in res]
    assert not_me_title in result_title, 'Пост с заданным заголовком не найден'
    """assert str(not_me_title) in result_title, 'Пост с заданным заголовком не найден'"""

def test_create_post(login):
    logging.info("Test create post api started")
    url=addr_post
    headers={'X-Auth-Token': login}
    d={'title': title,
       'description': description,
       'content': content
       }
    res = S.post(url, headers=headers, data=d)
    logging.debug(f"Response is {str(res)}")
    assert str(res) == '<Response [200]>', "Новый пост не создан"


def test_check_description(login, get_description):
    logging.info("Test check description api started")
    url=url_post
    headers={'X-Auth-Token': login}
    res = S.get(url=url, headers=headers).json()['data']
    logging.debug(f"get request return: {res}")
    list_description = [i['description'] for i in res]
    assert data['description'] in list_description, 'check_post_create FAIL'

def test_send_email(email_sender):
    assert email_sender['To'] == 'kot-1012@mail.ru'


if __name__ == "__main__":
    pytest.main(["-vv"])