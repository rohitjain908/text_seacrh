from django.shortcuts import render
from .models import *


# Create your views here.


def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products' : products})


def editDistance(str1, str2):
    str1 = str1.lower()
    str2 = str2.lower()
    a = len(str1)
    b = len(str2)
    string_matrix = [[0 for i in range(b+1)] for i in range(a+1)]
    for i in range(a+1):
        for j in range(b+1):
            if i == 0:
                string_matrix[i][j] = j   # If first string is empty, insert all characters of second string into first.
            elif j == 0:
                string_matrix[i][j] = i   # If second string is empty, remove all characters of first string.
            elif str1[i-1] == str2[j-1]:
                string_matrix[i][j] = string_matrix[i-1][j-1]  # If last characters of two strings are same, nothing much to do. Ignore the last two characters and get the count of remaining strings.
            else:
                string_matrix[i][j] = 1 + min(string_matrix[i][j-1],      # insert operation
                                       string_matrix[i-1][j],      # remove operation
                                       string_matrix[i-1][j-1])    # replace operation
    return string_matrix[a][b]


##version- 1

# def search(request, inputText):
#     #print(inputText)

#     ##compare with productName
#     filterProducts = []

#     threshold = 2

#     products = Product.objects.all()
#     for product in products:
#         #compare with name
#         distanceBetweenName = editDistance(inputText, product.name)
#         print("distanceBetweenName ", distanceBetweenName)

#         #compare with brand
#         distanceBetweenBrand = editDistance(inputText, product.brand)

#         #compare with category
#         distanceBetweenCategory = editDistance(inputText, product.category)

#         #compare with subcategory
#         distanceBetweenSubCategory = editDistance(inputText, product.subCategory)

#         if distanceBetweenName < threshold or \
#         distanceBetweenBrand < threshold or \
#         distanceBetweenCategory < threshold or \
#         distanceBetweenSubCategory < threshold:

#             filterProducts.append(product)


#     return render(request, 'index.html', {'products' : filterProducts})


#version-2(key-value mapping)


# def search(request, inputText):
#     filterProductsID = set()

#     threshold = 2

#     for valueObject in DictKeyValue.objects.all():
#         distance = editDistance(inputText, valueObject.value)
#         keyObject =  valueObject.container
#         type = keyObject.type.lower()


#         if type == 'name':
#             if distance < threshold:
#                 products = Product.objects.all().filter(name = keyObject.name)
#                 for product in products:
#                     filterProductsID.add(product.id)

#         elif type == 'category':
#             #print("here ", valueObject.value, distance, inputText)
#             if distance < threshold:
                
#                 products = Product.objects.all().filter(category = keyObject.name)
#                 for product in products:
#                     filterProductsID.add(product.id)

#         elif type == 'brand':
#             if distance < threshold:
#                 products = Product.objects.all().filter(brand = keyObject.name)
#                 for product in products:
#                     filterProductsID.add(product.id)


        

#     filterProducts = []
#     for id in filterProductsID:
#         filterProducts.append(Product.objects.get(id = id))



#     return render(request, 'index.html', {'products' : filterProducts})



##version-3 

# soundex algo
# key value mapping
# input spliting on the basis of space
    

def soundexCode(word):

    if len(word) == 0:
        return ""

    mapping = dict()

    mapping['a'] = mapping['e'] = mapping['i'] = mapping['o'] \
    = mapping['u'] = mapping['h'] = mapping['w'] = mapping['y'] = '0'

    mapping['b'] = mapping['f'] = mapping['p'] = mapping['v'] = '1'

    mapping['c'] = mapping['g'] = mapping['j'] = mapping['k'] \
    = mapping['q'] = mapping['s'] = mapping['x'] = mapping['z'] = '2'

    mapping['d'] = mapping['t'] = '3'

    mapping['l'] = '4'

    mapping['m'] = mapping['n'] = '5'

    mapping['r'] = '6'


    code = word[0].upper()
    codeLength = 1


    for i in range(1, len(word)):
        c = word[i].lower()
        if c >= 'a' and c <= 'z':
            if mapping[c] != '0':
                if mapping[c] != code[codeLength - 1]:
                    code = code + mapping[c]
                    codeLength = codeLength + 1

                if codeLength > 3:
                    break

    
    if codeLength <= 3:
        while codeLength <= 3:
            code = code + "0"
            codeLength = codeLength + 1

    return code



def splitString(inputText):
    result = []
    temp = ""
    for c in inputText:
        if c == ' ':
            if temp != "":
                result.append(temp)
            temp = ""
        else:
            temp = temp + c
    if temp != "":
        result.append(temp)

    return result


import math

