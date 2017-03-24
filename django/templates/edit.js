$('')

function adddropify() {
    var id = 'medias-' + new Date().getTime();
    $('#medias .row')[0].insertAdjacentHTML(
        'beforeend',
        '<div class="col m4 s6"><input type="file" multi=true id="'+ id +'" name="media-' + id + '" class="dropify" data-allowed-file-extensions="jpg jpeg" accept=".jpg,.jpeg" capture="true" data-max-file-size-preview="3M" /></div>'
        );

    var drEvent = $('#'+id).dropify({
        messages: {
            'default': 'Glissez-déposez un fichier ici ou cliquez',
            'replace': 'Glissez-déposez un fichier ici ou cliquez pour remplacer',
            'remove':  'Supprimer',
            'error':   'Ooops, une erreur est arrivée.'
        },
        error: {
            'fileSize': 'La taille du fichier doit être inférieur à {{ value }}.',
            'minWidth': 'La largeur de l\'image doit être supérieure à {{ value }}px.',
            'maxWidth': 'La largeur de l\'image doit être inférieure à {{ value }}px.',
            'minHeight': 'La hauteur de l\'image doit être supérieure à {{ value }}px.',
            'maxHeight': 'La hauteur de l\'image doit être inférieure à {{ value }}px.',
            'imageFormat': 'Le format de l\'image doit être de type {{ value }}.'
        }
    });

    drEvent.on('dropify.afterClear', function(event, element) {
        $('#carousel-' + event.target.id).remove();
        event.target.parentNode.parentNode.remove();
    });

    drEvent.on('change', function(event) {
        if (event.target.hasFile === undefined) {
            adddropify();
            setTimeout(function() {
                refreshcarousel();
                event.target.hasFile = true;
            }, 1000);
        }
    });
}

function refreshcarousel() {
    $('.carousel').remove();
    document.getElementById('-image').insertAdjacentHTML(
        'beforeend',
        '<div class="carousel"></div>'
        );
    var carousel = $('.carousel')[0];
    var ids_files = [];
    var dropifies = $('.dropify');
    for(var i=0; i<(dropifies.length - 1); i++) {
        var dropify = dropifies[i];
        var img = $(dropify.parentNode).find('img');
        if (img.length === 0) {
            continue;
        }
        var src = img[0].src;
        if (src !== undefined) {
            ids_files.push([dropify.id, src]);
        }
    }
    ids_files.forEach(function(id_file) {
        carousel.insertAdjacentHTML(
            'beforeend',
            '<a id="carousel-' + id_file[0] + '" class="carousel-item" data-caption="' + document.getElementById('name').value + '" href="#one!"><img class="responsive-img" src="' + id_file[1] + '" /></a>'
            );
    });
    $('.carousel').carousel(
        {
            //shift: 200,
            //fullWidth: true,
            //indicators: true,
            //noWrap: true
        });
    $('.materialboxed').materialbox();
}

function updateProperty(name) {
    var demos = $('.' + name);
    for (var i = 0; i<demos.length; i++) {
        demos[i].innerHTML = document.getElementById(name).value;
    }
}

{% for media in product.medias.all %}

adddropify();

{% empty %}

adddropify();

{% endfor %}
