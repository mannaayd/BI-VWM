import pandas as pd
import numpy as np
import os.path
import os
import time



def creat_user(user_id = None):
    f = open('movies.txt','r')
    text = []
    movie_all = []
    for line in f:
        text.append(line)

    df_r = pd.read_csv("storage/ratings.csv")
    df_m = pd.read_csv('storage/movies.csv')
    user_id = df_r['userId'].max()+1
    #print(user_id)
    for i in text:
        a, b = i.split()[-1], i[:-3]
        #print(a,'++',b, '++')
        movieId = df_m[df_m['title']==b]['movieId'].values[0]
        movie_all.append(movieId)
        print(user_id, "  ", movieId, " ", b)
        df1 = pd.DataFrame({"userId":[user_id],
                            "movieId":[movieId],
                            "rating":[float(a)],
                            "timestamp":[964982703]})
        df_r = df_r.append(df1,ignore_index = True)
    #print(df_r)
    create_corr(user_id,df_r,movie_all)




def create_corr(user_id:int,df,movie_all):
    print(df)
    #df = pd.read_csv("ratings.csv",)
    df = df[['movieId','rating','userId']]
    dff = pd.pivot_table(df,index=['userId'],columns=['movieId'],values='rating',aggfunc=np.sum)
    
    #ddf = dff.fillna(0)
    #dff = pd.get_dummies(df['user_Id'])
    f = open('method.txt','r')
    method = f.read()
    a = dff.T.corr(method=method)

    #a.fillna(0)
    #print(a.sort_values(ascending=False).head(20))
    dff = dff.fillna(0)
    a = a.fillna(0)
    #print(a[user_id].sum())
    ind = dff.index
    col = dff.columns
    #print(dff.loc[1,1],a.loc[1,1])
    #print(dff.loc[2,1],a.loc[1,2])
    #print(dff.loc[3,1],a.loc[1,3])
    #for i in ind:
    #    for j in col:
    #        dff.loc[i,j] = dff.loc[i,j]*a.loc[1,i]
    #    print(i)
    
    #print(dff.values)
    #print(a[1].values)
    
    dff = dff.mul(a[user_id].values,axis=0)
    dff = dff.drop(columns=movie_all)
    #print(movie_all)
    #print(dff.sum().sort_values(ascending=False))
    df_new_res = dff.sum().sort_values(ascending=False)
    res = []
    arr_film_res = df_new_res.index[:5]
    df_m = pd.read_csv("storage/links.csv")
    for i in arr_film_res:
        res.append(df_m[df_m['movieId']==i]['tmdbId'].values[0])
    #print(res)
    f = open('res.txt','w')
    for i in res:
        f.write(""+str(int(i))+"\n")
    #print(dff.head(10))
    #print(a.head(10))
    #df_new_res = 
    print("result is complete.")



#create_corr(1)


def main():
    if os.path.exists('res.txt'):
        os.remove('res.txt')
    if os.path.exists('method.txt'):
        os.remove('method.txt')
    while True:
        time.sleep(3)
        check_file = os.path.exists('method.txt')
        if check_file:
            creat_user()
            if os.path.exists('method.txt'):
                os.remove('method.txt')
            


main()