import os,sys,random,math,time


import MSD_util


def fl():

    sys.stdout.flush()



###
### PREDICTORS

###


class Pred:

    ''' implement generic predictor'''

    def __init__(self):
        pass

    def Score(self,user_songs,all_songs):
        return {}


class PredSI(Pred):

    ''' implemtn song-similarity based predicor '''


    def __init__(self,_s2u_tr,_A=0,_Q = 1):

        Pred.__init__(self)

        self.s2u_tr=_s2u_tr
        self.Q=_Q
        self.A=_A


    def printati(self):

        print "PredSI(A=%f,Q=%f) " % (self.A,self.Q)


    def Match(self,s,u_song):

        l1 = len(self.s2u_tr[s])
        l2 = len(self.s2u_tr[u_song])

        up = float(len(self.s2u_tr[s]&self.s2u_tr[u_song]))

        if up > 0:
            dn = math.pow(l1,self.A)*math.pow(l2,(1.0-self.A))

            return up/dn

        return 0.0


    def Score( self, user_songs,all_songs):

        s_scores={}


        for s in all_songs:

            s_scores[s]=0.0

            if not (s in self.s2u_tr):

                continue

            for u_song in user_songs:

                if not (u_song in self.s2u_tr):
                    continue

                s_match=self.Match(s,u_song)

                s_scores[s]+=math.pow(s_match,self.Q)

        return s_scores





class PredSU(Pred):

    ''' implement user-similarity based predictor'''

    def __init__(self, _u2s_tr,_A=0,_Q=1):

        Pred.__init__(self)

        self.u2s_tr = _u2s_tr
        self.Q = _Q
        self.A = _A

    def printati(self):

        print "PredSu(A = %f , Q = %f ) " % (self.A, self.Q)


    def Score(self, user_songs, all_songs):

        s_scores = {}

        for u_tr in self.u2s_tr:

            if not u_tr in self.u2s_tr:
                continue

            w = float(len(self.u2s_tr[u_tr]&user_songs))

            if w > 0:
                l1 = len(user_songs)
                l2 = len(self.u2s_tr[u_tr])

                w/= (math.pow(l1,self.A)*(math.pow(l2,(1.0-self.A))))

                w = math.pow(w,self.Q)

            for s in self.u2s_tr[u_tr]:

                if s in s_scores:

                    s_scores[s]+=w

                else:

                    s_scores[s]=w

        return s_scores




###
### recommenders
###


class Reco:

    ''' implements recommender'''

    def __init__(self,_all_songs):

        self.predictors =[]

        self.all_songs = _all_songs

        self.tau = 500


    def Add(self,p):

        self.predictors.append(p)


class SReco(Reco):



    def __init__(self,_all_songs):

        Reco.__init__(self,_all_songs)

        self.Gamma = []

    def RecommendToUser(self,user,u2s_v):

        songs_sorted=[]
        for p in self.predictors:
            ssongs=[]
            if user in u2s_v:
                ssongs = MSD_util.sort_dict_dec(p.Score(u2s_v[user],self.all_songs))
            else:
                ssongs = list(self.all_songs)


            cleaned_songs=[]
            for x in ssongs:
                if len(cleaned_songs) >= self.tau:
                    break
                if x not in u2s_v[user]:
                    cleaned_songs.append(x)

            songs_sorted+= cleaned_songs

        return songs_sorted;


    def RecommendToUsers(self,l_users,u2s_v):

        sti = time.clock()
        rec4users = []

        for i,u in enumerate(l_users):
            if not (i+1)%10:
                if u in u2s_v:
                    print " %d] %s w/ %d songs " % (i+1,l_users[i],len(u2s_v[u]))
                else:
                    print " %d] %ssss w/ 0 songs " % (i+1,l_users[i])

                fl()

            rec4users.append(self.RecommendToUser(u,u2s_v))
            cti= time.clock()-sti

            if not (i+1)%10:

                print " tot secs : %f (%f) " % (cti,cti/(i+1))

                fl()

        return rec4users
            
                    
    
        

    
        

                

                


                
        
            




























    
            

    
        


        
        
    
    


    
