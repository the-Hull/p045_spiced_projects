import requests
import urllib.parse as upa
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


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

    n_links = len(artist_links['links'])

    lyric_list = [None] * n_links
    title_list = [None] * n_links
    response_list = [None] * n_links
    status_list = [None] * n_links

    for id, li in enumerate(artist_links['links']):

        response = requests.get(li)

        response_list[id] = response
        status_list[id] = response.status_code

        if response.status_code == 200:
            html = BeautifulSoup(markup = response.text, features = 'html.parser')
            ly = str.join(" ", html.find(name = 'pre', id = 'lyric-body-text').text.split())
            lyric_list[id] = ly

            ti = html.find(name = 'h1', id = 'lyric-title-text').text
            title_list[id] = ti

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
        # check if 1 > not None links


    return res




def make_lyric_df(artist_lyrics: dict) -> pd.core.frame.DataFrame:
    
    lyric_df = pd.DataFrame({'artist' : artist_lyrics['artist'], 'text' : artist_lyrics['lyric_text']})

    return lyric_df



def make_model_df(artist_list: list):

    if len(artist_list) != 2:
        raise ValueError("Supply a list of two artist lyric dictionaries to proceed")

    dfs = []
    for ar in artist_list:
        dfs.append(make_lyric_df(ar))
    
    model_df = pd.concat(dfs, axis = 0)

    return model_df

def select_proba_idx(predicted_artist:str, artists: list):

    artists = sorted(artists)
    idx = [i for i, ar in enumerate(artists) if ar == predicted_artist][0]
    return idx



def run_logreg(moddf, new_lyric, c_strength = 1):

    new_lyric = pd.DataFrame({'text' : new_lyric}, index=[0])
   
    X = moddf['text']
    y = moddf['artist']

    log_reg = Pipeline(
        [('transformer', TfidfVectorizer(stop_words = 'english')),
        ('logreg', LogisticRegression(C=c_strength, class_weight='balanced'))
        ]
    )
    log_reg.fit(X, y)

    predicted_artist = log_reg.predict(X = new_lyric['text'])[0]
    predicted_proba = log_reg.predict_proba(X = new_lyric['text'])
    
    prob_idx = select_proba_idx(predicted_artist=predicted_artist, artists=moddf['artist'].unique())

    res = {
        'predicted_artist': predicted_artist,
        # 'predicted_proba' : predicted_proba[0][prob_idx]
        'predicted_proba' : max(predicted_proba[0])
    }

    return res
    

    

def predict_artist(first: str, second: str, new_lyric: str, drop_duplicates: bool = True, drop_instrumentals: bool = True, drop_similar:bool = True, verbose:bool = True):
    
    if not ((isinstance(first, str)) or (isinstance(second, str))):
        raise ValueError('Artists must be supplied as strings')
    
    if first == second:
        raise ValueError('Please supply two different artists')


    artist_list = [str(first), str(second)]

    artist_res = [None] * 2
    # loop over artists to get lyrics dic
    for i, ar in enumerate(artist_list):
        artist_res[i] = process_artist(
            artist = ar,
            drop_duplicates = True,
            drop_instrumentals = True,
            drop_similar = True,
            verbose = True
        )



    # make model df
    model_df = make_model_df(artist_res)

    # predict artist
    mod_res = run_logreg(moddf=model_df, new_lyric=new_lyric)

    print(pd.DataFrame(mod_res, index = [0]))

    return mod_res
  