{% load i18n %}

var {{ name }}_catname = '{{ name }}';

var {{ name }}_high = document.getElementById({{ name }}_catname + '-categories-0');
var {{ name }}_middle = document.getElementById({{ name }}_catname + '-categories-1');
var {{ name }}_low = document.getElementById({{ name }}_catname + '-categories-2');

function {{ name }}_insertCategoryDom(dom, lvl, id, name, parentid, gparentid) {
	var cls = {{ name }}_catname + '-category ' + {{ name }}_catname + '-lvl-' + lvl + ' ' + {{ name }}_catname + '-category-' + parentid + ' ' + {{ name }}_catname + '-category-' + gparentid;
	var action = 'onclick="{{ name }}_selectCategory(\'' + id + '\', ' + lvl + ');"';
	var catdom = '<a id="' + {{ name }}_catname + '-category-' + id + '" class="btn btn-flat ' + cls + '" ' + action + '>' + name + '</a>';
	dom.insertAdjacentHTML('beforeEnd', catdom);
	return $('#' + {{ name }}_catname + '-category-' + id);
}

var all = {
	id: 'all',
	name: '{% trans 'all' %}',
	url: '',
	lvl: 0
};

var {{ name  }}_categories = {
	all: all
};

{{ name }}_insertCategoryDom({{ name }}_high, all.lvl, all.id, all.name);

{% autoescape off %}
{% for topcategory in categories %}
var topid = '{{ topcategory.name }}'.replace('/', '--');
var topname = '{% trans topcategory.display_name %}';
var topdom = {{ name }}_insertCategoryDom({{ name }}_high, 0, topid, topname);
var properties = {
{% for property in topcategory.properties %}
'{{ property.name }}': {
	'name': '{% trans property.display_name %}',
	'unit': '{{ trans property.unit }}',
	'values': '{{ property.values }}',
	'allvalues': [{% for value in property.allvalues %}'{{ value }}', {% endfor %}]
},
{% endfor %}
};
{{ name }}_categories[topid] = {
	id: topid,
	name: topname,
	url: '{{ topcategory.media.furl }}',
	lvl: 0,
	properties
};
{% for middlecategory in topcategory.children %}
var middleid = '{{ middlecategory.name }}'.replace('/', '--');
var middlename = '{% trans middlecategory.display_name %}';
topdom.addClass({{ name }}_catname + 'category-' + middleid).addClass({{ name }}_catname + 'category-chain-' + middleid);
var middledom = {{ name }}_insertCategoryDom({{ name }}_middle, 1, middleid, middlename, topid);
var properties = {
{% for property in middlecategory.properties %}
'{{ property.name }}': {
	'name': '{% trans property.display_name %}',
	'unit': '{{ trans property.unit }}',
	'values': '{{ property.values }}',
	'allvalues': [{% for value in property.allvalues %}'{{ value }}', {% endfor %}]
},
{% endfor %}
};
{{ name }}_categories[middleid] = {
	id: middleid,
	name: middlename,
	url: '{{ middlecategory.media.furl }}',
	parent: topid,
	lvl: 1,
	properties: properties
};
$('#' + {{ name }}_catname + '-category-' + topid).addClass({{ name }}_catname + '-category-' + middleid);
{% for lowcategory in middlecategory.children %}
var lowid = '{{ lowcategory.name }}'.replace('/', '--');
var lowname = '{% trans lowcategory.display_name %}';
topdom.addClass({{ name }}_catname + '-category-' + lowid).addClass({{ name }}_catname + '-category-chain-' + lowid);
middledom.addClass({{ name }}_catname + '-category-' + lowid).addClass({{ name }}_catname + '-category-chain-' + lowid);
var lowdom = {{ name }}_insertCategoryDom({{ name }}_low, 2, lowid, lowname, middleid, topid);
var properties = {
{% for property in lowcategory.properties %}
'{{ property.name }}': {
	'name': '{% trans property.display_name %}',
	'unit': '{{ trans property.unit }}',
	'values': '{{ property.values }}',
	'allvalues': [{% for value in property.allvalues %}'{{ value }}', {% endfor %}]
},
{% endfor %}
};
{{ name }}_categories[lowid] = {
	id: lowid,
	name: lowname,
	url: '{{ lowcategory.media.furl }}',
	parent: middleid,
	lvl: 2,
	properties
};
$('#' + {{ name }}_catname + '-category-' + topid).addClass({{ name }}_catname + '-category-' + lowid);
$('#' + {{ name }}_catname + '-category-' + middleid).addClass({{ name }}_catname + '-category-' + lowid);
{% endfor %}
{% endfor %}
{% endfor %}
{% endautoescape %}

