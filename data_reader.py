import re

def read_stock_data(ticker):
	#formatted to work with Yahoo Finance data
	try: 
		f = open(ticker + ".csv")
	except:
		print("something isn't right")
		return None
		
	table = f.read();
	
	rows = re.split("\n", table) #split data into rows, line by line
	rows = rows[1:-1] #get rid of the heading and last (empty) row
	
	date, op, hi, lo, cl, adj, vo = [[] for i in range(7)]
	#initialize columns
	
	for i in range(len(rows)): #every row, add data point to each column
		cols = re.split(",", rows[i])
		date.append(cols[0])
		try:
			op.append(float(cols[1]))
			hi.append(float(cols[2]))
			lo.append(float(cols[3]))
			cl.append(float(cols[4]))
			adj.append(float(cols[5]))
			vo.append(float(cols[6]))
		except: #if there is no data for a particular date, repeat last bar
			op.append(op[-1])
			hi.append(hi[-1])
			lo.append(lo[-1])
			cl.append(cl[-1])
			adj.append(adj[-1])
			vo.append(vo[-1])
		
	return date, op, hi, lo, cl, adj, vo

