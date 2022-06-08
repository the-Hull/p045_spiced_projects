import requests
import urllib.parse as upa
from bs4 import BeautifulSoup
import re




def refine_artist_link(artist_req: requests.models.Response, artist_url: str, base_url: str, verbose: bool) -> str:

    # artist does not exist
    str_no_match = "We couldn't find any artists matching your query."
    if re.search(str_no_match, artist_req.text):
        if verbose:
            print(f'No unique artist found')
        artist_url_clean = None
        return artist_url_clean
    
    # arist has multiple matches; return first artist
    str_multi_match = "Yee yee!"
    if re.search(str_multi_match, artist_req.text):
        if verbose:
            print(f'Several options for artist; picking first')
        artist_url_clean = base_url + BeautifulSoup(artist_req.text).find(class_= "tal fx").a['href']
        return artist_url_clean


    # artist has single option
    str_single_match = "Famous lyrics"
    if re.search(str_single_match, artist_req.text):
        if verbose:
            print(f'Found unique artist')
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

    base_url = 'https://www.lyrics.com/'
    artist_url = base_url + 'artist/' + upa.quote(str.strip(artist)) + '/' 

    artist_req = requests.get(artist_url)

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
        'artist' : artist, 
        'url' : artist_url,
        'url_refined' : artist_url_refined,
        'response' : artist_req,
        'status_code' : artist_req.status_code,
        'exists_on_site' : artist_exists
    }



    return res



