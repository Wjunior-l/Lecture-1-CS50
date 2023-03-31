from django.shortcuts import redirect, render
from . import util
import markdown, random
from django import forms



class NewPageForm(forms.Form):
        title = forms.CharField(
        label='Title', max_length=100, min_length=1, 
        widget=forms.TextInput(attrs={'class': 'my-title-area', 'placeholder': 'Enter a title:'}))
        
        content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'my-text-area', 'placeholder': 'Enter the content:'}),
        label ='Content', min_length=1,
        )
        
class EditPageForm(forms.Form):
        title = forms.CharField(
        label='Title', max_length=100, min_length=1,
        widget=forms.TextInput(attrs={'placeholder': 'Enter a title:'}))

        content = forms.CharField(
        label='Content', min_length=1,
        widget=forms.Textarea(attrs={'class': 'my-text-area', 'placeholder': 'Enter the content:'}),
        )


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def md_to_html(title):
    content = util.get_entry(title)
    markdownder = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdownder.convert(content)
    
def wiki_entry(request, title):
    html_topic = md_to_html(title)
    if html_topic == None:
       return render(request, "encyclopedia/error.html", {"error_message": "We could not find the above page on our servers."})
    else:
        return render(request, "encyclopedia/entry.html", {
        "content": html_topic, 
         "title": title
        } )



def search_(request):
    if request.method == "GET":
        search = request.GET['q']
        html_topic = md_to_html(search)
        if html_topic is not None:
            return render(request, "encyclopedia/entry.html", {
                "content": html_topic, 
                "title": search
            })
        else:
            allEntries = util.list_entries()
            recommend = []
            for entry in allEntries:
                if search.lower() in entry.lower():
                    recommend.append(entry)
            if len(recommend) == 0:
                
                
                return render(request, "encyclopedia/search_error.html", {
                    
                    "new_page_link": search
                })
                
            else:
                return render(request, "encyclopedia/search.html", {
                    "recommend": recommend
                })


def newpage(request):
    
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            content_with_title = f'# {title}\n\n{content}'
            if title in util.list_entries():
                 return render(request, "encyclopedia/error.html", {
                    "error_message": f"An entry with the title '{title}' already exists.",
                    "title_link": title
                })
            util.save_entry(title, content_with_title)
            return render(request, "encyclopedia/entry.html", {
                "content": md_to_html(title), 
                "title": title

            })
    else:
        form = NewPageForm()
    return render(request, 'encyclopedia/newpage.html', {'form': form})
               
    
def editpage(request, title):
    if request.method == 'POST':
        form = EditPageForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data['content']
            util.save_entry(title, new_content)
            return redirect('wiki:wiki_entry', title=title)
    else:
        content = util.get_entry(title)
        if content is None:
            return render(request, "encyclopedia/error.html", {"error_message": "We could not find the above page on our servers."})
        else:
            form = EditPageForm(initial={'title': title, 'content': content})
        return render(request, 'encyclopedia/editpage.html', {'form': form, 'title': title})

def randompage(request):
    allEntries = util.list_entries()
    randomEntry = random.choice(allEntries)
    return redirect('wiki:wiki_entry', title=randomEntry)
