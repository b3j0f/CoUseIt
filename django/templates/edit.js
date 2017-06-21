{% load i18n %}

$('.add').hide();
$('.update').hide();
{% if common %}
$('.update').show();
{% else %}
$('.add').show();
{% endif %}

var action = '{{ action }}';

var actions = {
    give: {
        translation: '{% trans 'give' %}',
    },
    share: {
        translation: '{% trans 'share' %}',
    },
    stock: {
        translation: '{% trans 'stock' %}',
    }
}

for(var _action in actions) {
    $('.' + _action).hide();
}
$('.' + action).show();

var types = {
    product: {
        translation: '{% trans 'product' %}',
        name: '{% trans 'Picture camera Nikon D80' %}',
        shortdescription: '',
        description: ''
    },
    stock: {
        translation: '{% trans 'stock' %}',
        name: '',
        shortdescription: '',
        description: ''
    },
    service: {
        translation: '{% trans 'service' %}',
        name: '',
        shortdescription: '',
        description: ''
    }
};

var type = '{{ commontype }}';
for(var _type in types) {
    $('.' + _type).hide();
}
$('.' + type).show();

var common = {
    {% include 'common.js' with common=common %}
};

var supplyings = {
    {% for supply in supplyings %}
    '{{ supply.id }}'
    {% endfor %}
}

var common = {
    name: '{{ common.name }}',
    shortdescription: '{{ common.shortdescription }}',
    description: '{{ common.description }}',
    created: '{{ common.created }}',
    owners: [{% for owner in common.owners.all %}'{{ owner.id }}', {% endfor %}],
    suppliers: [{% for supplyer in common.suppliers.all %}'{{ supplyer.id }}', {% endfor %}],
    users: [{% for user in common.users.all %}'{{ user.id }}', {% endfor %}],
    category: '{{ common.category }}',
    professional: {% if common.professional %}true{% else %}false{% endif %}
};

var owners_material_chip = {
    placeholder: '{% trans '+pseudo' %}',
    secondaryPlaceholder: '{% trans '+pseudo' %}',
    data: [],
    autocompleteOptions: {
        data: {
            {% for account in accounts %}
            '{{ account.user.name }}': '{{ account.avatar.furl }}'
            {% endfor %}
        },
        limit: Infinity,
        minLength: 1
    }
};

var supplyers_material_chip = {
    placeholder: '{% trans '+pseudo' %}',
    secondaryPlaceholder: '{% trans '+pseudo' %}',
    data: [],
    autocompleteOptions: {
        data: {
            {% for account in accounts %}
            '{{ account.user.name }}': '{{ account.avatar.furl }}'
            {% endfor %}
        },
        limit: Infinity,
        minLength: 1
    },
    data: [
    {% for supplyer in common.suppliers %}
    {
        tag: '{{ supplyer.user.username }}',
        image: '{{ supplyer.avatar.furl }}',
        id: {{ supplyer.id }}
    },
    {% endfor %}
    ]
};

{% if common %}
$('#owners').material_chip({
    placeholder: 'Entrez un pseudo',
    secondaryPlaceholder: '+pseudo',
    data: [
    {% for owner in common.owner %}
    {% if owner.id != user.id %}
    {
        tag: '{{ owner.pseudo }}',
        image: '{{ owner.avatar.furl }}',
        id: {{ owner.id }}
    },
    {% endif %}
    {% endfor %}
    ],
    autocompleteOptions: {
      data: {
        {% for user in users %}
        '{{ user.pseudo }}': '{{ user.avatar.furl }}',
        {% endfor %}
    },
    limit: Infinity,
    minLength: 1
}
});
for(var prop in common) {
    try {
        $('#' + prop).val(common[prop]);
    } catch {
    }
}
{% endif %}

