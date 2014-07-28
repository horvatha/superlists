#!/usr/bin/env python3
# coding: utf-8

"""functional_test for Test Driven Program Development by Harry Percival
"""

from selenium import webdriver
browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title
