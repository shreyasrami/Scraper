from selenium import webdriver
import time
import csv
import os
import pandas as pd
from csv import writer


def get_nft_rarity(slp_sec: int, total: int, nft: str, site: str):

    filename = nft + "_rarity.csv"
    file_path = 'nft_csv/' + filename

    url = site + nft
    PATH = "C:\Program Files (x86)\chromedriver.exe"

    driver = webdriver.Chrome(PATH)
    driver.get(url)
    time.sleep(slp_sec)

    el = driver.find_element_by_xpath("//main[@class='mx-0 sm:mx-0 py-6 sm:pt-6 sm:pb-8 px-6 sm:px-6 lg:px-6 flex-1 relative sm:overflow-y-auto focus:outline-none bg-gray-100 dark:bg-transparent']")
    driver.execute_script("arguments[0].scrollIntoView();", el)

    i = 0
    while i <= total:
        elements = driver.find_elements_by_xpath("//div[@class='group relative bg-white bg-opacity-95 rounded-lg flex flex-col overflow-hidden shadow-mr-card-shadow dark:shadow-mr-card-shadow-dark dark:bg-mr-black-currant']")
        driver.execute_script("arguments[0].scrollIntoView();", elements[-4])
        i = i + 9
        time.sleep(slp_sec)

    nft_no = driver.find_elements_by_xpath("//div[@class='group relative bg-white bg-opacity-95 rounded-lg flex flex-col overflow-hidden shadow-mr-card-shadow dark:shadow-mr-card-shadow-dark dark:bg-mr-black-currant']//span[@x-text='name']")
    rarity_rank = driver.find_elements_by_xpath("//div[@class='group relative bg-white bg-opacity-95 rounded-lg flex flex-col overflow-hidden shadow-mr-card-shadow dark:shadow-mr-card-shadow-dark dark:bg-mr-black-currant']//span[@x-text='rank']")
    rarity_percent = driver.find_elements_by_xpath("//div[@class='group relative bg-white bg-opacity-95 rounded-lg flex flex-col overflow-hidden shadow-mr-card-shadow dark:shadow-mr-card-shadow-dark dark:bg-mr-black-currant']//div[@class='w-9/12 text-right whitespace-nowrap overflow-hidden text-ellipsis']")

    rr1 = []
    rr2 = []
    rr3 = []

    for i in nft_no:
        cnt = i.text.count(' ')
        try:
            rr1.append(int(i.text.split()[cnt].split('#')[1]))
        except IndexError:
            rr1.append(i.text.rsplit(' ', 1)[0])

    for j in rarity_rank:
        rr2.append(int(j.text))

    for k in rarity_percent:
        rr3.append(k.text)

    driver.quit()

    li = list(zip(rr1, rr2, rr3))

    print(str(len(li)) + " NFT Rarities Fetched")

    heading = ['#Number', 'Rarity Rank', 'Rarity Percent']

    with open(file_path, 'w', encoding='utf-8', newline="") as f:
        w_obj = writer(f)
        headers = csv.DictWriter(f, fieldnames=heading)
        headers.writeheader()

        for i, j, k in li:
            w_obj.writerow([i, j, k])

        f.close()

    return li


def get_nft_details(slp_sec: int, total: int, pages: int, nft: str, site: str):
    url = "https://magiceden.io/marketplace/" + nft
    PATH = "C:\Program Files (x86)\chromedriver.exe"

    driver = webdriver.Chrome(PATH)
    driver.get(url)
    time.sleep(slp_sec)
    prev_height = driver.execute_script('return document.body.scrollHeight')

    j = 0
    while j <= pages:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        time.sleep(slp_sec)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == prev_height:
            break
        prev_height = new_height
        j = j + 1

    nm = driver.find_elements_by_xpath(
        "//div[@class='tw-flex tw-flex-initial flex-column tw-p-3 tw-pb-0']//h6[@class='mb-0 tw-truncate grid-card__title tw-font-bold tw-leading-none !tw-text-sm']")
    pr = driver.find_elements_by_xpath(
        "//div[@class='tw-flex tw-flex-initial flex-column tw-p-3 tw-pb-0']//div[@class='tw-flex tw-items-center tw-gap-1']//span[@class='tw-truncate']")

    ds1 = []
    ds2 = []
    ds3 = []

    for i in nm:
        cnt = i.text.count(' ')
        try:
            ds1.append(i.text.split()[cnt].split('#')[1])
        except IndexError:
            ds1.append(i.text.rsplit(' ', 1)[0])

    for j in pr:
        ds2.append(j.text.split()[0])

    driver.quit()

    fn = nft + "_rarity.csv"
    fp = 'nft_csv/' + fn

    if os.path.isfile(fp):
        pass
    else:
        get_nft_rarity(1, total, nft, site)

    df = pd.read_csv(fp)

    try:
        for k in ds1:
            df_temp = df.loc[df['#Number'] == int(k)]
            ds3.append(df_temp.iloc[0, :]['Rarity Rank'])
    except IndexError:
        print("NFT Number " + str(k) + " not found in the rarity list !!")
    else:
        di = dict(zip(ds1, list(zip(ds2, ds3))))
        details = dict(sorted(di.items(), key=lambda item: float(item[1][0])))

        print(str(len(details)) + " NFT Marketplace Details Fetched")

        filename = nft + ".csv"
        file_path = 'nft_csv/' + filename

        if os.path.isfile(file_path):
            os.remove(file_path)

        heading = ['#Number', 'Price', 'Rarity Rank']

        with open(file_path, 'w', encoding='utf-8', newline="") as f:
            w_obj = writer(f)
            headers = csv.DictWriter(f, fieldnames=heading)
            headers.writeheader()

            for i, (j, k) in details.items():
                w_obj.writerow([i, j, k])

            f.close()

        return details


print(get_nft_details(2, 101, 2, "ai_ufos", "https://moonrank.app/collection/"))
