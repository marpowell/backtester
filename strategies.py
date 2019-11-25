from data_reader import read_stock_data
import math

def stdev(sample): #standard deviation calculator
	ave = sum(sample)/len(sample)
	total = 0
	for each in sample:
		total += math.pow(each-ave,2)
	return math.sqrt(total/len(sample))
	
def bollinger_bands(data):
	date = data[0]
	adj = data[5]
	bbands = [["Index", "Date", "Upper Band", "Moving Average", "Lower Band", "Price"]]
	#initialize the array to heading
	for i in range(len(adj)):
		if i < 20:
			theta = stdev(adj[:i+1])
			mu = sum(adj[:i+1])/(i+1)
		else:
			theta = stdev(adj[i-19:i+1]) 
			mu = sum(adj[i-19:i+1])/20
		
		bbands.append([i, date[i], mu + 2*theta, mu, mu-2*theta, adj[i]])
	
	signals = [["Date", "Signal", "Price"]]
	
	for each in bbands: #Sell signal when the price is 2 std devs from the mean
		if each[5] > each[2] and signals[-1][1] != "Sell":
			signals.append([each[1], "Sell", each[5]])
		elif each[5] < each[4] and signals[-1][1] != "Buy": #Buy signal when price is 2 std devs above the mean
			signals.append([each[1], "Buy", each[5]])
			
	return signals

def sma_crossover(data):
	date = data[0]
	adj = data[5]
	sma9 = [] #SMA9 for Simple Moving Average with a window of 9 bars
	sma18 = []
	signals = [["Date", "Signal", "Price"]]
	for i in range(len(adj)):
	
		if i >= 8:
			sma9.append(sum(adj[i-8:i+1])/9.0)
		else: 
			sma9.append(sum(adj[:i+1])/float(i+1))
		if i >= 17:
			sma18.append(sum(adj[i-17:i+1])/18.0)
		else:
			sma18.append(sum(adj[:i+1])/float(i+1))
	
		if i < 1:
			sma9.append(adj[0])
			sma18.append(adj[0])
			continue
	
		if sma9[i-1] < sma18[i-1] and sma9[i] > sma18[i]:   #when the fast average moves above
			signals.append([date[i], "Buy", adj[i]])        #the slow average, generate buy signal
		elif sma9[i-1] > sma18[i-1] and sma9[i] < sma18[i]: #do the reverse for
			signals.append([date[i], "Sell", adj[i]])       #the sell signal
	
	return signals
	
def macd(data):
	date = data[0]
	adj = data[5]
	ema12 = []
	ema26 = []
	macd = [] #the difference ema12-ema26
	macd_signal_line = [] #a 9 period ema of the macd
	a9 = 2/10.0
	a12 = 2/13.0
	a26 = 2/27.0
	signals = []
	
	for i in range(len(adj)):
			
		if i <= 11:
			ema12.append(sum(adj[:i+1])/float(i+1))
		else:
			ema12.append(a12 * adj[i] + (1-a12) * ema12[i-1])
			
		if i <= 25:
			ema26.append(sum(adj[:i+1])/float(i+1))
		else:
			ema26.append(a26 * adj[i] + (1-a26) * ema26[i-1])
			
		macd.append(ema12[i]-ema26[i])
		
		if i <= 8:
			macd_signal_line.append(sum(macd[:i+1])/float(i+1))
		else:
			macd_signal_line.append(a9 * macd[i] + (1-a9) * macd[i-1])
			
		if i >=26:
			if macd[i] - macd_signal_line[i] < 0 and macd[i-1] - macd_signal_line[i-1] > 0:
				signals.append([date[i], "Sell", adj[i]])
			elif macd[i] - macd_signal_line[i] > 0 and macd[i-1] - macd_signal_line[i-1] < 0:
				signals.append([date[i], "Buy", adj[i]])
		
	return signals
			
def buy_and_hold(data):
	date = data[0]
	adj = data[5]
	return([["Date", "Signal", "Price"], [date[0], "Buy", adj[0]]])	
