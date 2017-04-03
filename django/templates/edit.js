
function adddropify() {
    var id = 'medias-' + new Date().getTime();
    $('#medias .row')[0].insertAdjacentHTML(
        'beforeEnd',
        '<div class="col l3 m4 s12"><input type="file" multi=true id="'+ id +'" name="media-' + id + '" class="dropify" data-allowed-file-extensions="jpg jpeg" accept=".jpg,.jpeg" capture="true" data-max-file-size-preview="3M" /></div>'
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

{% for media in product.medias.all %}

adddropify();

{% empty %}

adddropify();

{% endfor %}

function refreshcarousel() {
    $('.carousel').remove();
    document.getElementById('-image').insertAdjacentHTML(
        'beforeEnd',
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
            'beforeEnd',
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
    for (var i = 0; i < demos.length; i++) {
        demos[i].innerHTML = document.getElementById(name).value;
    }
}

function changetype() {
    var type = document.getElementById('type');
    $('#capacities')[type.value === 'product' ? 'hide' : 'show']();
    $('#name')[0].placeholder = (type.value === 'product') ? 'Appareil photo Nikon D80' : 'Garage voiture et moto';
    $('#shortdescription')[0].placeholder = (type.value === 'product') ? '10 millions de pixels, carte mémoire 2 Go' : '10 places en plein centre ville';
}

changetype();

var lowcategories = {
    //{% for lowcategory in lowcategories %}
    '{{ lowcategory.name }}': '{{ lowcategory.media.media.path.url }}',
    //{% endfor %}
};

function newentryset(parentid, entryid, additional) {
    if (entryid === undefined) {
        entryid = new Date().getTime();
    }
    var html = '<table class="bordered striped highlight centered" id="entry-'+ entryid + '"><thead><tr>';
    html += '<td>Type</td><td>Montant</td>';
    html += '<td>' + (additional ? ('<a onclick="newentryset(\'' + parentid + '\', undefined, true);" class="btn-floating blue" ><i class="material-icons">add</i></a>') : '') + '</td>';
    html += '</tr></thead>';
    html += '<tbody id="entry-content-' + new Date().getTime() + '"></tbody></table>';
    document.getElementById(parentid).insertAdjacentHTML(
        'beforeEnd',
        html
    );
}

function newEntry(entrysetid, entryid, type, amount) {
    if (entryid === undefined) {
        entryid = new Date().getTime();
    }
    var html = '<tr id="">';
    html += '<td><input type="text" name="entry-type-' + entryid + '" value="' + type +'" placeholder="€, voiture, ..." /></td>';
    html += '<td><input type="number" name="entry-amount-' + entryid + '" value="' + amount + '" placeholder="10" /></td>';
    html += '<td><a onclick="removeEntry(this);" class="btn-floating red"><i class="material-icons">remove</i></a></td></tr>';
    document.getElementById(entryid)
}

function removeEntry(elt) {
    var body = elt.parentNode.parentNode.parentNode;
    elt.remove();
    if (body.childElementCount === 0) {
        newEntry(body.parentNode.id);
    }
}

var lastcapacity;

function updatecapacity(elt) {
    var capacity = elt.parentNode.parentNode;
    if (elt.value === '') {
        var empty = false;
        elt.parentNode.parentNode.children.forEach({
            function(child) {
                empty = (child.children[0] === '');
            }
        });
        if (empty && lastcapacity !== capacity) {
            capacity.remove();
        }
    } else if (capacity === lastcapacity) {
        addcapacity();
    }
}

function deletecapacity(elt) {
    var capacity = elt.parentNode.parentNode;
    if (capacity !== lastcapacity) {
        capacity.remove();
    }
}

function addcapacity(name, amount) {
    name = name ? name : '';
    amount = amount ? amount : 10;
    var id = 'capacity-' + (name ? name : new Date().getTime().toString());
    var table = $('#capacities tbody')[0];
    var html = '<tr id="' + id + '">';
    html += '<td>';
    html += '<input onchange="updatecapacity(this);" type="number" value="' + amount + '" name="capacity-amount-' + id + '" />';
    html += '</td>';
    html += '<td>';
    html += '<input placeholder="voiture" onchange="updatecapacity(this);" type="text" value="' + name + '" name="capacity-name-' + id + '" class="autocomplete" />';
    html += '</td>';
    html += '<td>';
    html += '<a class="close btn-floating" onclick="deletecapacity(this);"><i class="material-icons red">close</i></a>';
    html += '</td>';
    html += '</tr>';
    table.insertAdjacentHTML('beforeEnd', html);
    $('.' + id).autocomplete(
    {
        data: lowcategories,
        minLength: 1
    });
    lastcapacity = document.getElementById(id);
}

$( document ).ready(function(){
    {% for capacity in product.capacities %}
    addcapacity('{{ capacity.name }}', '{{ capacity.amount');
    {% empty %}
    addcapacity();
    {% endfor %}
});

var lastcondition = {};

function updatecondition(kind, elt) {
    var condition = elt.parentNode.parentNode;
    if (elt.value === '') {
        var empty = false;
        elt.parentNode.parentNode.children.forEach({
            function(child) {
                empty = (child.children[0] === '');
            }
        });
        if (empty && lastcondition !== condition) {
            condition.remove();
        }
    } else if (condition === lastcondition) {
        addcondition(kind);
    }
}

function deletecondition(kind, elt) {
    var condition = elt.parentNode.parentNode;
    if (condition !== lastcondition[kind]) {
        condition.remove();
    }
}

function addcondition(kind, name, amount) {
    name = name ? name : '';
    amount = amount ? amount : 0;
    var id = kind + '-' + (name ? name : new Date().getTime().toString());
    var table = $('#'+ kind + 's tbody')[0];
    var html = '<tr id="' + id + '">';
    html += '<td>';
    html += '<input onchange="updatecondition(\'' + kind + '\', this);" type="number" value="' + amount + '" name="' + kind + '-amount-' + id + '" />';
    html += '</td>';
    html += '<td>';
    html += '<input placeholder="carottes" onchange="updatecondition(\'' + kind + '\', this);" type="text" value="' + name + '" name="' + kind + '-name-' + id + '" class="autocomplete" />';
    html += '</td>';
    html += '<td>';
    html += '<a class="close btn-floating" onclick="deletecondition(\'' + kind + '\', this);"><i class="material-icons red">close</i></a>';
    html += '</td>';
    html += '</tr>';
    table.insertAdjacentHTML('beforeEnd', html);
    $('.' + id).autocomplete(
    {
        data: lowcategories,
        minLength: 1
    });
    lastcondition[kind] = document.getElementById(id);
}

function addconditionset() {}

$( document ).ready(function() {
    {% for give in product.gives.all %}
    {% for conditionset in give.conditions %}
    {% for condition in conditionset.conditions.all %}
    addcondition('give', '{{ conditionset.name }}', '{{ condition.type }}', '{{ condition.amount }}', '{{ condition.duedate }}');
    {% endfor %}
    {% endfor %}
    {% empty %}
    addconditionset('give');
    {% endfor %}

    {% for share in product.gives.all %}
    {% for conditionset in share.conditions %}
    {% for condition in conditionset.days.all %}
    addcondition('share', '{{ conditionset.name }}', '{{ condition.type }}', '{{ condition.amount }}', '{{ condition.duedate }}');
    {% endfor %}
    {% for condition in conditionset.weeks.all %}
    addcondition('share', '{{ conditionset.name }}', '{{ condition.type }}', '{{ condition.amount }}', '{{ condition.duedate }}');
    {% endfor %}
    {% for condition in conditionset.weekends.all %}
    addcondition('share', '{{ conditionset.name }}', '{{ condition.type }}', '{{ condition.amount }}', '{{ condition.duedate }}');
    {% endfor %}
    {% for condition in conditionset.months.all %}
    addcondition('share', '{{ conditionset.name }}', '{{ condition.type }}', '{{ condition.amount }}', '{{ condition.duedate }}');
    {% endfor %}
    {% for condition in conditionset.years.all %}
    addcondition('share', '{{ conditionset.name }}', '{{ condition.type }}', '{{ condition.amount }}', '{{ condition.duedate }}');
    {% endfor %}
    {% endfor %}
    {% empty %}
    addconditionset('share');
    {% endfor %}
});
/*
function addset(set, single) {
    var html = '<table class="bordered striped highlight centered responsiv-table>';
    html += '<thead>';
    html += '<tr>';
    html += '<td>Montant</td>';
    html += '<td>type</td>';
    var thirdcolumn = '';
    if (single) {
        thirdcolumn = '<a onclick="addset(\'' + set + '\', true);" class="btn-floating red"><i class="material-icons">add</i></a>';
    }
    html += '<td>' + thirdcolumn + '</td>';
    html += '</tr></thead>';
    html ++ '<tbody></tbody>';
    html += '</table>'
    $(set).insertAdjacentHTML('beforeEnd', html);
}*/

{% include 'categories.js' %}

{% include 'map.js' %}
