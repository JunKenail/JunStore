import numpy as np

class Node:
    def __init__(self, value = None):
        self.value = value
        self.father = None
        self.lchild = None
        self.rchild = None

class KDtree:
    def __init__(self):
        self.root = None

    def creatkdtree(self, d, k ,dimension):  # 从第k维开始比较
        self.dimension = dimension
        self.k = k
        self.data = d
        d = sorted(d, key=lambda x: x[(k - 1) % self.dimension])  # dimension维数据
        i = int((len(d) + 1) / 2 - 1
                if len(d) % 2 == 1 else len(d) / 2 - 1)
        node = Node(d[i])
        self.root = node
        self.root.father = None
        qd = [d]
        qn = [self.root]
        while len(qd) != 0:
            pop_data = qd.pop(0)
            pop_node = qn.pop(0)
            i = int((len(pop_data) + 1) / 2 - 1
                    if len(pop_data) % 2 == 1 else len(pop_data) / 2 - 1)
            k += 1
            if len(pop_data) == 1:
                pop_node.lchild = Node(pop_data[0])
                pop_node.lchild.father = pop_node
            else:
                if i == 0:
                    ldata = pop_data[0:1]
                else:
                    ldata = pop_data[0:i]
                if len(ldata) > 1:
                    ldata = sorted(ldata, key=lambda x: x[(k - 1) % self.dimension])
                rdata = pop_data[i + 1:]
                if len(rdata) > 1:
                    rdata = sorted(rdata, key=lambda x: x[(k - 1) % self.dimension])
                i1 = int((len(ldata) + 1) / 2 - 1 if len(ldata) % 2 == 1 else len(ldata) / 2 - 1)
                pop_node.lchild = Node(ldata[i1])
                pop_node.lchild.father = pop_node
                i2 = int((len(rdata) + 1) / 2 - 1 if len(rdata) % 2 == 1 else len(rdata) / 2 - 1)
                pop_node.rchild = Node(rdata[i2])
                pop_node.rchild.father = pop_node
                if len(ldata) > 1:
                    ldata.pop(i1)
                    qd.append(ldata)
                    qn.append(pop_node.lchild)
                if len(rdata) > 1:
                    rdata.pop(i2)
                    qd.append(rdata)
                    qn.append(pop_node.rchild)

    def printkdtree(self):
        print("The kdtree of "+str(self.data)+" is:")
        nl = [self.root]
        while len(nl) != 0:
            pop_node = nl.pop(0)
            if pop_node.lchild is None:
                lstr = str(None)
            else:
                lstr = str(pop_node.lchild.value)
            if pop_node.rchild is None:
                rstr = str(None)
            else:
                rstr = str(pop_node.rchild.value)
            print(str(pop_node.value)+":"+lstr+"/"+rstr)
            if pop_node.lchild is not None:
                nl.append(pop_node.lchild)
            if pop_node.rchild is not None:
                nl.append(pop_node.rchild)

    def getroot(self):
        print("\n"+"Root:"+str(self.root.value))
        return self.root

    def getlevels(self):
        levels = []
        for leaf in self.leaves:
            l = 1
            temp = leaf
            while temp != self.root:
                temp = temp.father
                l += 1
            levels.append(l)
        print("Levels:" + str(max(levels)))
        return max(levels)

    def getleaves(self):
        print("Leaves:",end='')
        q = [self.root]
        leaves = []
        while len(q) != 0:
            node = q.pop(0)
            if (node.lchild is None) & (node.rchild is None):
                leaves.append(node)
                print(str(node.value), end=' ')
            if node.lchild is not None:
                q.append(node.lchild)
            if node.rchild is not None:
                q.append(node.rchild)
        print()
        self.leaves = leaves
        return leaves

    def searchthenearestpoint(self, x):
        print("\nSearching starting...")
        time = 1
        current_nearest_node = self.root
        k = self.k
        while (current_nearest_node.lchild != None) or (current_nearest_node.rchild != None):
            if (current_nearest_node.lchild != None) and (current_nearest_node.rchild != None):
                if x[(k-1) % self.dimension] < current_nearest_node.value[(k-1) % self.dimension]:
                    current_nearest_node = current_nearest_node.lchild
                else:
                    current_nearest_node = current_nearest_node.rchild
            elif current_nearest_node.lchild != None:
                current_nearest_node = current_nearest_node.lchild
            elif current_nearest_node.rchild != None:
                current_nearest_node = current_nearest_node.rchild
            #print(current_nearest_node.value)
            k += 1
        d = self.distance(x, current_nearest_node.value)
        print("Time "+str(time)+":the current nearest point(leaf) is "+str(current_nearest_node.value)
              +"with the distance of "+str(d))
        temp = current_nearest_node
        backnode = current_nearest_node
        while backnode != self.root:
            backnode = backnode.father
            d2 = self.distance(backnode.value, x)
            if d2 < d:
                current_nearest_node = backnode
                d = d2
                time += 1
                print("Time " + str(time) + ":the current nearest point is "
                      + str(current_nearest_node.value)+" with the distance of "+str(d))
                if backnode.lchild != None:
                    if (backnode.lchild == temp) and (backnode.rchild != None):
                        d3 = self.distance(backnode.rchild.value, x)
                        if d3 < d:
                            current_nearest_node = backnode.rchild
                            d = d3
                            time += 1
                            print("Time " + str(time) + ":the current nearest point is " + str(
                                current_nearest_node.value)+" with the distance of "+str(d))
                    else:
                        d3 = self.distance(backnode.lchild.value, x)
                        if d3 < d:
                            current_nearest_node = backnode.lchild
                            d = d3
                            time += 1
                            print("Time " + str(time) + ":the current nearest point is " + str(
                                current_nearest_node.value)+" with the distance of "+str(d))
        print("Searching ending...")
        print("Finally,the nearest point is:"+str(current_nearest_node.value)+" with the distance of "+str(d))
        return current_nearest_node,d

    def distance(self, x, y):
        return sum(map(lambda z: z**2, list(np.array(x)-np.array(y))))



def main():
    data = [[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]]  # 二维数据
    data = [[2, 3, 1], [5, 4, 7], [9, 6, 2], [4, 7, 3], [8, 1, 5], [7, 2, 6]]  # 三维数据
    newkdtree = KDtree()
    newkdtree.creatkdtree(data, 1, 3)
    newkdtree.printkdtree()
    newkdtree.getroot()
    newkdtree.getleaves()
    newkdtree.getlevels()
    x = [3,4.5,6]
    newkdtree.searchthenearestpoint(x)
    print("\nVerifyng：\nAll the distance by calculating ditectly is: ",end='')
    dn = []
    for d in data:
        dn.append(newkdtree.distance(d,x))
        print(newkdtree.distance(d, x),end=' ')
    print("\nThe nearest distance by calculating ditectly is："+str(min(dn)), end='')


if __name__ == '__main__':
    main()








