from googlesearch import search
for url in search('"Breaking Code" WordPress blog', stop=1, pause=.1):
    print(url)