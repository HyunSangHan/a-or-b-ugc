from django.shortcuts import render

history = []

def home(request):
    return render(request, 'feedpage/home.html')

def about(request):
    return render(request, 'feedpage/about.html')

def result(request):
    new_text = request.GET["fulltext"]
    words = new_text.split()
    word_dic = {}

    if words !=[]:
        history.append(new_text)

    unique = 0
    for word in words:
        if word in word_dic:
            word_dic[word] += 1
        else:
            word_dic[word] = 1
            unique += 1

    return render(request, 'feedpage/result.html',{'fulltext': new_text, 'count': len(words), 'dictionary': word_dic.items(), 'unique': unique, 'history': history})