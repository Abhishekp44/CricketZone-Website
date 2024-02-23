from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from cricketapp.models import Matches,Matches2,BookTickets,CricketNews,Teams,Players
import razorpay
from django.core.mail import send_mail
from cricketapp.forms import ContactForm

# Create your views here.
def home(request):

    p=Matches.objects.filter(is_active=True)
    t=Matches2.objects.filter(mid__in=p)
    n=CricketNews.objects.all()
    context={}
    context['data']=t
    context['news']=n
    return render(request,'index.html',context)

def register(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        context={}

        n=request.POST['uname']
        f=request.POST['fname']
        l=request.POST['lname']
        em=request.POST['email']
        p=request.POST['upass']
        cp=request.POST['ucpass']

        if n=='' or f=='' or l=='' or em=='' or p=='' or cp=='':
            context['errmsg']='Field can not be blank'
            return render(request,'register.html',context)
        elif len(p)<=8:
            context['errmsg']='password must be atleast 8 character'
            return render(request,'register.html',context)
        elif p!=cp:
            context['errmsg']='password and confirm password must be same'
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(username=n,email=em,first_name=f,last_name=l)
                u.set_password(p )
                u.save()
                context['success']='User Created Successfully'
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="User already Exist, Please Login!"
                return render(request,'register.html',context)
            
def user_login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        n=request.POST['uname']
        p=request.POST['upass']
        
        u=authenticate(username=n,password=p)
        if u is not None:
            login(request,u)
            return redirect('/home')
        else:
            context={}
            context['errmsg']='Invalid Username and Password'
            return render(request,'login.html',context)
        
def dashboard(request):
    u=User.objects.filter(id=request.user.id)
    b=BookTickets.objects.filter(uid__in=u)
    context={}
    context['data']=b
    context['data1']=u
    return render(request,'dashboard.html',context)
        
def search(request):
    query=request.GET['query']
    
    mname=Matches.objects.filter(name__icontains=query,is_active=True)
    mcat=Matches.objects.filter(cat__icontains=query,is_active=True)
    t1name=Matches.objects.filter(team1_name__icontains=query,is_active=True)
    t2name=Matches.objects.filter(team2_name__icontains=query,is_active=True)

    allmatches=mname.union(mcat,t1name,t2name)
    context={}
    if allmatches.count()==0:
        context['errmsg']='No Results'
    context['data']=allmatches
    return render(request,'matches.html',context)
        
def user_logout(request):
    logout(request)
    return redirect('/home')

def teams(request):
    t=Teams.objects.filter(cat=1)
    context={}
    context['data']=t
    return render(request,'teams.html',context)

def league(request):
    t=Teams.objects.filter(cat=2)
    context={}
    context['data']=t
    return render(request,'leagues.html',context)

def players(request,tid):
    t=Teams.objects.filter(id=tid)
    p=Players.objects.filter(tid=tid)
    context={}
    context['data']=t
    context['data1']=p
    return render(request,'players.html',context)

def matches(request):
    p=Matches.objects.filter(is_active=True)
    context={}
    context['data']=p
    m=Matches.objects.filter(is_active=False)
    context['data1']=m
    return render(request,'matches.html',context)

def rank_m(request):
    return render(request,'ranking_m.html')

def rank_w(request):
    return render(request,'ranking_w.html')

def scorecard(request,sid):
    p=Matches.objects.filter(id=sid)
    t=Matches2.objects.filter(mid=sid)
    context={}
    context['data1']=p
    context['data2']=t
    return render(request,'scorecard.html',context)

def tickets(request):
    p=Matches.objects.filter(is_active=False)
    t=Matches2.objects.filter(mid__in=p)
    context={}
    context['data1']=t
    
    return render(request,'tickets.html',context)

def contact_us(request):
    context={}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Thank you for reaching out! We will get back to you soon."
            context['msg']=message
    else:
        form = ContactForm()
    
    context['form']=form
    

    return render(request, 'contact.html',context)

def thankyou(request):
    render(request,'thankyou.html')

def add(request,pid):
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        p=Matches.objects.filter(id=pid)
        m=Matches2.objects.filter(mid=pid)
        c=BookTickets.objects.create(uid = u[0],mid = p[0],mid1 = m[0])
        c.save()
        return redirect('/viewcart')
    else:
        return redirect('/login')
    
def view(request):
    c=BookTickets.objects.filter(uid=request.user.id)
    context={}
    sum=0
    for x in c:
        sum=sum+x.mid1.m_price*x.qty
    c.update(amount=sum)
    if request.method == 'POST':  
        radio_value = request.POST.get('seats')
        c.update(seats=radio_value)
    context['data']=c 
    return render(request,'details.html',context)


def updateqty(request,x,cid):
    c=BookTickets.objects.filter(id=cid)
    q=c[0].qty

    if x == '1':
        q=q+1
    elif q>1:
        q=q-1
    c.update(qty=q)
    return redirect('/viewcart')

def updateseats(request):
    if request.method == 'POST':
        radio_value = request.POST.get('seats')
        BookTickets.objects.create(seats=radio_value)

    return redirect('/viewcart') 

def pay(request):
    return render(request,'pay.html')

def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_QjBnpIzB3Rfjt0", "3jO0jEdn0QAKqQETF0CuGQzG"))
    o=BookTickets.objects.filter(uid=request.user.id)
    amt=o[0].amount
    id=o[0].uid
    DATA = { "amount": amt*100, "currency": "INR", "receipt": id }
    payment = client.order.create(data=DATA)
    context={}
    context['payment']=payment
    return render(request,'pay.html')

def paymentsuccess(request):
    u=User.objects.filter(id=request.user.id)
    b=BookTickets.objects.filter(uid__in=u).first()
    sub='You successfully book tickets'
    msg=f'Enjoy the match!\n\n'\
        f'Match Details:\n'\
        f'Match Name:{b.mid.name}\n'\
        f'Match Date:{b.mid1.m_date}\t{b.mid.status}\n'\
        f'Stadium:{b.mid1.stadium}\n'\
        f'Booked Tickets:{b.qty}\n'\
        f'Seats:{b.seats}\n\n'\
        f'Payment Details:\n'\
        f'Match Price/Ticket:{b.mid1.m_price}\n'\
        f'QTY:{b.qty}\n'\
        f'Total Price:{b.amount}\n'\
        f'Payment Status:PAID'
    frm='abhiphapale101@gmail.com'
    u=User.objects.filter(id=request.user.id)
    to=u[0].email
    send_mail(
        sub,
        msg,
        frm,
        [to],
        fail_silently=False
    )
    return render(request,'paymentsuccess.html') 

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')