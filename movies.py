import imdb

ia = imdb.IMDb() #object for accessing imdb database

#search for a movie
def movie_desc(movie_name):
    s_result = ia.search_movie(movie_name)
    #Saving the list of search results
    for item in s_result:
        s_list = item['long imdb canonical title'], item.movieID
    m_name = s_result[0]
    #print m_name.summary()
    m_id = ia.get_imdbID(m_name)
    ia.update(m_name)
    desc = m_name.summary()
    return desc

def get_review(movie_name):
    s_result = ia.search_movie(movie_name)
    m_name = s_result[0]
    ia.update(m_name)
    result = m_name['rating']
    return result

test = 'The Avengers'
#movie_desc(test)
#get_review(test)
