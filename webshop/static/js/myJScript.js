$(document).ready(function(){

  $('.remove_single_item_from_cart').click(function(){
	id = $(this).attr('productid')
	//alert(product_id)
	
	var str0 = "http://localhost:8000/webShop/remove_single_item_from_cart/"
	//var str1 = "remove_single_item_from_cart/";
	var str2 = id;
	var res = str0.concat(str2);


    $.ajax({
        type: 'GET',
        url: res,
        success: function(response){
	    	$('.item_quantity').html(response);

        }
    })
   })

  $('.add_to_cart').click(function(){
	id = $(this).attr('productid')
	//alert(product_id)
	
	var str0 = "http://localhost:8000/webShop/add_to_cart/"
	//var str1 = "remove_single_item_from_cart/";
	var str2 = id;
	var res = str0.concat(str2);

    $.ajax({
        type: 'GET',
        url: res,
        success: function(response){
        	$('.item_quantity').html(response);
        }
    })
   })


  $('.remove_from_cart').click(function(){
	id = $(this).attr('productid')
	//alert(product_id)
	
	var str0 = "http://localhost:8000/webShop/remove_from_cart/"
		
	var str2 = id;
	var res = str0.concat(str2);

    $.ajax({
        type: 'GET',
        url: res,
        success: function(response){
        	$('.item_quantity').html(response);

        }
    })
   })
});

