
$(document).ready(function(){
    // let geocoder = new maptiler.Geocoder({
    //     input: 'id_address',
    //     key: 'sgRLtHO0dUL7548L8tiZ'
    // });
    // // address line    
    // geocoder.on('select', function(response) {
    //     console.log('Selected', response);
    //     $('#id_country').html(response.id)
    //     console.log(response.id);
    // });


    function DeliveryCredentials() {
        let checkBox = document.getElementById("chk_reciver");
        let credentials = document.getElementById("custom_reciver");
        if (checkBox.checked == false){
            credentials.style.display = "block";
        } else {
            credentials.style.display = "none";
        };
      };
      $('#chk_reciver').on('change', function(e){
            e.preventDefault();
            DeliveryCredentials();
      });

    // add to cart
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('cart-id');

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

                    // total price
                    applyCartAmount(response.cart_amount['total']);

                    changeItemTotal(cart_id, response.price, response.qty)
                }
            }
        })
    });

    // decrease cart
    $('.decrease_cart').on('click',function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        cart_id = $(this).attr('cart-id');
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
                    removeCartItem(response.qty,cart_id);
                    applyCartAmount(response.cart_amount['total'])
                    changeItemTotal(cart_id, response.price, response.qty)
                }
            }
        })
    });

    // delete cart
    $('.delete_cart').on('click',function(e){
        e.preventDefault();
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)
                if(response.status == "Failed"){
                    swal({
                        title: response.message,
                        text: "",
                        icon: "error",
                      })
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    removeCartItem(0,cart_id);
                    applyCartAmount(response.cart_amount['total'])
                    
                }
            }
        })
    });

    // place cart item quantity on load
    $('.item_qty').each(function(){
        let the_id = $(this).attr('id')
        let qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    });
    // delete cart element if qty <= 0
    function removeCartItem(cartItemQty, cart_id){
        if(window.location.pathname == '/cart/'){
            if (cartItemQty <= 0){
            document.getElementById("cart-item-"+cart_id).remove();
            swal({
                title: "Success",
                text: "Cart item has been deleted",
                icon: "success",
              })
              checkEmptyCart();
        }
    }};

    function checkEmptyCart(){
        let cart_counter = document.getElementById('cart_counter').innerHTML
        if (cart_counter == 0){
            document.getElementById('empty-cart').style.display = "block";
            document.getElementById('confirm-order').style.display = "none";
        }

    }

    // apply cart amounts
    function applyCartAmount(total){
        if(window.location.pathname == '/cart/'){
            $('#total').html(total)
        }
    }

    // change item total price
    function changeItemTotal(cart_id , price, qty){
        if(window.location.pathname == '/cart/'){
            let result = Math.round(price * qty).toFixed(2);
            $('#cart-amount-price-'+cart_id).html(result)
        }
    }

    $('.add_hour').on('click',function(e){
        e.preventDefault();
        let day = document.getElementById('id_day').value
        let from_hour = document.getElementById('id_from_hour').value
        let to_hour = document.getElementById('id_to_hour').value
        let is_closed = document.getElementById('id_is_closed').checked
        let csrf = $('input[name=csrfmiddlewaretoken]').val()
        if (is_closed){
            is_closed = "True"
            condition = "day != ''"
        }else{
            is_closed = "False"
            condition = "day != '' && from_hour != '' && to_hour != ''"
        }
        
        
        if(eval(condition)){

        }else{
            alert("Please fill all fields") 
        }
        
        // console.log(day, from_hour, to_hour, is_closed ,csrf)
    });



});

