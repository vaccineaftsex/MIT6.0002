class food(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.calories = w
    def getvalue(self):
        return self.value
    def getweight(self):
        return self.calories
    def density(self):
        return self.value/self.calories
    def __str__(self):
        return self.name + '<value>' + self.value + '<calories>' + self.calories

def buildmenus(names, values, calories):
    menu = []
    for i in range(len(names)):
        menu.append(food(names[i], values[i], calories[i]))
    return menu

def greedy(menu, constraint, keyFunction):
    maxval, weight = 0, 0
    sortedmenu = sorted(menu, key = keyFunction, reverse = True)
    for i in range(len(sortedmenu)):
        if weight + sortedmenu[i].calories <= constraint:
            weight += sortedmenu[i].calories
            maxval += sortedmenu[i].value
    return(maxval)

def testgreedys(menu, constraint):
    print('value:' + str(greedy(menu, constraint, food.getvalue)))
    print('weight:' + str(greedy(menu, constraint, lambda x:1/food.getweight(x))))
    print('density:' + str(greedy(menu, constraint, food.density)))

names = ['wine', 'beer', 'pizza', 'burger', 'fries',
         'cola', 'apple', 'donut']
values = [89,90,95,100,90,79,50,10]
calories = [123,154,258,354,365,150,95,195]
menu = buildmenus(names, values, calories)
testgreedys(menu, constraint = 750)