var {{ name }}_selectedcategories = [];

function {{ name }}_selectCategory(id, lvl) {
	if ({{ name }}_selectedcategories.length < lvl) {
		{{ name }}_selectedcategories.push(id);
	} else {
		{{ name }}_selectedcategories = {{ name }}_selectedcategories.slice(0, lvl + 1);
		{{ name }}_selectedcategories[lvl] = id;
	}

	$('.' + {{ name }}_catname + '-category').hide();
	$('.' + {{ name }}_catname + '-category').removeClass('btn');
	$('.' + {{ name }}_catname + '-category').addClass('btn-flat');

	$('.' + {{ name }}_catname + '-lvl-0').show();

	{{ name }}_selectedcategories.forEach(function (category) {
		$('#' + {{ name }}_catname + '-category-' + category).addClass('btn');
		$('#' + {{ name }}_catname + '-category-' + category).removeClass('btn-flat');
	});

	var newlvl = 0;

	if (id === all.id) {
		$('#' + {{ name }}_catname + '-categories-1').hide();
		$('#' + {{ name }}_catname + '-categories-2').hide();
		//$('#categories-1').removeClass('carousel-item');
		//$('#categories-2').removeClass('carousel-item');
		newlvl = 0;
	} else {
		//$('#categories-1').addClass('carousel-item');
		$('#' + {{ name }}_catname + '-categories-1').show();
		$('.' + {{ name }}_catname + '-category-' + {{ name }}_selectedcategories[0] + '.' + {{ name }}_catname + '-lvl-1').show();
		if (lvl > 0) {
			//$('#categories-2').addClass('carousel-item');
			$('#' + {{ name }}_catname + '-categories-2').show();
			$('.' + {{ name }}_catname + '-category-' + {{ name }}_selectedcategories[1] + '.' + {{ name }}_catname + '-lvl-2').show();
		} else {
			//$('#categories-2').removeClass('carousel-item');
			$('#' + {{ name }}_catname + '-categories-2').hide();
		}
		newlvl = Math.min(lvl + 1, 2);
	}

	$('#' + {{ name }}_catname + '-categories-' + lvl).css('background-image', {{ name }}_categories[id].url);
	$('#' + {{ name }}_catname + '-category').val(id.replace('--', '/'));
	$('#' + {{ name }}_catname + '-categories').carousel({fullWidth: true});
	$('#' + {{ name }}_catname + '-categories').carousel('set', newlvl);
	$('#' + {{ name }}_catname + '-category-choose').text('{% trans 'Category:' %} ' + {{ name }}_categories[id].name);

	if (lvl === 2) {
		$('#' + {{ name }}_catname + '-categories').fadeToggle();
	}

}

var {{ name }}_category = {{ name }}_categories['{{ category.name }}'.replace('/', '--')];

function updateCategory(category) {
	{{ name }}_selectedcategories = [];
	var _selectedcategories = [];
	while (categories[category].parent) {
		_selectedcategories.push(category.id);
		category = category.parent;
	}
	_selectedcategories.push(category.id);
	_selectedcategories.forEach(function(category) {
		{{ name }}_selectedcategories.push(category);
	});
	{{ name }}_selectCategory(category, categories[category].lvl);
}

if ({{ name }}_category) {
	{{ name }}_updateCategory({{ name }}_category.id);
} else {
	{{ name }}_selectCategory('all', 0);
}

$('#' + {{ name }}_catname + '-categories').hide();

function viewCategories(newlvl) {
	$('#' + {{ name }}_catname + '-categories').carousel(newlvl);
}