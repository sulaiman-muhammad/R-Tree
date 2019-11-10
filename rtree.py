class Point:

	def __init__(self,x,y):
		self.x=x
		self.y=y

class Rectangle:

	def __init__(self,ux,uy,lx,ly):
		#upper left(u) to lower right(l)
		self.ux=ux
		self.uy=uy
		self.lx=lx
		self.ly=ly

	def is_present(self,item):
		#the origin is at the bottom left
		if (type(item)==Point):
			if (self.ux<=item.x<=self.lx and self.ly<=item.y<=self.uy):
				return True

		elif (type(item)==Rectangle):
			if(self.ux<=item.ux<=self.lx and self.ly<=item.uy<=self.uy and self.ux<=item.lx<=self.lx and self.ly<=item.ly<=self.uy):
				return True
		return False

	def size(self):
		return (self.lx-self.ux)*(self.uy-self.ly)

	def __str__(self):
		return ("Rectange:  "+str(self.ux)+" "+str(self.uy)+" "+str(self.lx)+" "+str(self.ly)+" \n")

class Rnode_Internal:

	def __init__(self,parent=None,rec1=None,p1=None,rec2=None,p2=None,rec3=None,p3=None,rec4=None,p4=None):
		self.bb=[None]*4
		self.p=[None]*4
		self.bb[0]=rec1
		self.p[0]=p1
		self.bb[1]=rec2
		self.p[1]=p2
		self.bb[2]=rec3
		self.p[2]=p3
		self.bb[3]=rec4
		self.p[3]=p4
		self.parent=parent

class Rnode_Leaf:

	def __init__(self,parent=None,rec1=None,p1=None,rec2=None,p2=None,rec3=None,p3=None,rec4=None,p4=None):
		self.bb=[None]*4
		self.p=[None]*4
		self.bb[0]=rec1
		self.p[0]=p1
		self.bb[1]=rec2
		self.p[1]=p2
		self.bb[2]=rec3
		self.p[2]=p3
		self.bb[3]=rec4
		self.p[3]=p4
		self.parent=parent

