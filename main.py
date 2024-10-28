import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient import discovery
from bs4 import BeautifulSoup


# Start the OAuth flow to retrieve credentials
def authorize_credentials():
    CLIENT_SECRET = 'client_secret.json'
    SCOPE = 'https://www.googleapis.com/auth/blogger'
    STORAGE = Storage('credentials.storage')
    # Fetch credentials from storage
    credentials = STORAGE.get()
    # If the credentials doesn't exist in the storage location then run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials

# print(credentials)
def getBloggerService():
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://blogger.googleapis.com/$discovery/rest?version=v3')
    service = discovery.build('blogger', 'v3', http=http, discoveryServiceUrl=discoveryUrl)
    return service

def postToBlogger(payload):
    service = getBloggerService()
    post=service.posts()
    insert=post.insert(blogId='1932796379899459077',body=payload).execute()
    print("Post Published!")
    return insert

def build_html():
    # reading the lyrics from the lyrics.txt
    with open("lyrics.txt", 'r', encoding="utf-8") as file:
        lyrics_content = file.read()

    lyrics_soup = BeautifulSoup(lyrics_content, 'html.parser')
    first_div = lyrics_soup.find('div')

    # reading other song crew details form the details.txt
    with open("details.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

        singer = lines[0].strip()
        musician = lines[1].strip()
        lyricist = lines[2].strip()

    # Reading the target HTML
    with open("blogger_post.html", 'r', encoding="utf-8") as file:
        target_soup = BeautifulSoup(file, 'html.parser')  

    # inserting the lyrics to the template
    target_div = target_soup.find('div', id="div1")
    target_div.clear()  
    target_div.append(first_div)

    # inserting other song crew details to the template
    singer_place = target_soup.find('td', id="singer_name")
    lyricist_place = target_soup.find('td', id="lyricist_name")
    musician_place = target_soup.find('td', id="musician_name")
    singer_place.clear()  
    lyricist_place.clear()  
    musician_place.clear()  
    singer_place.append(singer)
    lyricist_place.append(lyricist)
    musician_place.append(musician)


    # removing the pulled lyrics from source file    
    with open("lyrics.txt", 'w', encoding="utf-8") as file:
        file.write(str(lyrics_soup))

    # returning the modified post template
    return str(target_soup)



def get_title():
    # reading song title details from the details.txt
    with open("details.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

        title_english = lines[3].strip()
        title_malayalam = lines[4].strip()
        movie = lines[5].strip()

    return f"{title_english} ({title_malayalam}) | {movie}"


def get_labels():
    # reading song details from the details.txt
    with open("details.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

        singer = lines[0].strip().replace(" ", "_")
        musician = lines[1].strip().replace(" ", "_")
        lyricist = lines[2].strip().replace(" ", "_")
        movie = lines[5].strip().replace(" ", "_")

    with open("details.txt", "w", encoding="utf-8") as file:
        file.writelines(lines[6:])

    return ["Movie_Song", "Malayalam", movie, singer, musician, lyricist,]

# publishing the post
customMetaData = "This is meta data"
payload={
        "content": build_html(),
        "title": get_title(),
        'labels': get_labels(),
        'customMetaData': customMetaData
    }
postToBlogger(payload)