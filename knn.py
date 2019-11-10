from rtree import *
from operator import itemgetter


class nns:
	'''
	mindist is the minimum distance of the point from the rectangle
	'''
	def __init__(self,point,r,k=1):
		self.neighbour=[None for i in range(k)]
		self.md=[float('inf') for i in range(k)]
		self.max=[float('inf'),0]
		self.knn(point,r.root)
		l=[]
		for i in range(k):
			l.append((self.neighbour[i],int(self.md[i])))
		l.sort(key=lambda x:x[1])
		print(l)

	def knn(self,point,node):
		'''
		compare the current mindist to the rectangle and only visit if there is a possiblility of the distance being less
		'''
		if type(node)==Rnode_Internal:
			for i in range(4):
				if node.p[i]==None:
					return
				m=self.mindist(point,node.bb[i])
				if m<self.max[0]:
					self.knn(point,node.p[i])


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