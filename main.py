from rtree import *
from knn import *

def main():
	
	a=RTree()

	rec1=Rectangle(1,2,2,1)
	rec2=Rectangle(3,4,4,3)
	rec3=Rectangle(9,10,10,9)
	rec4=Rectangle(14,15,15,14)
	rec5=Rectangle(20,22,22,20)
	rec6=Rectangle(25,27,27,25)
	rec7=Rectangle(30,32,32,30)
	rec8=Rectangle(35,36,36,35)
	rec9=Rectangle(40,45,45,40)
	rec10=Rectangle(50,53,53,50)
	rec11=Rectangle(5,6,6,5)
	rec12=Rectangle(7,8,8,7)
	rec13=Rectangle(55,57,57,55)
	rec14=Rectangle(60,62,62,60)
	rec15=Rectangle(65,66,66,65)
	rec16=Rectangle(90,100,100,90)
	rec17=Rectangle(60,70,65,60)
	rec18=Rectangle(150,200,170,140)
	rec19=Rectangle(80,100,90,90)
	rec20=Rectangle(12,32,32,12)

	p1="w1"
	p2="w2"
	p3="w3"
	p4="w4"
	p5="w5"
	p6="w6"
	p7="w7"
	p8="w8"
	p9="w9"
	p10="w10"
	p11="w11"
	p12="w12"
	p13="w13"
	p14="w14"
	p15="w15"
	p16="w16"
	p17="w17"
	p18="w18"
	p19="w19"
	p20="w20"

	#Inserting 20 rectangles 
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
	a.insert(rec16,p16)
	a.insert(rec17,p17)
	a.insert(rec18,p18)
	a.insert(rec19,p19)
	a.insert(rec20,p20)
	
	#R-Tree Representaion
	print("\n",30 * "-" , "R-Tree Representaion" , 30 * "-","\n",)
	a.visualizer()
	
	#Look-Up for rec
	print("\n",30 * "-" , "Look-Up for Point(62,65)" , 30 * "-","\n",)
	p=Point(62,65)
	print(a.lookup(p))
	
	#Finding n nearest neighbours to the point p  (In this case : 5 nearest rectangles to the point p(1,2))
	print("\n",30 * "-" , "KNN (5 Nearest Neighbours to Point(1,2))" , 30 * "-","\n",)
	p=Point(1,2)
	nns(p,a,5)

	#Deleting rec1 (and R-Tree Representation after deleting rec1)
	print("\n",30 * "-" , "Deletion (for w4)" , 30 * "-","\n",)
	a.delete(rec4)
	a.visualizer()
	
if __name__ == '__main__':
	main()	