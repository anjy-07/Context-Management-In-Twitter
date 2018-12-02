import csv
import os


#with open(os.path.join('Result_100.csv')  , 'w' , newline='' , errors="ignore") as f:
                                    #writer = csv.writer(f)
                                    #writer.writerow(["userId", "followeeId", "User_Affinity", "Content_Similarity"])
                                    #pow



                                    
with open(os.path.join('Users.csv' ) , 'r' , newline='' , errors="ignore" ) as csvf:
        reader = csv.DictReader(csvf)
        for row in reader:
                u = row["Users"]
            
                newpath1 =  '.\Data'+'_'+u
                with open(   os.path.join(newpath1 ,  'final_output.csv'  ) , 'r' , newline='' , errors="ignore" ) as csvf:
                    reader = csv.DictReader(csvf)
                    for row in reader:
                        foll = row["followeeName"]
                        ua = row["Final_User_Affinity"]
                        cs = row["Final_Content_Similarity"]
                        list1 = []
                        
                        
                        list1.append(u)
                        list1.append(foll)
                        list1.append(ua)
                        list1.append(cs)
                        
                        with open(os.path.join('Result_100.csv')  , 'a' , newline='' , errors="ignore") as f:
                                    writer = csv.writer(f)
                                    print(list1)
                                    writer.writerow(list1)
                                    
                                    
                                    pow
                       
                    
                       

                        
                        
