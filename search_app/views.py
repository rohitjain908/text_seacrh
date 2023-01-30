from django.shortcuts import render
from .models import Product

# Create your views here.


def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products' : products})


def editDistance(str1, str2):
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


def search(request, inputText):
    #print(inputText)
    
    ##compare with productName
    filterProducts = []

    threshold = 4

    products = Product.objects.all()
    for product in products:
        #compare with name
        distanceBetweenName = editDistance(inputText, product.name)

        #compare with brand
        distanceBetweenBrand = editDistance(inputText, product.brand)

        #compare with category
        distanceBetweenCategory = editDistance(inputText, product.category)

        #compare with subcategory
        distanceBetweenSubCategory = editDistance(inputText, product.subCategory)

        if distanceBetweenName < threshold or \
        distanceBetweenBrand < threshold or \
        distanceBetweenCategory < threshold or \
        distanceBetweenSubCategory < threshold:

            filterProducts.append(product)


    return render(request, 'index.html', {'products' : filterProducts})




   