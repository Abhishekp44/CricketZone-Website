from django.db import models

# Create your models here.
class Matches(models.Model):
    CAT=((1,'T20'),(2,'ODI'),(3,'Test'))
    name=models.CharField(max_length=100 ,verbose_name='Match name')
    cat=models.IntegerField(verbose_name='Category' ,choices=CAT)
    status=models.CharField(max_length=300, verbose_name='match status')
    team1_name=models.CharField(max_length=50 ,verbose_name='team1 name')
    team2_name=models.CharField(max_length=50 ,verbose_name='team2 name')
    team1_score=models.CharField(max_length=50 ,verbose_name='team1 score')
    team2_score=models.CharField(max_length=50 ,verbose_name='team2 score')
    is_active=models.BooleanField(default=True)
    team1_flag=models.ImageField(upload_to='image')
    team2_flag=models.ImageField(upload_to='image')


    
class Matches2(models.Model):
    mid=models.ForeignKey('Matches',on_delete=models.CASCADE, db_column='mid')
    stadium=models.CharField(max_length=300, verbose_name='match stadium')
    m_date= models.DateField()
    m_price=models.FloatField()

class BookTickets(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE, db_column='uid')
    mid=models.ForeignKey('Matches',on_delete=models.CASCADE, db_column='mid')
    mid1=models.ForeignKey('Matches2',on_delete=models.CASCADE, db_column='mid1')
    seats=models.CharField(max_length=50,default='Wing A')
    qty=models.IntegerField(default=1)
    amount=models.IntegerField(default=800)

class CricketNews(models.Model):
    title=models.CharField(max_length=100 ,verbose_name='News Title')
    ndetail=models.TextField(max_length=1000,verbose_name='News Detail')
    nimg=models.ImageField(upload_to='image')

class Teams(models.Model):
    CAT=((1,'International Teams'),(2,'League Teams'))
    tname=models.CharField(max_length=50 ,verbose_name='Team Name')
    cat=models.IntegerField(verbose_name='Category' ,choices=CAT)
    timage=models.ImageField(upload_to='image')


class Players(models.Model):
    CAT=((1,'India'),(2,'Australia'),(3,'Pakistan'),(4,'England'),(5,'Afghanistan'),(6,'Sri Lanka'),(7,'Bangladesh'),(8,'South Africa'),(9,'West Indies'),(10,'New Zealand'),(11,'Chennai Super Kings'),(12,'Mumbai Indians'),(13,'Gujrat Titans'),(14,'Lucknow Super Giants'),(15,'Royal Challenger Bangalore'),(16,'Sunrisers Hyderabad'),(17,'Kolkata Knight Riders'),(18,'Delhi Capitals'),(19,'Punjab Kings'),(20,'Rajasthan Royals'))
    pname=models.CharField(max_length=50 ,verbose_name='Player Name')
    jersey_no=models.IntegerField()
    cat=models.IntegerField(verbose_name='Category' ,choices=CAT)
    pimg=models.ImageField(upload_to='image')
    ptype=models.CharField(max_length=50)
    tid=models.ForeignKey('Teams',on_delete=models.CASCADE, db_column='tid')
 
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
    


    
