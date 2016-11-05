
class Config:
    couchUrl = 'http://localhost:5984/'
    couchDbUrl = couchUrl + 'social/'

    webPort = 8001
    webUrl = 'http://localhost:' + str(webPort) + '/cgi-bin/'
