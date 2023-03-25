from django.shortcuts import render
from .models import Post,Comment,About,OurTeam,Contact_details
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm,SearchForm,Contactform
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector

def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
       tag = get_object_or_404(Tag, slug=tag_slug)
       post_list = post_list.filter(tags__in=[tag])

    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
            posts = paginator.page(page_number)
            
    except PageNotAnInteger:
           # If page_number is not an integer deliver the first page
           posts = paginator.page(1)
    except EmptyPage:
            # If page_number is out of range deliver last page of results
            posts = paginator.page(paginator.num_pages)
    return render(request,
                 'blog/post/list.html',
                 {'posts': posts,
                  'tag': tag})
    
    
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request,
                'blog/post/detail.html',
                {'post': post,
                'comments': comments,
                'form': form,
                'similar_posts': similar_posts})

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                                                  post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'junioralexio607@gmail.com',
            [cd['to']])
            sent = True
            # ... send email
            # Save the email to the database
            form.save()
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                            'form': form,
                            'sent': sent})
    
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request, 'blog/post/comment.html',
                            {'post': post,
                            'form': form,
                            'comment': comment})  
    
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title', 'body'),).filter(search=query)
            return render(request,
                         'blog/post/search.html',
                         {'form': form,
                         'query': query,
                         'results': results})
 
def contact_us(request):
    Contact_info = Contact_details.objects.all()
    if request.method == 'POST':
        # Form was submitted
        form = Contactform(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            subject = f"{cd['name']}  with email {cd['email']}  Sent you a message  from  topDevBlog:{cd['subject']} "
            message = f"Message: {cd['message']}"
            send_mail(subject, message, 'junioralexio607@gmail.com',
            ['junioralexio607@gmail.com'])
            sent = True
            # ... send email
            return render(request, 'blog/post/contact.html', 
                  {'Contact_info': Contact_info,
                   'form': form,
                   'sent': sent})
        
    else:
        form = Contactform()
    return render(request, 'blog/post/contact.html', 
                  {'Contact_info': Contact_info,
                   'form': form})

def about_us(request):
    about = About.objects.all()
    ourteam = OurTeam.objects.all()
    
    return render(request,
                'blog/post/about.html',
                {'about': about,
                'ourteam': ourteam,
                })
    