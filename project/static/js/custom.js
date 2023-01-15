var geocoder = new maptiler.Geocoder({
    input: 'id_address',
    key: 'sgRLtHO0dUL7548L8tiZ'
});

geocoder.on('select', function(item) {
    console.log('Selected', item);
});

$(document).ready(function(){
    // add to cart
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == "login_required"){
                    swal({
                        title: response.message,
                        text: "You need to login first",
                        icon: "info",
                      }).then(function(){
                        window.location = '/login'
                      });
                }
                else if(response.status == "Failed"){
                    swal({
                        title: response.message,
                        text: "",
                        icon: "error",
                      })
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)
                }
            }
        })
    })
    // decrease cart
    $('.decrease_cart').on('click',function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){

                if(response.status == "login_required"){
                    swal({
                        title: response.message,
                        text: "You need to login first",
                        icon: "info",
                      }).then(function(){
                        window.location = '/login'
                      });
                }
                else if(response.status == "Failed"){
                    swal({
                        title: response.message,
                        text: "",
                        icon: "error",
                      })
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)
                }
                
            }
        })
    })


    // place cart item quantity on load
    $('.item_qty').each(function(){
        let the_id = $(this).attr('id')
        let qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })
});

