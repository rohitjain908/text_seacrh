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
    x = 2
    y = 2
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
                                        distance(str1[i - 1], str2[j - 1]) + string_matrix[i-1][j-1])    # replace operation
    return string_matrix[a][b]


def ok(totalCost, costBetweenCode, costBetweenWords):
    if totalCost < 17 and costBetweenCode < 3 and costBetweenWords < 15:
        return True
    return False


def search(request, inputText):
    filterProductsID = set()
    splitWords = splitString(inputText)

    for word in splitWords:
        wordCode = soundexCode(word)

        for valueObject in DictKeyValue.objects.all():
            objectCode = soundexCode(valueObject.value)
            keyObject =  valueObject.container
            type = keyObject.type.lower()
            costBetweenWords = editDistanceWithDifferentCost(word, valueObject.value)
            costBetweenCode = editDistance(wordCode, objectCode)


            
            totalCost = costBetweenCode + costBetweenWords
            if type == 'name':
                if ok(totalCost, costBetweenCode, costBetweenWords):
                    products = Product.objects.all().filter(name = keyObject.name)
                    for product in products:
                        filterProductsID.add(product.id)

            elif type == 'category':
                if ok(totalCost, costBetweenCode, costBetweenWords):
                    products = Product.objects.all().filter(category = keyObject.name)
                    for product in products:
                        filterProductsID.add(product.id)

            elif type == 'brand':
                if ok(totalCost, costBetweenCode, costBetweenWords):
                    products = Product.objects.all().filter(brand = keyObject.name)
                    for product in products:
                        filterProductsID.add(product.id)

            elif type == 'subcategory':
                if ok(totalCost, costBetweenCode, costBetweenWords):
                    products = Product.objects.all().filter(subCategory = keyObject.name)
                    for product in products:
                        filterProductsID.add(product.id)

            # if wordCode == objectCode:
            #     print(valueObject.value)

    filterProducts = []
    for id in filterProductsID:
        filterProducts.append(Product.objects.get(id = id))



    return render(request, 'index.html', {'products' : filterProducts})




   









   