import streamlit as st
import pickle


mov= pickle.load(open("movies.pkl",'rb'))
movies=mov['title'].values

name= pickle.load(open("recommendation.pkl",'rb'))


st.header("Movie Recommendation System")
select_value= st.selectbox("Select the movies from dropdown",movies)


from fuzzywuzzy import fuzz

def fuzzy_movie_name_matching (input_str,mapper,print_matches):
    # match_movie is list of tuple of 3 values(movie_name,index,fuzz_ratio)
    match_movie = []
    for movie,ind in mapper.items():
        current_ratio = fuzz.ratio(movie.lower(),input_str.lower())
        if(current_ratio>=50):
            match_movie.append((movie,ind,current_ratio))
     
    # sort the match_movie with respect to ratio 

    match_movie = sorted(match_movie,key =lambda x:x[2])[::-1]
    
    if len(match_movie)==0:
        print("Oops..! no such movie is present here\n")
        return -1
    if print_matches == True:
        print("some matching of input_str are\n")
        for title,ind,ratio in match_movie:
            print(title,ind,'\n')
     
        
    return match_movie[0][1]  


def make_recommendation(input_str,data,model,mapper,n_recommendation):
    
    print("system is working....\n")
    model.fit(data)
    
    index = fuzzy_movie_name_matching (input_str,mapper,print_matches = False)
    
    if index==-1 :
        print("pls enter a valid movie name\n")
        return 
    
    name = model.kneighbors(data[index],n_neighbors=n_recommendation+1,return_distance=False)
    # now we ind of all recommendation
    # build mapper index->title
    index_to_movie={
        ind:movie for movie,ind in mapper.items()
    }
    print("Viewer who watches this movie ",input_str,"also watches following movies.")
    #print(index_list[0][2])
    for i in range(1,name.shape[1]):
        print(index_to_movie[name[0][i]])
    
    
    return 


if st.button("Show Recommendations"):
   movie_name=make_recommendation(select_value)
   col1,col2,col3,col4,col5= st.columns(5)
   with col1:
       st.text(movie_name[0])
   with col2:
       st.text(movie_name[1])
   with col3:
       st.text(movie_name[2])
   with col4:
       st.text(movie_name[3])
   with col5:
       st.text(movie_name[4])
