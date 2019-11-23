import data_reader
import strategies

date, op, hi, lo, cl, adj, vo = data_reader.read_stock_data("AAPL")
signals = strategies.sma_crossover(date, adj) #this line dictates which strat to use
	
equity = 100000 #start with $100,000 cash
shares = 0
portfolio = [["Date", "Cash", "Shares of AAPL"]]

for i in range(len(signals)):
	price = signals[i][2] 
	if signals[i][1] == "Buy" and shares == 0:    #if there's a buy signal and we have no shares
		units = int(equity / price)               #buy as many shares as you can
		units = min(1000, units - (units % 100))  #afford, in increments of 100
		equity -= units * price                   #with a maximum order of 1000 shares
		shares = units
	elif signals[i][1] == "Sell" and shares != 0: #at sell signals, sell all remaining
		equity += shares * price                  #stock at the current day's price
		shares = 0
	#this investment strategy is long only--no short selling
	portfolio.append([signals[i][0], equity, shares]) 		

if shares > 0: #if there are any shares leftover on today's date, cash out
	equity += shares * adj[-1]
	shares = 0
	
portfolio.append([date[-1], equity, 0])

#portfolio array represents the cash/shares amount at the time of each signal
print(portfolio[-1])
