from django.shortcuts import render,HttpResponse
import numpy as np
import pickle
import pandas as pd
import pymongo
from scipy.sparse import csr_matrix
from pymongo import MongoClient
from bson import ObjectId
from sklearn.neighbors import NearestNeighbors
from urllib.parse import urlencode





movies_dict = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_dict)

client = MongoClient('localhost',27017)
db = client.uimatic
col=db.Rating
col1=db.UserName
col2=db.UserData
col3=db.MovieName

pymongo_cursor1 = col1.find()
UserName = list(pymongo_cursor1)
pymongo_cursor3 = col3.find()
MovieName = list(pymongo_cursor3)


movie_rating = col2.find()
ratings = pd.DataFrame(movie_rating)

movie_name = col3.find()
movie = pd.DataFrame(movie_name)

# data=col2.find({'User_id':3})
# userdata= pd.DataFrame(data)
# m_id = userdata['Movie_id'].unique()



def userid_to_username():
    user= col2.find()
    user1=col1.find()
    userData1= pd.DataFrame(user1)
    UserData = pd.DataFrame(user)
    userid = UserData['User_id'].unique()
    userid.sort()
    user_id = list(userid)
   
    username = userData1['user_name']
    user_name = list(username)
    data1 = []
    for i in user_id :
        data1.append({'uname':user_name[i-1]})    
    return data1
    

def FetchMovie():
    movie_rating = col2.find()
    ratings = pd.DataFrame(movie_rating)

    movie_name = col3.find()
    movie = pd.DataFrame(movie_name)
    movies = movie['movie_name']
    id = ratings['Movie_id']
    movie_list=[]
    for i in id:
        movie_list.append(movies[i-1])
    return movie_list
    

# fetching the User Name on the basis of the User_id

def FetchUser():
    pymongo_cursor1 = col1.find()
    UserName = list(pymongo_cursor1)
    usern =pd.DataFrame(UserName)
    user = usern['user_name']
    movie_rating = col2.find()
    ratings = pd.DataFrame(movie_rating)
    uid = ratings['User_id']
    user_list=[]
    for i in uid:
        user_list.append(user[i-1])
    return user_list

    




def create_matrix(rating): 
    N = len(rating['User_id'].unique())
    M = len(rating['Movie_id'].unique())
  
    user_mapper = dict(zip(np.unique(rating["User_id"]), list(range(N))))
    
    movie_mapper = dict(zip(np.unique(rating["Movie_id"]), list(range(M))))
    
    user_inv_mapper = dict(zip(list(range(N)), np.unique(rating["User_id"])))
    
    movie_inv_mapper = dict(zip(list(range(M)), np.unique(rating["Movie_id"])))

    user_index = [user_mapper[i] for i in rating['User_id']]
    movie_index = [movie_mapper[i] for i in rating['Movie_id']]

    X = csr_matrix((rating["Rating"], (movie_index, user_index)), shape=(M, N))

    
    return X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper
    



#instead of writing this code on every function we simply create a data function which fetch all the needed data from database
#and whenever we need this function we can simply call it.


def data():
    # user = col2.find()
    # UserData = pd.DataFrame(user)
    # userid = UserData['User_id'].unique()
    # userid.sort()
    # movieid = UserData['Movie_id'].unique()
    # movieid.sort()
    # user_id = list(userid)
    # movie_id = list(movieid)
    pymongo_cursor2 = col3.find()
    MovieName = list(pymongo_cursor2)
    
    options = movies['title']
    pymongo_cursor2 = col1.find()
    UserName = list(pymongo_cursor2)
    pymongo_cursor = col2.find()
    all_data = list(pymongo_cursor)
    
  
    
   
    

    
    aryan={
    
        'title':options,
        'UserName':UserName,
        'MovieName':MovieName,
        'all_data':all_data
    }
    return aryan
    

def find_similar_movies(id,X,k,movie_mapper,movie_inv_mapper, metric='cosine', show_distance=False):
    neighbour_ids = []
      
    movie_ind = movie_mapper[id]
    movie_vec = X[movie_ind]
    k+=1
    kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
    kNN.fit(X)
    movie_vec = movie_vec.reshape(1,-1)
    neighbour = kNN.kneighbors(movie_vec, return_distance=show_distance)
    for i in range(0,k):
        n = neighbour.item(i)
        neighbour_ids.append(movie_inv_mapper[n])
    neighbour_ids.pop(0)
    return neighbour_ids

def index(request):
    aryan = data()
    return render(request , 'Rating_front.html',aryan)


