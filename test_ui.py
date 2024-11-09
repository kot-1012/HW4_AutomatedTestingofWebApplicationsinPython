from testpage import OperationHelper
import pytest
import logging
import yaml
import time

with open("testdata.yaml", encoding='utf-8') as f:
    testdata = yaml.safe_load(f)
name = testdata.get("login")
pswd = testdata.get("password")
title = testdata.get("title")
description = testdata.get("description")
content = testdata.get("content")
user = testdata.get("username")
email = testdata.get("user_email")
contact = testdata.get("content_contact")


def test_step1(browsser):
    logging.info("Test1 Starting")
    testpage = OperationHelper(browsser)
    testpage.go_to_site()
    testpage.enter_login("test")
    testpage.enter_pass("test")
    testpage.click_login_button()
    assert testpage.get_error_text() == "401", "Test FAILED!"


def test_step2(browsser):
    logging.info("Test2 Starting")
    testpage = OperationHelper(browsser)
    testpage.go_to_site()
    testpage.enter_login(name)
    testpage.enter_pass(pswd)
    testpage.click_login_button()
    assert testpage.get_user_text() == f"Hello, {name}", "Test FAILED!"


def test_step3(browsser):
    logging.info("Test3 Stsrting")
    testpage = OperationHelper(browsser)
    testpage.click_new_post_btn()
    testpage.enter_title(title)
    testpage.enter_description(description)
    testpage.enter_content(content)
    testpage.click_save_btn()
    time.sleep(3)
    assert testpage.get_res_text() == title, "Test FAILED!"


def test_step4(browsser):
    # test contact us
    logging.info("Test Contact_us Starting")
    testpage = OperationHelper(browsser)
    testpage.click_contact_link()
    testpage.enter_contact_name(user)
    testpage.enter_contact_email(email)
    testpage.enter_contact_content(contact)
    testpage.click_contact_send_btn()
    assert testpage.get_allert_message() == "Form successfully submitted", "Test FAILED!"


if __name__ == "__main__":
    pytest.main(["-vv"])