from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator

# post의 상세 내용을 보여줌
def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post.html', {'post':post})

# postlist를 보여줌 / pagination 구현 해야함
def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 6) # 한 페이지 당 6개씩 보여줌
    page = int(request.GET.get('p', 1)) # 없으면 1로 지정
    contacts = paginator.get_page(page)
    return render(request, 'index.html', {'posts':posts, 'contacts':contacts})


# post만드는 html
def create(request):
    return render(request, 'create.html')

# post만드는 메소드
def postcreate(request):
    if request.method == 'POST': # POST 방식으로 요청이 들어올 때
        form = PostForm(request.POST) # 입력된 내용을 form 변수에 저장
        if form.is_valid(): # form이 유효하면(models.py에서 정의한 필드에 적합하면)
            post = form.save(commit=False) # form데이터를 가져온다.
            
            post.save() # form 데이터를 db에 저장한다
            return redirect('index')
        else: 
            return redirect('index')
    else: # GET 방식으로 요청이 들어올 때
        form = PostForm()
        return render(request, 'create.html', {'form': form})

# post 수정하는 html
def update(request):
    return render(request,'update.html')

# post 수정하는 메소드
def postupdate(request, post_id): # post_id로 수정하고자 하는 post 객체를 get
    post = get_object_or_404(Post, pk=post_id) 
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post', post_id=post.pk)
        else:
            return redirect('index')
    else:
        form = PostForm(instance=post)
        return render(request, 'update.html', {'form':form})

# post를 삭제하는 메소드
def postdelete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete() # Post db에서 post객체 삭제
    return redirect('index')