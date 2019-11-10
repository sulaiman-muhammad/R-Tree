from rtree import *

def whereami(a):
	x=input("Enter your Co-Ordinates : ")
	l=x.split(" ")
	p=Point(int(l[0]),int(l[1]))
	z=a.lookup(p)
	if z!=[]:
		print("YOU ARE IN : ",z)
	else:
		print("YOU ARE CLOSEST TO : ",end='')
		nns(p,a,1)

class nns:
	def __init__(self,point,r,k=1,name=None):
		self.neighbour=[None for i in range(k)]
		self.md=[float('inf') for i in range(k)]
		self.max=[float('inf'),0]
		if name==None:
			self.nearest(point,r.root)
		else:
			self.nearestkey(point,r.root,name)
		l=[]
		for i in range(k):
			l.append((self.neighbour[i],self.md[i]))
		l.sort(key=lambda x:x[1])
		print(l)

	def nearest(self,point,node):
		if type(node)==Rnode_Internal:
			for i in range(4):
				if node.p[i]==None:
					return
				m=self.mindist(point,node.bb[i])
				if m<self.max[0]:
					self.nearest(point,node.p[i])
		if type(node)==Rnode_Leaf:
			for i in range(4):
				if node.p[i]==None:
					return
				m=self.mindist(point,node.bb[i])
				if m<self.max[0]:
					self.neighbour[self.max[1]]=node.p[i]
					self.md[self.max[1]]=m

					self.max=[self.md[0],0]
					for i in range(len(self.md)):
						if self.md[i]>self.max[0]:
							self.max[0]=self.md[i]
							self.max[1]=i

	def nearestkey(self,point,node,key):
		if type(node)==Rnode_Internal:
			for i in range(4):
				if node.p[i]==None:
					return
				m=self.mindist(point,node.bb[i])
				if m<self.max[0]:
					self.nearestkey(point,node.p[i],key)
		if type(node)==Rnode_Leaf:
			for i in range(4):
				if node.p[i]==None:
					return
				if key==node.p[i][0]:
					m=self.mindist(point,node.bb[i])
					if m<self.max[0]:
						self.neighbour[self.max[1]]=node.p[i]
						self.md[self.max[1]]=m

						self.max=[self.md[0],0]
						for i in range(len(self.md)):
							if self.md[i]>self.max[0]:
								self.max[0]=self.md[i]
								self.max[1]=i

	def mindist(self,point,rec):
		dist=0
		if rec.ux>point.x:
			dist+=(point.x-rec.ux)**2
		elif rec.lx<point.x:
			dist+=(point.x-rec.lx)**2
		if rec.uy<point.y:
			dist+=(point.y-rec.uy)**2
		elif rec.ly>point.y:
			dist+=(point.y-rec.ly)**2
		return dist

def print_menu():
	print(40 * "-" , "MENU" , 40 * "-")
	print("1. Visualizer (R-Tree representaion of our Map objects) ")
	print("2. What's around Me? (Displays n nearest Places based on a Co-Ordinate input) ")
	print("3. Where am I? (Displays your current location) ")
	print("4. Nearby particular Place (Displays n nearest particular Place [eg: School,Hospital]) ")
	print("5. Insert Utility ")
	print("6. Exit")

def main():
	
	a=RTree()

	rec1=Rectangle(3,23,9,20)
	rec2=Rectangle(1,5,5,2)
	rec3=Rectangle(2,17,6,13)
	rec4=Rectangle(2,10,5,8)
	rec5=Rectangle(1,7,3,6)
	rec6=Rectangle(13,23,15,20)
	rec7=Rectangle(10,17,16,14)
	rec8=Rectangle(7,6,9,4)
	rec9=Rectangle(14,11,18,9)
	rec10=Rectangle(11,7,16,3)
	rec11=Rectangle(16,19,18,18)
	rec12=Rectangle(3,19,5,18)
	rec13=Rectangle(8,9,10,8)
	rec14=Rectangle(9,13,12,11)
	rec15=Rectangle(7,17,9,15)

	p1=["Restaurant","Red-Rock"]
	p2=["School","DPS"]
	p3=["School","IHS"]
	p4=["Shop","Nandini"]
	p5=["ATM","ICICI"]
	p6=["School","OOEHS"]
	p7=["Restaurant","Pit-Stop"]
	p8=["Shop","Nescafe"]
	p9=["Restaurant","Sai-Suraj"]
	p10=["Hospital","Srinivas"]
	p11=["ATM","SBI"]
	p12=["ATM","Axis"]
	p13=["ATM","Canara"]
	p14=["Shop","Amul"]
	p15=["Restaurant","Ocean-Pearl"]

	a.insert(rec1,p1)
	a.insert(rec2,p2)
	a.insert(rec3,p3)
	a.insert(rec4,p4)
	a.insert(rec5,p5)
	a.insert(rec6,p6)
	a.insert(rec7,p7)
	a.insert(rec8,p8)
	a.insert(rec9,p9)
	a.insert(rec10,p10)
	a.insert(rec11,p11)
	a.insert(rec12,p12)
	a.insert(rec13,p13)
	a.insert(rec14,p14)
	a.insert(rec15,p15)
	
	loop=True

	while loop:
		print_menu()   
		choice =int(input("Enter your choice [1-6]: "))
		if choice==1:
			print(40 * "-" , "VISUALIZER" , 40 * "-")
			a.visualizer()
		elif choice==2:
			print(40 * "-" , "WHAT'S AROUND ME?" , 40 * "-")
			x=input("Enter your Co-Ordinates : ")
			n=int(input("How many? : "))
			l=x.split(" ")
			p=Point(int(l[0]),int(l[1]))
			nns(p,a,n)
		elif choice==3:
			print(40 * "-" , "WHERE AM I?" , 40 * "-")
			whereami(a)
		elif choice==4:
			print(40 * "-" , "NEARBY PARTICULAR PLACE" , 40 * "-")
			x=input("Enter your Co-Ordinates : ")
			key=input("What are you looking for? [School,Restaurant,Shop,Hospital,ATM] : ")
			n=int(input("How many? : "))
			l=x.split(" ")
			p=Point(int(l[0]),int(l[1]))
			nns(p,a,n,key)
		elif choice==5:
			ut=input("What Utility? : ")
			n=input("Name? :  ")
			p=[ut,n]
			x=input("Upper-Left Co-Ordinates : ")
			u=x.split(" ")
			x=input("Lower-Right Co-Ordinates : ")
			l=x.split(" ")
			rec=Rectangle(int(u[0]),int(u[1]),int(l[0]),int(l[1]))
			a.insert(rec,p)
		elif choice==6:
			loop=False
		else:
			print("Wrong option selection. Enter any key to try again..")

if __name__ == '__main__':
	main()	