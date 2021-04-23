from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Item, Order, OrderItem
# Create your views here.



def home(request):
	context = {
		'items': Item.objects.all()
	}
	return render(request, 'webshop/home.html', context)



class PostCreateView(LoginRequiredMixin, CreateView):
	model = Item
	fields = ['name','price','category','description','photo','author']
	
	def form_valid(self, form):
		user = self.request.user
		return super().form_valid(form)
	

	def img_url(self):
		if self.photo and hasattr(self.photo,'url'):
			return self.photo.url
		

	
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Item
	fields = ['name','price','category','description','photo','author']
	

	#def form_valid(self, form):
	#	form.instance.photo.url = './default.jpg'
	#	return super().form_valid(form)

	def form_valid(self, form):
		user = self.request.user
		return super().form_valid(form)

	def test_func(self):
		item = self.get_object()
		if self.request.user == item.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Item
	success_url = '/webShop/'
	def test_func(self):
		item = self.get_object()
		if self.request.user == item.author:
			return True
		return False


def about(request):
	return render(request, 'webshop/about.html', {'title': 'about'})


##not in use right now
def item_list(request):
	items_list = Item.objects.all()
	page = request.GET.get('page')
	paginator = Paginator(items_list,5)
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)
	return render(request, 'webshop/item_list.html', {'page': page, 'items': items})


class HomeView(ListView):
	model = Item
	template_name = 'webshop/home-page.html' #app>/<model>_<viewtype>.html
	context_object_name = 'items'
	# ordering = ['-created_at']
	paginate_by = 10

class ItemDetailView(DetailView):
	model = Item
	template_name = 'webshop/product.html'


def add_to_cart(request, pk):
	#item = get_object_or_404(Item, slug=pk)
	
	item = Item.objects.get(id = pk)
	slug = item.slug
	order_item, created = OrderItem.objects.get_or_create(
		item=item,
		user=request.user,
		ordered=False
		)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		#check if the order is in the order
		if order.items.filter(item__slug=item.slug).exists():
			order_item.quantity +=1
			order_item.save()
			messages.info(request,"This item quantity was updated.")
			return redirect('product', pk=slug)
		else:
			messages.info(request,"This item was added to your cart.")
			order.items.add(order_item)
			return redirect('product', pk=slug)
	else:
		ordered_date = timezone.now()
		order = Order.objects.create(user=request.user, ordered_date=ordered_date)
		order.items.add(order_item)
		messages.info(request,"This item was added to your cart.")
		return redirect('product', pk=slug)
	
	#return render(request, '/webshop/product/', order_item)


def remove_from_cart(request, pk):
	item = Item.objects.get(id = pk)
	slug = item.slug
	order_qs = Order.objects.filter(
		user=request.user,
		ordered=False
	)
	if order_qs.exists():
		order = order_qs[0]
		#check if the order is in the order
		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(
				item=item,
				user=request.user,
				ordered=False
			)[0]
			order.items.remove(order_item)
			order_item.delete()
			messages.info(request,"This item was removed to your cart.")
			return redirect('product', pk=slug)
		else:
			messages.info(request,"This item was not in your cart.")
			return redirect('product', pk=slug)
	else:
		messages.info(request,"You do not have an active order.")
		return redirect('product', pk=slug)
	