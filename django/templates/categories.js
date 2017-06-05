{% load i18n %}

var high = document.getElementById('categories-0');
var middle = document.getElementById('categories-1');
var low = document.getElementById('categories-2');

function insertCategoryDom(dom, lvl, id, name, parentid, gparentid) {
	var cls = 'category lvl-' + lvl + ' category-' + parentid + ' category-' + gparentid;
	var action = 'onclick="selectCategory(\'' + id + '\', ' + lvl + ');"';
	var catdom = '<a id="category-' + id + '" class="btn btn-flat ' + cls + '" ' + action + '>' + name + '</a>';
	dom.insertAdjacentHTML('beforeEnd', catdom);
	return $('#category-' + id);
}

var all = {
	id: 'all',
	name: '{% trans 'all' %}',
	url: '',
	lvl: 0
};

var categories = {
	all: all
};

insertCategoryDom(high, all.lvl, all.id, all.name);

{% autoescape off %}
{% for topcategory in categories %}
var topid = '{{ topcategory.name }}'.replace('/', '--');
var topname = '{% trans topcategory.display_name %}';
var topdom = insertCategoryDom(high, 0, topid, topname);
categories[topid] = {
	id: topid,
	name: topname,
	url: '{{ topcategory.media.furl }}',
	lvl: 0
};
{% for middlecategory in topcategory.children %}
var middleid = '{{ middlecategory.name }}'.replace('/', '--');
var middlename = '{% trans middlecategory.display_name %}';
topdom.addClass('category-' + middleid).addClass('category-chain-' + middleid);
var middledom = insertCategoryDom(middle, 1, middleid, middlename, topid);
categories[middleid] = {
	id: middleid,
	name: middlename,
	url: '{{ middlecategory.media.furl }}',
	parent: topid,
	lvl: 1
};
$('#category-' + topid).addClass('category-' + middleid);
{% for lowcategory in middlecategory.children %}
var lowid = '{{ lowcategory.name }}'.replace('/', '--');
var lowname = '{% trans lowcategory.display_name %}';
topdom.addClass('category-' + lowid).addClass('category-chain-' + lowid);
middledom.addClass('category-' + lowid).addClass('category-chain-' + lowid);
var lowdom = insertCategoryDom(low, 2, lowid, lowname, middleid, topid);
categories[lowid] = {
	id: lowid,
	name: lowname,
	url: '{{ lowcategory.media.furl }}',
	parent: middleid,
	lvl: 2
};
$('#category-' + topid).addClass('category-' + lowid);
$('#category-' + middleid).addClass('category-' + lowid);
{% endfor %}
{% endfor %}
{% endfor %}
{% endautoescape %}

var selectedcategories = [];

function selectCategory(id, lvl) {
	if (selectedcategories.length < lvl) {
		selectedcategories.push(id);
	} else {
		selectedcategories = selectedcategories.slice(0, lvl + 1);
		selectedcategories[lvl] = id;
	}

	$('.category').hide();
	$('.category').removeClass('btn');
	$('.category').addClass('btn-flat');

	$('.lvl-0').show();

	selectedcategories.forEach(function (category) {
		$('#category-' + category).addClass('btn');
		$('#category-' + category).removeClass('btn-flat');
	});

	var newlvl = 0;

	if (id === all.id) {
		$('#categories-1').hide();
		$('#categories-2').hide();
		//$('#categories-1').removeClass('carousel-item');
		//$('#categories-2').removeClass('carousel-item');
		newlvl = 0;
	} else {
		//$('#categories-1').addClass('carousel-item');
		$('#categories-1').show();
		$('.category-' + selectedcategories[0] + '.lvl-1').show();
		if (lvl > 0) {
			//$('#categories-2').addClass('carousel-item');
			$('#categories-2').show();
			$('.category-' + selectedcategories[1] + '.lvl-2').show();
		} else {
			//$('#categories-2').removeClass('carousel-item');
			$('#categories-2').hide();
		}
		newlvl = Math.min(lvl + 1, 2);
	}

	$('#categories-' + lvl).css('background-image', categories[id].url);
	$('#category').val(id.replace('--', '/'));
	$('#categories').carousel({fullWidth: true});
	$('#categories').carousel('set', newlvl);
	$('#category-choose').text('{% trans 'Category:' %} ' + categories[id].name);

	if (lvl === 2) {
		$('#categories').fadeToggle();
	}

}

var category = categories['{{ category.name }}'.replace('/', '--')];

function updateCategory(category) {
	if (categories[category] !== undefined) {
		selectedcategories = [];
		_selectedcategories = [];
		while (categories[category].parent) {
			_selectedcategories.push(category.id);
			category = category.parent;
		}
		_selectedcategories.push(category.id);
		_selectedcategories.forEach(function(category) {
			selectedcategories.push(category);
		});
		selectCategory(category, categories[category].lvl);
	}
}

if (category) {
	updateCategory(category.id);
} else {
	selectCategory('all', 0);
}

$('#categories').hide();

/** method to use in order to get a user selected category. */
function getCategory(handler) {
	$('.modal').modal({
		dismissible: true, // Modal can be dismissed by clicking outside of the modal
		complete: function() { handler($('#category').val()); } // Callback for Modal close
	});
}

function viewCategories(newlvl) {
	$('#categories').carousel(newlvl);
}