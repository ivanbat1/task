# coding: utf-8
import pyautogui
from selenium import webdriver
import time
def click_t(name = 'EURUSD'):
    driver = webdriver.Remote(
        command_executor='http://localhost:9999',
        desired_capabilities={
            "app": r"C:\Program Files (x86)\InstaTrader\terminal.exe"})
    time.sleep(10)
    driver.find_element_by_name('{},H4'.format(name)).click()
    pyautogui.keyDown('alt')
    pyautogui.press('t')
    pyautogui.keyUp('alt')
click_t()