from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
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


class CheckoutView(DetailView):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")

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
	success_url = '/webshop/'
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


class OrderSummaryView(LoginRequiredMixin, DetailView):
	def get(self, *args,**kwargs):
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			context = {
				'object': order
			}

			return render(self.request, 'webshop/order-summary.html', context)

          
		except ObjectDoesNotExist:
			messages.warning(self.request,"You do not have an active order.")
			return redirect('webshop/items_list/')
	


class ItemDetailView(DetailView):
	model = Item
	template_name = 'webshop/product.html'

@login_required
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
			return redirect('order-summary')
		else:
			messages.info(request,"This item was added to your cart.")
			order.items.add(order_item)
			return redirect('order-summary')
	else:
		ordered_date = timezone.now()
		order = Order.objects.create(user=request.user, ordered_date=ordered_date)
		order.items.add(order_item)
		messages.info(request,"This item was added to your cart.")
		return redirect('order-summary')
	
	#return render(request, '/webshop/product/', order_item)

@login_required
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
			return redirect('order-summary')
		else:
			messages.info(request,"This item was not in your cart.")
			return redirect('product', pk=slug)
	else:
		messages.info(request,"You do not have an active order.")
		return redirect('product', pk=slug)
	

@login_required
def remove_single_from_cart(request, pk):
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
			if order_item.quantity > 1:
				order_item.quantity -=1
				order_item.save()
			else:
				order.items.remove(order_item)
			
			messages.info(request,"This item qquantity was updated.")
			return redirect('order-summary')
		else:
			messages.info(request,"This item was not in your cart.")
			return redirect('product', pk=slug)
	else:
		messages.info(request,"You do not have an active order.")
		return redirect('product', pk=slug)
	