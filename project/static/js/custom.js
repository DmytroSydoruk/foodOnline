var geocoder = new maptiler.Geocoder({
    input: 'id_address',
    key: 'sgRLtHO0dUL7548L8tiZ'
});

geocoder.on('select', function(item) {
    console.log('Selected', item);
    // fetch(item)
    //     .then( res => res.json())
    //     .then( data => {
    //         console.log(data)
    // });
});

