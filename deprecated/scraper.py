# import requests
# from bs4 import BeautifulSoup

# # URL = "https://realpython.github.io/fake-jobs/"
# target_URL = "https://www.target.com/s?searchTerm=kinky+hair"
# page = requests.get(target_URL)

# print(page.text) 
# #  .text is raw HTML code

# soup = BeautifulSoup(page.content, "html.parser")

# # results = soup.find(id="ResultsContainer")
# target_results = soup.find(id="product-details")

# print(target_results.prettify())

from requests_html import AsyncHTMLSession
asession = AsyncHTMLSession()
async def get_pythonorg():
    r = await asession.get('https://python.org/')
    return r

async def get_reddit():
    r = await asession.get('https://reddit.com/')
    return r

async def get_google():
    r = await asession.get('https://google.com/')
    return r

async def get_target():
    r = await asession.get('https://www.target.com/s?searchTerm=hair')
    # print(r.html.links)
    name = r.html.find('#h-display-flex')
    print(len(name))
    print(name[11].text)
    return r

results = asession.run(get_pythonorg, get_reddit, get_google, get_target)
print(results) # check the requests all returned a 200 (success) code

# Each item in the results list is a response object and can be interacted with as such
for result in results:
    print(result.html.url)