def submitData(request):
    pymongo_cursor2 = col3.find()
    MovieName = list(pymongo_cursor2)
    
    options = movies['title']
    if request.method=='POST':
        name = request.POST.get('user_name')
        Movie_name = request.POST.get('movie_name')
        rating = int(request.POST.get('Rating'))
        
        
        doc  = col1.find_one({'user_name':name})
        id=doc['_id']
        doc2 = col3.find_one({'movie_name':Movie_name})
        id1=doc2['_id']

        last_doc= col2.find_one(sort=[('_id',-1)])
        if last_doc is None:
            new_id=1
        else:
            new_id = last_doc['_id']+1
        new_doc={'_id':new_id,
                 'id':new_id,
                 "User_id":id,
                 "Movie_id":id1,
                 "Rating":rating   
                 }
        
        col2.insert_one(new_doc)  
        movie = FetchMovie()
        user = FetchUser()
        movie_rating = col2.find()
        ratings = pd.DataFrame(movie_rating)
        
        id=ratings['id']
        rating = ratings['Rating']
        
        data = []
        for i in range(len(movie)):
            data.append({'id':id[i],'uname':user[i],'mname':movie[i],'rating':rating[i]})   
        
        aryan={
            'data':data,
            'UserName':UserName,
            'MovieName':MovieName
            
        }
        return render(request,'Rating_front.html',aryan)
    
def add_movie(request):
    return render(request,'add_movie.html')


def add_user(request):
    return render(request,'add_user.html')


def AddUserName(request):
    if request.method=='POST':
        
        
    
        name = request.POST.get('user_name')
        options = movies['title']
        # doc  = col1.find_one({'user_name':name})
        # id=doc['_id']
        # doc2 = col3.find_one({'movie_name':Movie_name})
        # id1=doc2['_id']
        last_doc= col1.find_one(sort=[('_id',-1)])
        if last_doc is None:
            new_id=1
        else:
            new_id = last_doc['_id']+1
        
        add_User={
            '_id':new_id,
            'user_name':name
        }
        col1.insert_one(add_User)
        aryan=data()
        
        return render(request,'Rating_front.html',aryan)

def AddMovieName(request):
    if request.method=='POST':
        
        
    
        name = request.POST.get('movie_name')
        options = movies['title']
        # doc  = col1.find_one({'user_name':name})
        # id=doc['_id']
        # doc2 = col3.find_one({'movie_name':Movie_name})
        # id1=doc2['_id']
        last_doc= col3.find_one(sort=[('_id',-1)])
        if last_doc is None:
            new_id=1
        else:
            new_id = last_doc['_id']+1
        
        add_movie={
            '_id':new_id,
            'movie_name':name
        }
        col3.insert_one(add_movie)
        aryan=data()
        
        return render(request,'Rating_front.html',aryan)
    
    


#recommend-------------------------------------------------------
#-----------------------------------------------------------------


def recommend_movie(request):
    data = userid_to_username()
    user_data ={
        'data':data
    }
                
    
    
    return render(request,'recommend_movie.html',user_data)


def recommend_movie_display(request):
    
    data = userid_to_username()
        
    
    name = request.POST.get('movie_name')
    movie_table = col3.find({'movie_name':name})
    movie_id = pd.DataFrame(movie_table)
    movie_id = movie_id['_id']    
    movie_id=list(movie_id)
    id=0
    for i in movie_id:
        id=i
    
    
    movie_rating = col2.find()
    rating = pd.DataFrame(movie_rating)
    
    
    
    
    
    
    X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper = create_matrix(rating)
    
    k=5
    similar_ids = find_similar_movies(id,X,k,movie_mapper,movie_inv_mapper)
    movie_name = col3.find()
    movies = pd.DataFrame(movie_name)
    movie_titles = dict(zip(movies['_id'], movies['movie_name']))
    movie_title =[]
    for i in similar_ids:
        movie_title.append(movie_titles[i])
    
    name ={
        "name":movie_title,
        'data':data
        
    }
    return render(request,'recommend_movie.html',name)
    
    
def redirect_to_rate(request):
    aryan = data()
    return render(request,'Rating_front.html',aryan)
    

        

def find_movie(request):
    
    data1 = userid_to_username()
        
    
    name = request.POST.get("user_name")
    user = col1.find({'user_name':name})
    userid = pd.DataFrame(user)
    userid = userid['_id']
    userid = list(userid)
    id = 0
    for i in userid:
        id=i
    
    
    movie_name = col3.find()
    movie = pd.DataFrame(movie_name)
    

    data=col2.find({'User_id':id})
    userdata= pd.DataFrame(data)
    m_id = userdata['Movie_id'].unique()

    mname = movie['movie_name']
    m_name = list(mname)
    data=[]
    m=list(m_id)
    for i in m:
        data.append({'name':m_name[i-1]})
    
    
   
    
    aryan ={
        'data':data,
        'name':name,
        'data1':data1
        
    }
    
    return render(request,'check.html',aryan)
    
    
    








