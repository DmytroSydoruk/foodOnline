$(document).ready(function(){

    // accept oredered food
    $(".accept-order").on('click', function(e){
        e.preventDefault();
        url = $(this).attr('data-url');
        ordered_food_id = $(this).attr('data-id')
        
        $.ajax({
            type:  'GET',
            data: {
                ordered_food_id: ordered_food_id
            },
            url: url,
            success: function(response){
                console.log(response)
                document.getElementById('status-'+ordered_food_id).innerHTML = 'Accepted'
                document.getElementById('statusButtons-'+ordered_food_id).remove()
            },
        });
    });

    // decline ordered product
    $(".decline-order").on('click', function(e){
        e.preventDefault();
        url = $(this).attr('data-url');
        ordered_food_id = $(this).attr('data-id')
        
        $.ajax({
            type:  'GET',
            data: {
                ordered_food_id: ordered_food_id
            },
            url: url,
            success: function(response){
                console.log(response)
                document.getElementById('status-'+ordered_food_id).innerHTML = 'Cancelled'
                document.getElementById('statusButtons-'+ordered_food_id).remove()
            },
        });
    });

    // change order status
    $(".select-status").change(function(){
        url = $(this).attr('data-url');
        order = $(this).attr('data-id');
        $('select option:selected').each(function(){
            $.ajax({
                type:"GET",
                data:{
                    order_id: order,
                    order_status: $(this).text(),
                },
                url: url,
                success: function(response){
                    
                },

            });
        });
    });

    // filter orders by status
    $(".select-filter-order").change(function(){
        let filter = $(this).val();
        filterOrders(filter);
        
        });
    

    function filterOrders(value){
        let list = $('.order-heading-titles-order');
        $(list).hide();
        if(value == 'All'){
            $('.order-heading-titles-order').each(function(i){
                $(this).show();
            });
        }else{
            $(".order-heading-titles-order[data-id*="+value+"]").each(function(i){
                $(this).show();
            })
        };
    };


});