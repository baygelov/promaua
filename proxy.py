def get_free_proxies():
    list_proxies = []
    file = open("http.txt", "r", encoding="utf-8")
    while True:

        proxy = file.readline()
        if not proxy:
            break
        proxy = proxy.replace('\n', '')
        proxy = proxy.replace('\ufeff', '')
        list_proxies.append(proxy)
    file.close()
    return list_proxies
