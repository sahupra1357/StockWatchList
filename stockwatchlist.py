from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
from datetime import datetime
import urllib

stockwatchlist = Flask(__name__)
stockwatchlist.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mystock.db'
stockwatchlist.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(stockwatchlist)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stockCode = db.Column(db.String(10), nullable=False)
    stockName = db.Column(db.String(200), nullable=False)
    currentPrice = db.Column(db.Float)
    high52week = db.Column(db.Integer)
    low52week = db.Column(db.Integer)
    profitloss = db.Column(db.Integer)
    buyingprice = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,stockCode,stockName,buyingprice,currentPrice,high52week,low52week,profitloss):
        self.stockCode = stockCode
        self.stockName = stockName
        self.buyingprice = buyingprice
        self.currentPrice = currentPrice
        self.high52week = high52week
        self.low52week = low52week
        self.profitloss = profitloss

    def __repr__(self):
        return '<Stock %r>' % self.id


@stockwatchlist.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        profit_loss = 0
        stock_Code = request.form['stock']
        buying_price = request.form['buyingprice']

        scrap_stock(stock_Code)
        if current_Price == "" or current_Price == 0: 
            stocks = Stock.query.order_by(Stock.date_created).all()
            return render_template('index.html', stocks=stocks)
        else:
            if buying_price == "" or buying_price == 0 :
                buying_price = 0 
            else:
                profit_loss = float(current_Price) - float(buying_price)
            
            new_stock = Stock(stockCode=stock_Code,stockName=stock_name,buyingprice=buying_price,currentPrice=current_Price,high52week=high_52Week,low52week=low_52Week,profitloss=profit_loss)

            try: 
                db.session.add(new_stock)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your stock'
    else:
        stocks = Stock.query.order_by(Stock.date_created).all()
        return render_template('index.html', stocks=stocks)

@stockwatchlist.route('/delete/<int:id>')
def delete(id):
    stock_to_delete = Stock.query.get_or_404(id)

    try:
        db.session.delete(stock_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was problem deleting that stock'        


@stockwatchlist.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    stock = Stock.query.get_or_404(id)
    if request.method == 'GET':
        scrap_stock(stock.stockCode)

        if float(stock.currentPrice) != float(current_Price):
            stock.currentPrice = current_Price
        else:
            print "There is no change in Current price"

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating that stock'        
    else:
        stocks = Stock.query.order_by(Stock.date_created).all()
        return render_template('index.html', stocks=stocks)

def scrap_stock(stockCode):
    url = 'https://finance.yahoo.com/quote/'+stockCode
    try:
        page = urllib.urlopen(url)
    except:
        print "Error opening URL"
    
    global current_Price,high_52Week, low_52Week,stock_name
    soup = BeautifulSoup(page, "html.parser")
    try:
        if soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}):
            current_Price = soup.find_all('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
        else:
            current_Price = 0

        if soup.find('td',{'data-test':'FIFTY_TWO_WK_RANGE-value'}):
            week52_td = soup.find_all('td',{'data-test':'FIFTY_TWO_WK_RANGE-value'})[0].text
            week52_range_list = week52_td.split("-",2)
            high_52Week = week52_range_list[0]
            low_52Week = week52_range_list[1]
        else:
            high_52Week, low_52Week =0

        if soup.find('div',{'class':''}):
            stock_name = soup.find_all('div',{'class':''})[0].find('h1').text
    except:
        "Not a Valid stock!"

if __name__=="__main__":
    stockwatchlist.run(debug=True)
