from django.shortcuts import redirect, render
from . models import Stock
from . forms import StockForm
from django.contrib import messages


# Create your views here.
YOUR_TOKEN ="pk_ea84e96e193148a1b17cc2a5dfdcabea"

def index(request):
    from pip._vendor import requests
    import json
    
    
   
    if request.method == 'POST':
        ticker = request.POST['ticker']
         
        api_request = requests.get("https://api.iex.cloud/v1/data/core/quote/"+ticker+"?token=" +YOUR_TOKEN)
        try:
            api =json.loads(api_request.content)

        except Exception as e:
            api ="Error ...." 
        return render(request,'index.html', {'api':api})     
    else:
         return render(request,'index.html', {'ticker':"enter a ticker symbol"})
        


    
   

def about(request):
    return render(request, 'about.html',{})


def add_stock(request):
    from pip._vendor import requests
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request,("stock has been add successfly"))
            return redirect('add_stock')            
                
    else:   

        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://api.iex.cloud/v1/data/core/quote/"+ str(ticker_item) +"?token=" +YOUR_TOKEN)
            try:
                api =json.loads(api_request.content)
                output.append(api)

            except Exception as e:
                api ="Error ...." 
        return render(request,'add_stock.html',{'ticker':ticker, 'output': output})


def delete(request,stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request,("Stock deleted successfly"))
    return redirect(add_stock)