class RTree:

	def __init__(self):
		self.root=None

	def lookup(self,item,node=None):
		'''
		Go through each rectangle and check if the item searched is present in that, if it is continue further down the tree
		'''
		if node==None:
			node=self.root

		res=[]

		if(type(node)==Rnode_Internal):
			for i in range(4):
				if(node.bb[i]==None):
					break
				elif(node.bb[i].is_present(item)):
					res=res+self.lookup(item,node.p[i])

		else:
			for i in range(4):
				if(node.bb[i]==None):
					break
				elif(node.bb[i].is_present(item)):
					res.append(node.p[i])

		return res

	def insert(self,bb,p,node=None):
		'''
		Insert the entry into the rtree
		'''
		if node==None:
			node=self.root

		#If the root does not exist, create an internal node with a leaf node containing the single new entry
		if self.root==None:
			temp=Rnode_Leaf()
			temp.bb[0]=bb
			temp.p[0]=p
			self.root=Rnode_Internal(None,bb,temp)
			self.root.p[0].parent=self.root
			return

		#If the rtree exists
		l=self.choose_leaf(bb,node)


		if l.p[3]!=None:
			#If the selected leaf node is full, do a quadratic split and adjust the tree
			l1,ll,a1,a2=self.quadratic_split_node(l,bb,p)
			self.adjust_tree(l,l1,a1,ll,a2)

		else:
			#If the selected leaf node is not empty just insert the new entry into the first empty space
			for i in range(4):
				if(l.bb[i]==None):
					l.bb[i]=bb
					l.p[i]=p
					break

			#adjust the tree
			self.adjust_tree2(l,bb)

	def adjust_tree(self,node,l,a1,ll=None,a2=None):
		'''
		Adjust the covering rectangles and propogate node splits upwards
		'''
		n=l
		nn=ll
		while node!=self.root:

			#get the parent of the node and get the entry number
			p=node.parent
			for i in range(4):
				if p.p[i]==node:
					n.parent=node.parent
					p.p[i]=n
					p.bb[i]=a1
					break

			#if there is a split to be combined(i.e. the second node is not None)
			if nn!=None:
				split_flag=1
				for i in range(i+1,4):
					#if a space can be found to adjust put second node there and change the split flag to 0
					if p.p[i]==None:
						nn.parent=node.parent
						p.p[i]=nn
						p.bb[i]=a2
						split_flag=0
						break

				if split_flag==1:
					#if the node is full split the parent node again and repeat
					g1,g2,a1,a2=self.quadratic_split_node(p,a2,nn)
					if type(g1)==Rnode_Internal:
						for i in range(4):
							if g1.p[i]!=None:
								g1.p[i].parent=g1
							if g2.p[i]!=None:
								g2.p[i].parent=g2
					
					n=g1
					nn=g2
					node=node.parent

				#if there is no split, just adjust the size of the covering rectangles
				if split_flag==0:
					self.adjust_tree2(p,a1)
					return

		#if the changes go upto the root, split the root node and create a new root
		temp=Rnode_Internal()
		temp.bb[0]=a1
		temp.p[0]=n
		temp.bb[1]=a2
		temp.p[1]=nn
		self.root=temp
		self.root.p[0].parent=self.root
		self.root.p[1].parent=self.root

	def adjust_tree2(self,node,bb):
		#this just adjusts the size of the covering rectangles
		while node!=self.root:
			p=node.parent
			for i in range(4):
				if p.p[i]==node:
					break
			new_ux=min(p.bb[i].ux,bb.ux)
			new_uy=max(p.bb[i].uy,bb.uy)
			new_lx=max(p.bb[i].lx,bb.lx)
			new_ly=min(p.bb[i].ly,bb.ly)
			a1=Rectangle(new_ux,new_uy,new_lx,new_ly)
			p.bb[i]=a1
			node=node.parent

	def quadratic_split_node(self,l,bb,p):
		'''
		Divide a set of m+1 index entries into two groups
		'''
		all_bb=[l.bb[0],l.bb[1],l.bb[2],l.bb[3],bb]
		all_p=[l.p[0],l.p[1],l.p[2],l.p[3],p]
		a,b=self.pick_seeds(all_bb)

		#create two new groups of the same type g1 and g2
		if type(l)==Rnode_Leaf:
			g1=Rnode_Leaf()
			g2=Rnode_Leaf()
		else:
			g1=Rnode_Internal()
			g2=Rnode_Internal()

		#put a and b into two seperate groups
		g1.bb[0]=all_bb[a]
		area1=all_bb[a]
		g1.p[0]=all_p[a]
		g2.bb[0]=all_bb[b]
		area2=all_bb[b]
		g2.p[0]=all_p[b]

		#count number of rectangles in the two groups
		n1=1
		n2=1

		#delete the a,b from the arrays
		for index in sorted([a,b], reverse=True):
			del all_bb[index]
			del all_p[index]


		while all_bb!=[]:
			#if either group has 3 elements put the rest of the entires into the other group
			if n1>=3:
				for i in range(4):
					if g2.bb[i]==None:
						g2.bb[i]=all_bb[0]
						g2.p[i]=all_p[0]
						area2=a2
						n2=n2+1
						a=0
						del all_bb[a]
						del all_p[a]
						break
				continue
			elif n2>=3:
				for i in range(4):
					if g1.bb[i]==None:
						g1.bb[i]=all_bb[0]
						g1.p[i]=all_p[0]
						area1=a1
						n1=n1+1
						a=0
						del all_bb[a]
						del all_p[a]
						break
				continue
			
			#pick the next element to be inserted
			a=self.pick_next(all_bb,area1,area2)


			new_ux=min(all_bb[a].ux,area1.ux)
			new_uy=max(all_bb[a].uy,area1.uy)
			new_lx=max(all_bb[a].lx,area1.lx)
			new_ly=min(all_bb[a].ly,area1.ly)
			a1=Rectangle(new_ux,new_uy,new_lx,new_ly)
			d1=((new_lx-new_ux)*(new_uy-new_ly)-((area1.lx-area1.ux)*(area1.uy-area1.ly)))
			new_ux=min(all_bb[a].ux,area2.ux)
			new_uy=max(all_bb[a].uy,area2.uy)
			new_lx=max(all_bb[a].lx,area2.lx)
			new_ly=min(all_bb[a].ly,area2.ly)
			a2=Rectangle(new_ux,new_uy,new_lx,new_ly)
			d2=((new_lx-new_ux)*(new_uy-new_ly)-((area2.lx-area2.ux)*(area2.uy-area2.ly)))
			
			#add to group whose covering rectangle has to enlarged the least
			#resolve ties by adding to the group with smaller area
			if d1<d2:
				for i in range(4):
					if g1.bb[i]==None:
						g1.bb[i]=all_bb[a]
						g1.p[i]=all_p[a]
						area1=a1
						n1=n1+1
						break
			elif d1>d2:
				for i in range(4):
					if g2.bb[i]==None:
						g2.bb[i]=all_bb[a]
						g2.p[i]=all_p[a]
						area2=a2
						n2=n2+1
						break
			elif d1==d2:
				if area1.size()<area2.size():
					for i in range(4):
						if g1.bb[i]==None:
							g1.bb[i]=all_bb[a]
							g1.p[i]=all_p[a]
							area1=a1
							n1=n1+1
							break
				elif area1.size()>=area2.size():
					for i in range(4):
						if g2.bb[i]==None:
							g2.bb[i]=all_bb[a]
							g2.p[i]=all_p[a]
							area2=a2
							n2=n2+1
							break
			del all_bb[a]
			del all_p[a]

		return g1,g2,area1,area2

	def pick_next(self,bb,ga1,ga2):
		#choose next entry to classify into the group
		d_max=-1
		p1=-1
		for i in range(len(bb)):
			new_ux=min(bb[i].ux,ga1.ux)
			new_uy=max(bb[i].uy,ga1.uy)
			new_lx=max(bb[i].lx,ga1.lx)
			new_ly=min(bb[i].ly,ga1.ly)
			d1=((new_lx-new_ux)*(new_uy-new_ly)-((ga1.lx-ga1.ux)*(ga1.uy-ga1.ly)))
			new_ux=min(bb[i].ux,ga2.ux)
			new_uy=max(bb[i].uy,ga2.uy)
			new_lx=max(bb[i].lx,ga2.lx)
			new_ly=min(bb[i].ly,ga2.ly)
			d2=((new_lx-new_ux)*(new_uy-new_ly)-((ga2.lx-ga2.ux)*(ga2.uy-ga2.ly)))
			d=abs(d1-d2)
			if d_max<d:
				d_max=d
				p1=i
			#d1 area increase to include in g1
			#d2 area increase to include in g2
			#select the one with maximum difference between d1 and d2
		return p1

	def pick_seeds(self,bb):
		'''
		selects the two entries with the most wasteful space
		'''
		d_max=-1
		p1=-1
		p2=-1
		for i in range(5):
			for j in range(i+1,5):
				new_ux=min(bb[i].ux,bb[j].ux)
				new_uy=max(bb[i].uy,bb[j].uy)
				new_lx=max(bb[i].lx,bb[j].lx)
				new_ly=min(bb[i].ly,bb[j].ly)
				area=((new_lx-new_ux)*(new_uy-new_ly))
				d=area-((bb[i].lx-bb[i].ux)*(bb[i].uy-bb[i].ly))-((bb[j].lx-bb[j].ux)*(bb[j].uy-bb[j].ly))
				if d_max<d:
					d_max=d
					p1=i
					p2=j

		return p1,p2

	def choose_leaf(self,bb,node=None):
		'''
		Find the leaf in which to put the entry
		'''
		if node==None:
			node=self.root

		if(type(node)==Rnode_Internal):
			l=[]
			maximum_size=4
			for i in range(4):
				if node.bb[i]==None:
					maximum_size=i
					break
				elif(node.bb[i].is_present(bb)):
					#If the entry rectangle fits in a paticular rectangle, that rectangle is selected
					return self.choose_leaf(node.bb[i],node.p[i])
				else:
					#If the entry rectangle has dimensions outside the existing rectangles, the new area to include the data rectangle is calulated
					new_ux=min(bb.ux,node.bb[i].ux)
					new_uy=max(bb.uy,node.bb[i].uy)
					new_lx=max(bb.lx,node.bb[i].lx)
					new_ly=min(bb.ly,node.bb[i].ly)
					area=((new_lx-new_ux)*(new_uy-new_ly))
					l.append(area)

			min_area=l[0]
			min_index=0

			i=0
			#find the rectangle with minimum area and choose that node pointer
			for i in range(1,maximum_size):
				if l[i]<min_area:
					min_area=l[i]
					min_index=i
			return self.choose_leaf(node.bb[i],node.p[i])

		else:
			#if the node is a leaf, return that node
			return node
	
	def visualizer(self,node=None,d=0):
		#just a debigging tool to visualize the tree
		if node==None:
			node=self.root
		if type(node)==Rnode_Internal:
			for i in range(4):
				if node.p[i]==None:
					break
				print(node.bb[i])
				self.visualizer(node.p[i],d+1)
		else:
			for i in range(4):
				print(node.bb[i],"  ",node.p[i]," ---- ")
			return

	def delete(self,obj):
		'''
		delete the record and update the tree
		'''
		#locate the record to be deleted in the tree
		res=self.findleaf(obj)

		if res[0]==None:
			print("Does not exist")
			return
		
		else:
			#delete the record
			lnode=res[0]
			index=res[1]

			lnode.p[index]=None
			lnode.bb[index]=None

			i=index

			for i in range(index+1,4):
				if lnode.p[i]==None:
					break
			i=i-1
			lnode.p[index]=lnode.p[i]
			lnode.bb[index]=lnode.bb[i]
			lnode.p[i]=None
			lnode.bb[i]=None

			#propogate the changes upward
			self.condense(lnode)

		#if the root contains only one element at the end, make that the new root
		if type(self.root.p[0])==Rnode_Internal and self.root.p[1]==None:
			self.root=self.root.p[0]

	def get_entries(self,node,res=[]):
		if type(node)==Rnode_Internal:
			for i in range(4):
				if node.p[i]==None:
					break
				res=self.get_entries(node.p[i],res) 
		else:
			for i in range(4):
				if node.p[i]==None:
					break
				res.append((node.bb[i],node.p[i]))
		return res

	def condense(self,lnode,Q=[]):

		if lnode==self.root:
			#reinsert other entries at the end
			while Q!=[]:
					node=Q.pop()
					res=self.get_entries(node)
					for i in res:
						self.insert(i[0],i[1])
			return

		i=0

		for i in range(4):
			if lnode.p[i]==None:
				break

		#if the entries is less than M/2
		if i<2:
			#get parent
			N=lnode
			P=lnode.parent

			for i in range(4):
				if P.p[i]==lnode:
					break

			#add the remaining nodes to the reinsertion list
			Q.append(lnode)

			#delete the entry
			P.bb[i]=None
			P.p[i]=None
			index=i

			for i in range(i+1,4):
				if P.p[i]==None:
					break

			#rearrange the remaining entries in that node
			i=i-1
			P.p[index]=P.p[i]
			P.bb[index]=P.bb[i]
			P.p[i]=None
			P.bb[i]=None
			N=lnode.parent

			#propogate changes upward
			self.condense(N,Q)
			return


		else:
			#get parent and just update the covering rectangle
			P=lnode.parent
			for i in range(4):
				if P.p[i]==lnode:
					ind=i
					break
			uxnew=1e8
			uynew=0
			lxnew=0
			lynew=1e8
			for i in range(4):
				if lnode.p[i] != None:
					uxnew=min(uxnew,lnode.bb[i].ux)
					uynew=max(uynew,lnode.bb[i].uy)
					lxnew=max(lxnew,lnode.bb[i].lx)
					lynew=min(lynew,lnode.bb[i].ly)
			P.bb[ind].ux=uxnew
			P.bb[ind].uy=uynew
			P.bb[ind].lx=lxnew
			P.bb[ind].ly=lynew
			N=lnode.parent
			self.condense(N,Q)

	def findleaf(self,item,node=None):
		y=None
		x=None
		if node==None:
			node=self.root
		if(type(node)==Rnode_Internal):
			
			for i in range(4):
				if(node.bb[i]==None):
					break
				elif(node.bb[i].is_present(item)):
					y=self.findleaf(item,node.p[i])
					if y!=None:
						return y
		else:
			for i in range(4):
				if(node.bb[i]==None):
					break
				elif(node.bb[i].is_present(item)):
					y=node
					x=i
					return y,x