from django.shortcuts import render, get_object_or_404
from .models import Post, comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, commentForm, SearchForm
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector,SearchRank, SearchQuery

def post_list(request):
    object_list= Post.published.all()
    paginator =Paginator(object_list, 3) #3 post per each page
    page = request.GET.get('page')
    try:
        posts =paginator.page(page)
    except PageNotAnInteger:
        #if page is not an interger deliver the first page
        posts=paginator.page(1)
    except EmptyPage:
        #if the page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                    'bitcoin/post/list.html',
                    {'page':page,
                        'posts': posts})     

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                    status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
    #list of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment =None
    comment_form = commentForm()
    if request.method=='POST':
        #comment was posted
        comment_form = commentForm(data=request.POST)
        if comment_form.is_valid():
            #create comment object but dont save it to the database yet
            new_comment=comment_form.save(commit=False)
            #assign the current post to the comment
            new_comment.post=post
            #save the commet to the database
            new_comment.save()
        else:
            comment_form=commentForm()
    return render(request,
                        'bitcoin/post/detail.html',
                        {'post': post,
                        'comments':comments,
                        'new_comment': new_comment,'comment_form':comment_form})  

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent =  False

    if request.method =="POST":
        #form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #form passed validation
            cd =form.cleaned_data
            #...send email
            post_url = request.build_absolute_uri(
                                    post.get_absolute_url())
            subject = f"{cd['name']} recommends you read "f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'kevinisaackareithi@gmail.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'bitcoin/post/share.html',{'post':post,'form':form, 'sent':sent})

def post_search(request):
    form = SearchForm()
    query = None
    results =[]
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title','body')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                search = search_vector,
                rank = SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')
    return render(request,
                    'bitcoin/post/search.html',
                    {'form':form,
                    'query':query,
                    'results':results
                    }
    )
