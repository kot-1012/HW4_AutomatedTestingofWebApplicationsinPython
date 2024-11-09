import yaml
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import logging
import requests

with open("testdata.yaml", encoding='utf-8') as f:
    testdata = yaml.safe_load(f)
    browser = testdata["browser"]


@pytest.fixture(scope="session")
def browsser():
    if browser == "firefox":
        service = Service(executable_path=GeckoDriverManager().install())
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(service=service, options=options)
    else:
        service = Service(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

S = requests.Session()

@pytest.fixture()
def login():
    try:
        result = S.post(url=testdata['url_login'], data={'username': testdata['login'], 'password': testdata['password']})
        response_json = result.json()
        token = response_json.get('token')
    except:
        logging.exception("Get token exception")
        token = None
    logging.debug(f"Return token success")
    return token

@pytest.fixture()
def get_description():
    return 'Some description for test'

@pytest.fixture(scope="session")
def email_sender():
    with open("testdata.yaml", encoding='utf-8') as f:
        testdata = yaml.safe_load(f)

    fromaddr = testdata.get("fromaddr")
    toaddr = testdata.get("toaddr")
    mypass = testdata.get("fromaddr_passwd")
    reportname = "log.txt"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Отчет по тестированию"

    with open(reportname, "rb") as log:
        part = MIMEApplication(log.read(), Name=reportname)
        part['Content-Disposition'] = f'attachment; filename="{reportname}"'
        msg.attach(part)

    letter = "Отчет о тестировании"
    msg.attach(MIMEText(letter, "plain"))

    server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
    server.login(fromaddr, mypass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    return msg

