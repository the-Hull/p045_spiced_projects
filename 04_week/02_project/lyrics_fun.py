import requests
import urllib.parse as upa
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np




def refine_artist_link(artist_req: requests.models.Response, artist_url: str, base_url: str, verbose: bool) -> str:

    # artist does not exist
    str_no_match = "We couldn't find any artists matching your query."
    if re.search(str_no_match, artist_req.text):
        if verbose:
            print(f'    No unique artist found')
        artist_url_clean = None
        return artist_url_clean
    
    # arist has multiple matches; return first artist
    str_multi_match = "Yee yee!"
    if re.search(str_multi_match, artist_req.text):
        if verbose:
            print(f'    Several options for artist; picking first')
        artist_url_clean = base_url + "/" + BeautifulSoup(artist_req.text, features = 'html.parser').find(class_= "tal fx").a['href']
        return artist_url_clean


    # artist has single option
    str_single_match = "Famous lyrics"
    if re.search(str_single_match, artist_req.text):
        if verbose:
            print(f'    Found unique artist')
        artist_url_clean = artist_url
        return artist_url_clean




def get_artist(artist: str, verbose: bool) -> dict:
    """Posts a request to lyrics.com with an URL encoded _artist_ name.\n 
    Returns a _dict_ with the artist, the encoded URL, the response, and 
    status code, for further processing 
    """

    
    if not isinstance(artist, str):
        raise ValueError("Artist name not a string")


    # encode artist and 
    # post request to lyrics.com

    base_url = 'https://www.lyrics.com'
    artist_url = base_url + '/artist/' + upa.quote(str.strip(artist)) + '/' 

    artist_req = requests.get(artist_url)

    if (artist_req.status_code != 200):
        raise Exception("Request unsuccessful")

    if verbose:
        print(f'Artist: {artist} ----- Status: {artist_req.status_code}')



    artist_url_refined = refine_artist_link(
        artist_req=artist_req,
        artist_url=artist_url,
        base_url=base_url,
        verbose = verbose
    )


    artist_exists = artist_url_refined is not None

    res = {
        'base_url' : base_url,
        'artist' : artist, 
        'url' : artist_url,
        'url_refined' : artist_url_refined,
        'response' : artist_req,
        'status_code' : artist_req.status_code,
        'exists_on_site' : artist_exists
    }

    return res



def extract_lyric_links(artist, drop_duplicates = False, drop_instrumentals = False, drop_similar = False, verbose = False) -> dict:

    if not artist['exists_on_site']:
        print("    Can only proceed with an artist listed at lyrics.com, ensure exists_on_site is True. Returning None")
        return None

    response = requests.get(artist['url_refined'])

    html = BeautifulSoup(markup = response.text, features = 'html.parser')
    links = [h.a['href'] for h in html.find_all('td', class_ = 'tal qx')]
    links = [artist['base_url'] + l for l in links]

    if drop_duplicates:
        dup = pd.Series([re.search("[^\/]+$", al).group(0) for al in links])
        dup_idx = dup[dup.duplicated().values==False].index.values.astype(int)
        if verbose:
            print(f'    Dropped {len(links) - len(dup_idx)} duplicated lyric links')
        links = list(np.array(links)[dup_idx])
    else:
        if verbose:
            print(f'    No duplicate lyric links dropped')


    if drop_instrumentals:
        inst_idx = [el is None for el in [re.search('(?i)Instrumental', li ) for li in links]]
        
        if verbose:
            print(f'    Dropped {len(links) - sum(np.array(inst_idx))} instrumental lyric link(s)')
        links = list(np.array(links)[np.array(inst_idx)])
    else:
        if verbose:
            print(f'    No instrumental lyric link dropped')


    if drop_similar:
        sim_idx = [el is None for el in [re.search('(?i)(Remix|Acoustic)', li ) for li in links]]
    
        if verbose:
            print(f'    Dropped {len(links) - sum(np.array(sim_idx))} Remix/Acoustic lyric link(s)')
        links = list(np.array(links)[np.array(sim_idx)])
    else:
        if verbose:
            print(f'    No Remix/Acoustic lyric link dropped')


    res = {
    'base_url' : artist['base_url'],
    'artist' : artist['artist'], 
    'url' : artist['url'],
    'url_refined' : artist['url_refined'],
    'response' : response,
    'status_code' : response.status_code,
    'exists_on_site' : artist['exists_on_site'],
    'links' : links
    }


    return res


def extract_lyric(artist_links: dict, verbose: bool = False):

    if artist_links is None:
        print("    Can only proceed with an artist listed at lyrics.com, ensure lyric link extraction was successful. Returning None")
        return None

    lyric_list = []
    title_list = []
    response_list = []
    status_list = []

    for li in artist_links['links']:

        response = requests.get(li)

        response_list.append(response)
        status_list.append(response.status_code)

        if response.status_code == 200:
            html = BeautifulSoup(markup = response.text, features = 'html.parser')
            ly = str.join(" ", html.find(name = 'pre', id = 'lyric-body-text').text.split())
            lyric_list.append(ly)

            ti = html.find(name = 'h1', id = 'lyric-title-text').text
            title_list.append(ti)




        else:
            lyric_list.append(None)
            title_list.append(None)



    # return [title_list, lyric_list]


    res = {
    'base_url' : artist_links['base_url'],
    'artist' : artist_links['artist'], 
    'url' : artist_links['url'],
    'url_refined' : artist_links['url_refined'],
    'response' : response_list,
    'status_code' : status_list,
    'exists_on_site' : artist_links['exists_on_site'],
    'lyric_link' : artist_links['links'],
    'lyric_title' : title_list,
    'lyric_text' : lyric_list
    }


    return res



def process_artist(artist: str, drop_duplicates: bool = True, drop_instrumentals: bool = True, drop_similar:bool = True, verbose:bool = True):
    """
    Downloads all lyrics for an _artist_ from lyrics.com with safe handling of duplicate artists. 
    Allows dropping instrumentals, similar song versions in remixes and acoustic versions, and duplicate listings. 
    The verbose option gives some details on the processing.
    """

    res = None

    artist = get_artist(artist=artist, verbose=True)

    if artist['exists_on_site']:
        artist_links = extract_lyric_links(artist, drop_duplicates = True, drop_instrumentals = True, drop_similar=True, verbose=True)
    else:
        raise ValueError("Artist does not exist on site; artist['exists_on_site'] must be True")
    
    if artist_links:
        artist_extract = extract_lyric(artist_links=artist_links, verbose = False)
        res = artist_extract
    else:
        raise ValueError("artist_links cannot be None; indicates no links were found.")


    return res

    