def distance(c1, c2):
    if c1 < 'a' or c1 > 'z':
        return 20
    if c2 < 'a' or c2 > 'z':
        return 20
    arr = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
           ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
           ['z', 'x', 'c', 'v', 'b', 'n', 'm']]
    

    row = dict()
    column = dict()

    for i in range(0, 3):
        for j in range(0, len(arr[i])):
            row[arr[i][j]] = i
            column[arr[i][j]] = j

    x1 = row[c1]
    y1 = column[c1]
    x2 = row[c2]
    y2 = column[c2]

    dist = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
    dist = math.sqrt(dist)

    return dist
    
## abce
## abdg

##""

## "a"

## abc

##i = 4, j = 4

def editDistanceWithDifferentCost(str1, str2):
    str1 = str1.lower()
    str2 = str2.lower()
    a = len(str1)
    b = len(str2)
    x = 0.2
    y = 0.2
    string_matrix = [[0.0 for i in range(b+1)] for i in range(a+1)]
    for i in range(a+1):
        for j in range(b+1):
            if i == 0:
                string_matrix[i][j] = j * x   # If first string is empty, insert all characters of second string into first.
            elif j == 0:
                string_matrix[i][j] = i * y # If second string is empty, remove all characters of first string.
            elif str1[i-1] == str2[j-1]:
                string_matrix[i][j] = string_matrix[i-1][j-1]  # If last characters of two strings are same, nothing much to do. Ignore the last two characters and get the count of remaining strings.
            else:
                string_matrix[i][j] =  min(string_matrix[i][j-1] + x,      # insert operation
                                       string_matrix[i-1][j] + y,      # remove operation
                                        distance(str1[i - 1], str2[j - 1])*0.1 + string_matrix[i-1][j-1])    # replace operation
    return string_matrix[a][b]




def cost(costBetweenCode, costBetweenWords, wordCode, keywordCode):
    Max = 2.5
    if costBetweenCode == 0:
        return 0
    
    
    c1 = wordCode[0].lower()
    c2 = keywordCode[0].lower()
    
    if c1 != c2:
        if distance(c1, c2) > 1:
            return Max
        

    
    return costBetweenCode + costBetweenWords


## for a word:-
## will take the minimum cost from all keyword related to a product

## then add the distance of all words cost

def search(request, inputText):
    splitWords = splitString(inputText)
    costOfProducts = dict()

    sumOfCost = dict()
    minimumOfCost = dict()
    
    for word in splitWords:
        wordCode = soundexCode(word)


        for valueObject in DictKeyValue.objects.all():
            keyObject =  valueObject.container
            keyword = valueObject.value
            typeOfKeyword = keyObject.type.lower()

            keywordCode = soundexCode(keyword)
            
            costBetweenWords = editDistanceWithDifferentCost(word, keyword)
            costBetweenCode = editDistance(wordCode, keywordCode)

            products = []

            totalCost = cost(costBetweenCode , costBetweenWords, wordCode, keywordCode)
            if typeOfKeyword == 'name':
                    products = Product.objects.all().filter(name = keyObject.name)
                        

            elif typeOfKeyword == 'category':
                    products = Product.objects.all().filter(category = keyObject.name)
                    
                    
            elif typeOfKeyword == 'brand':
                    products = Product.objects.all().filter(brand = keyObject.name)
                    
                   
            elif typeOfKeyword == 'subcategory':
                    products = Product.objects.all().filter(subCategory = keyObject.name)

            for product in products:
                productId = product.id
                if productId in costOfProducts.keys():
                    costOfProducts[productId] = min(costOfProducts[productId], totalCost)
                else:
                    costOfProducts[productId] = totalCost



        for productId in costOfProducts.keys():
            if productId in sumOfCost.keys():
                sumOfCost[productId] = sumOfCost[productId] + costOfProducts[productId]
            else:
                sumOfCost[productId] = costOfProducts[productId]

            if productId in minimumOfCost.keys():
                minimumOfCost[productId] = min(minimumOfCost[productId], costOfProducts[productId])
            else:
                minimumOfCost[productId] = costOfProducts[productId]

    
    filterProducts = set()
    for productId in sumOfCost.keys():
        filterProducts.add((minimumOfCost[productId], sumOfCost[productId], productId))
    
    filterProducts = sorted(filterProducts)
    Max = 2.2

    productsOrder = []
    for product in filterProducts:
        productName = Product.objects.get(id = product[2]).name
        print(productName, product[0], product[1])
        if product[0] >= Max or product[1] >= Max:
            continue
        productsOrder.append(Product.objects.get(id = product[2]))



    return render(request, 'index.html', {'products' : productsOrder})




   
