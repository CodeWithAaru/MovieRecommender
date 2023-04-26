# MovieRecommender

1.First Download The the Zip File and extract it.

2. open the extracted folder in your IDE(for me - Visual Studio Code).

3. Install the MongoDb Database  and create Three table.
      > MovieName
      > 
      > UserName
      > 
      > UserData
 
4. Change NAME to 'Your_Database_NAme' in Your Setting.py

  DATABASES = {
      'default': {
          'ENGINE': 'djongo',
          'NAME': 'Your Database Name',
        
      }
  }
  
  
  5. Now simply Click on Terminal >> New Terminal.
  
  6. Run Command python manage.py runserver    
      it gives you a link with your Localhost Adress simply click on that.
      
--------------------Congratulation----------------------------
-----You Succesfully Runned Your Movie Recommender System-----
