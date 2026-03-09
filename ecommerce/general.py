from .models import Category

def global_data(request):
    data={
        'category': Category.objects.filter(parent=None)
    }
    return data