function adddropify() {
    var id = 'medias-' + newId();
    var dom = '<div class="col l3 m4 s12">';
    dom += '<input type="file" multi=true id="'+ id +'" name="media-' + id + '" class="dropify" data-allowed-file-extensions="jpg jpeg" accept=".jpg,.jpeg" capture="true" data-max-file-size-preview="5M" />';
    dom += '</div>';
    $('#medias .row')[0].insertAdjacentHTML('beforeEnd', dom);

    var drEvent = $('#'+id).dropify({
        messages: {
            'default': '{% trans 'Slide-put a file here or click' %}',
            'replace': '{% trans 'Slide-put a file here or click for replacing' %}',
            'remove':  '{% trans 'Remove' %}',
            'error':   '{% trans 'Ooops, an error append.' %}'
        },
        error: {
            'fileSize': '{% blocktrans %}The file size must be lower than {{ value }} {% endblocktrans %}.',
            'minWidth': '{% blocktrans %}The image width must be greater than {{ value }} px {% endblocktrans %}.',
            'maxWidth': '{% blocktrans %}The image width must be lower than {{ value }} px {% endblocktrans %}.',
            'minHeight': '{% blocktrans %}The image height must be greater than {{ value }} px {% endblocktrans %}.',
            'maxHeight': '{% blocktrans %}The image height must be lower than {{ value }} px {% endblocktrans %}.',
            'imageFormat': '{% blocktrans %}The image format must be of type {{ value }} {% endblocktrans %}.'
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
        '<div class="carousel carousel-slider"></div>'
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
    $('.carousel').carousel();
    $('.materialboxed').materialbox();
}

function updateProperty(name) {
    $('.' + name).filter(function(index, elt) {
        elt.innerHTML = document.getElementById(name).value;
    });
}

var defaultproperties = {
    name: {
        product: 'Appareil photo Nikon D80',
        stock: 'Garage voiture et moto',
        service: 'Cours de guitare'
    },
    shortdescription: {
        product: '10 millions de pixels, carte mémoire 2 Go',
        stock: '10 places en plein centre ville',
        service: 'Maximum 10 grans débutants',
    },
    description: {
        product: '',
        stock: '',
        service: ''
    }
};

function newId() {
    return new Date().getTime();
}

function newSupply(supply) {
    if (supply === undefined) {
        supply = {
            id: newId('supply'),
            public: true,
            enable: true,
            conditions: []
        };
    }
    var dom = '<div class="supply col s12" id="supply-' + supply.id + '">\
    <ul class="collapsible" data-collapsible="accordion">\
    <li>\
    <div class="collapsible-header input-field">\
    <input type="text" id="supply-' + supply.id + '-name" name="supply-' + supply.id + '-name" />\
    <i class="material-icons right">settings</i>\
    <a onclick="cancelSupply(\'' + supply.id + '\');">\
    <i class="material-icons right">close</i>\
    </a>\
    </div>\
    <div class="collapsible-body">\
    <div class="row">\
    <div class="col s4 input-field">\
    <input type="checkbox" id="supply-' + supply.id + '-public" name="supply-' + supply.id + '-public" checked="' + supply.checked + '" />\
    <label for="supply-' + supply.id + '-public">\
    {% trans 'Public' %}\
    </label>\
    </div>\
    <div class="col s4 input-field">\
    <input type="checkbox" id="supply-' + supply.id + '-enable" name="supply-' + supply.id + '-enable" checked="' + supply.enable + '" />\
    <label for="supply-' + supply.id + '-enable">\
    {% trans 'Enable' %}\
    </label>\
    </div>\
    <div class="col s12 input-field">\
    <div class="chips tooltipped" name="supply-' + supply.id + '-suppliers" id="supply-' + supply.id + '-suppliers" data-tooltip="{% trans 'Users able to supply this condition' %}"></div>\
    <label for="supply-' + supply.id + '-supplyers">\
    {% trans 'Supplyers' %}\
    </label>\
    </div>\
    <div class="col s12 input-field">\
    <div class="chips tooltipped" name="supply-' + supply.id + '-sharedwith" id="supply-' + supply.id + '-sharedwith" data-tooltip="{% trans 'Users to notify' %}"></div>\
    <label for="supply-' + supply.id + '-sharedwith">\
    {% trans 'Shared with' %}\
    </label>\
    </div>\
    <div class="col s12 input-field">\
    <textarea class="materialize-textarea" name="supply-' + supply.id + '-description" id="supply-' + supply.id + '-description">' + supply.description + '</textarea>\
    <label for="supply-' + supplyid + '-description">\
    <i class="material-icons left">doc</i>\
    Description\
    </label>\
    </div>\
    <div class="col s4 input-field">\
    <input type="number" name="supply-' + supply.id + '-amount" id="supply-' + supply.id + '-amount" value="' + supply.amount + '" />\
    <label for="supply-' + supply.id + '-amount">\
    <i class="material-icons left">amount</i>\
    {% trans 'Amount' %}\
    </label>\
    </div>\
    <div class="col s4 input-field">\
    <input type="date" class="datepicker" name="supply-' + supply.id + '-startdate" value="' + supply.startdate + '" />\
    <label for="supply-' + supply.id + '-startdate">\
    <i class="material-icons left">date</i>\
    {% trans 'Start date' %}\
    </label>\
    </div>\
    <div class="col s4 input-field">\
    <input type="date" class="datepicker" name="supply-' + supply.id + '-duedate" id="supply-' + supply.id + '-duedate" value="' + supply.duedate + '" />\
    <label for="supply-' + supply.id + '-duedate">\
    <i class="material-icons left">date</i>\
    {% trans 'Due date' %}\
    </label>\
    </div>\
    <div class="col s3 input-field">\
    <input type="checkbox" name="supply-' + supply.id + '-peruser" id="supply-' + supply.id + '-peruser" value="' + supply.peruser + '" />\
    <label for="supply-' + supply.id + '-peruser">\
    <i class="material-icons left">group</i>\
    {% trans 'condition per user' %}\
    </label>\
    </div>\
    <div class="col s3 input-field">\
    <input type="number" name="supply-' + supply.id + '-minusers" id="supply-' + supply.id + '-minusers" value="' + supply.minusers + '" />\
    <label for="supply-' + supply.id + '-minusers">\
    <i class="material-icons left">group</i>\
    {% trans 'Min users' %}\
    </label>\
    </div>\
    <div class="col s3 input-field">\
    <input type="number" name="supply-' + supply.id + '-maxusers" id="supply-' + supply.id + '-maxusers" value="' + supply.maxusers + '" />\
    <label for="supply-' + supply.id + '-maxusers">\
    <i class="material-icons left">group</i>\
    {% trans 'Max users' %}\
    </label>\
    </div>\
    <div class="col s3 input-field">\
    <input type="checkbox" name="supply-' + supply.id + '-bid" id="supply-' + supply.id + '-bid" value="' + supply.bid + '" />\
    <label for="supply-' + supply.id + '-bid">\
    <i class="material-icons left">bid</i>\
    {% trans 'bid' %}\
    </label>\
    </div>\
    <div class="col s4 input-field share">\
    <input type="number" name="supply-' + supply.id + '-minduration" id="supply-' + supply.id + '-minduration" value="' + supply.minduration + '" />\
    <label for="supply-' + supply.id + '-minduration">\
    <i class="material-icons left">group</i>\
    {% trans 'Min duration users' %}\
    </label>\
    </div>\
    <div class="col s4 input-field share">\
    <input type="number" name="supply-' + supply.id + '-maxduration" id="supply-' + supply.id + '-maxduration" value="' + supply.maxduration + '" />\
    <label for="supply-' + supply.id + '-maxduration">\
    <i class="material-icons left">group</i>\
    {% trans 'Max duration users' %}\
    </label>\
    </div>\
    <div class="col s4 input-field share">\
    <select name="supply-' + supply.id + '-period" id="supply-' + supply.id + '-period">\
    {% for choice in choices %}\
    <option name="supply-' + supply.id + '-period-{{ choice }}" id="supply-' + supply.id + '-period-{{ choice }}" ' + ((supply.choice === '{{ choice }}')? 'selected' : '') + '>{% trans choice %}</option>\
    {% endfor %}\
    </select>\
    </div>\
    <h5>{% trans 'Price' %}</h5>';
    Object.values(supply.conditions).forEach(function(condition) {
        dom += '<div class="row">\
        <div class="col s3 input-field">\
        <input type="number" name="supply-' + supply.id + '-condition-' + condition.id + '-amount" id="supply-' + supply.id + '-condition-' + condition.id + '-amount" value="' + condition.amount + '" />\
        <label for="supply-' + supply.id + '-condition-' + condition.id + '-amount">\
        <i class="material-icons left">amount</i>\
        {% trans 'Amount' %}\
        </label>\
        </div>\
        <div class="col s3 input-field">\
        <input type="text" name="supply-' + supply.id + '-condition-' + condition.id + '-currency" id="supply-' + supply.id + '-condition-' + condition.id + '-currency" value="' + condition.currency + '" />\
        <script type="javascript">\
        $(\'#supply-' + supply.id + '-condition-' + condition.id + '-currency' + '\').autocomplete(\
        {\
            data: {\
                {% for currency in currencies %}\
                '{% trans currency %}'\
                {% endfor %}\
            },\
            minLength: 0\
        });\
        </script>\
        <label for="supply-' + supply.id + '-condition-' + condition.id + '-currency">\
        <i class="material-icons left">currency</i>\
        {% trans 'Currency' %}\
        </label>\
        </div>\
        <div class="col s3 input-field">\
        <input type="number" name="supply-' + supply.id + '-maxbid" id="supply-' + supply.id + '-maxbid" value="' + condition.maxbid + '" />\
        <label for="supply-' + supply.id + '-maxbid">\
        <i class="material-icons left">maxbid</i>\
        {% trans 'Max bid' %}\
        </label>\
        </div>\
        <div class="col s12 input-field">\
        <textarea class="materialize-textarea" name="supply-' + supply.id + '-conditino-id-description" id="supply-' + supply.id + '-condition-' + condition.id + '-description">' + condition.description + '</textarea>\
        <label for="supply-' + supply.id + '-condition-' + condition.id + '-description">\
        <i class="material-icons">\
        description\
        </i>\
        {% trans 'Description' %}\
        </label>\
        </div>\
        </div>'
    });
    dom += '</div></div></li></ul></div>';
    document.getElementById('conditions').insertAdjacentHTML('endbefore', dom);
}

Object.values(common.supplyings).forEach(function(supply) {
    newSupply(supply);
});
newSupply();


function selectCommon(commonid) {
    var dom = document.getElementById('select-common-' + commonid);
    var selection = document.getElementById('select-commons');
    var child = selection.children[1];
    if (child !== undefined) {
        dom.appendChild(child);
    }
    selection.appendChild(dom);
    document.getElementById('id').setAttribute('value', commonid);
}

{% include 'map.js' %}
