import numpy as np

# print("!")
# mass=[]
# for i in mass:
#     for j in i:
#         print(j,i[j]) 
# mas=[1,2,3,4,5,6,7]
# mas=mas[1:]
# def Turn(met):
#     #print(Split_dict[0][0])
#     #print("here")
#     turn=[]
#     turn.append(np.flip(met))
#     return turn
#     #print(time[0])
#     #print(Split_dict[0][0])
# mas=Turn(mas)
# print(mas)

class drink:
    def __init__(self,name):
        self.t=name
class food:
    i=drink("cola")
    def __init__(self,name):
        self.name=name
    def show(self):
        print(self.i.t)
        #print(i.k)
var=food("pizza")
var.show()

array=[0,1,2,3,4,5]
print(array)
array.reverse()
print(array)
np.flip(array)
print(array)
arr=np.arange(0,10,1)
print(arr)
arr=np.flip(arr)
print(arr)
# class vary:
#     k=0
#     z=3
#     def show():
#         print(vary.z)

# var=vary
# var.show()