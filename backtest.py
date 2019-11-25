import data_reader
import strategies

class backtest:
	def __init__(self, data, strategy):
		self.date = data[0]
		self.op = data[1]
		self.hi = data[2]
		self.lo = data[3]
		self.cl = data[4]
		self.adj = data[5]
		self.vo = data[6]
		self.signals = strategy(self.date, self.adj)
		self.holding_period_long = 100
		self.holding_period_short = 6
		
	def calculate_profits(self):
		signals_copy = list(self.signals)
		equity = 100000 #start with $100,000 cash
		shares = 0
		shorts = 0
		position_size = 1000
		positions = []
		portfolio = [["Date", "Account value", "Long shares of AAPL", "Short shares of AAPL"]]

		for i in range(len(self.date)):
			for each in positions:
				each[2] -= 1
				if each[2] == 0:
					if each[0] == "long":
						shares -= each[1]
						equity += each[1] * self.adj[i]
					elif each[0] == "short":
						shorts -= each[1]
						equity -= each[1] * self.adj[i] 
					positions.remove(each)
			
			if len(signals_copy) > 1 and self.date[i] == signals_copy[1][0]:
				if signals_copy[1][1] == "Buy":
					units = min(position_size, int(equity/self.adj[i]))
					units -= units % 100
					shares += units
					equity -= self.adj[i] * units
					positions.append(["long", units, self.holding_period_long])
				elif signals_copy[1][1] == "Sell":
					units = position_size
					shorts += units
					equity += units * self.adj[i]
					positions.append(["short", units, self.holding_period_short])
				signals_copy.remove(signals_copy[1])
	
			portfolio.append([self.date[i], equity + self.adj[i]*shares - 
				self.adj[i]*shorts, shares, shorts])
	
		return portfolio

	def optimize_holding_period(max_long=100,max_short=10): #very simple, brute force optimization
		best = [0, 0, 0]
		for l in range(max_long):
			for m in range(max_short):
				self.holding_period_long = l+1
				self.holding_period_short = m+1
				profits = calculate_profits()[-1][1] 		
				if profits > best[2]:
					best = [l+1, m+1, profits]
		
		self.holding_period_long = best[0]
		self.holding_period_short = best[1]
		return best
	
data = data_reader.read_stock_data("AAPL")
strategy = strategies.sma_crossover #


test = backtest(data, strategy)
print(test.calculate_profits()[-1]) #calculate profits returns an array of dates and the account value on each date



