var topcategories = {};
var midcategories = {};

var toplis = '<li><a onclick="selectcat(\'top\', this);">Tout</a></li>';
var midlis = '<li><a onclick="selectcat(\'mid\', this);">Tout</a></li>';
var lowlis = '<li><a onclick="selectcat(\'low\', this);">Tout</a></li>';;

{% for topcategory in topcategories %}
var topcat = '{{ topcategory.name }}'.replace('/', '-');
topcategories['{{ topcategory.name }}'] = [];
toplis += '<li class="top"><a id="' + topcat + '" onclick="selectcat(\'top\', this)">{{ topcategory.name }}</a></li>';
	{% for midcategory in topcategory.children.all %}
	var midcat = '{{ midcategory.name }}'.replace('/', '-');
topcategories['{{ topcategory.name }}'].push('{{ midcategory.name }}');
midlis += '<li class="mid ' + topcat + '"><a id="' + midcat + '" onclick="selectcat(\'mid\', this)">{{ midcategory.name }}</a></li>';
midcategories['{{ midcategory.name }}'] = [];
		{% for lowcategory in midcategory.children.all %}
var lowcat = '{{ lowcategory.name }}'.replace('/', '-');
midcategories['{{ midcategory.name }}'].push('{{ lowcategory.name }}');
lowlis += '<li class="low ' + topcat + ' ' + midcat + '"><a id="' + lowcat + '" onclick="selectcat(\'low\', this)">{{ lowcategory.name }}</a></li>';
		{% endfor %}
	{% endfor %}
{% endfor %}

$('#topcategories')[0].insertAdjacentHTML(
	'beforeEnd',
	toplis
);

$('#midcategories')[0].insertAdjacentHTML(
	'beforeEnd',
	midlis
);

$('#lowcategories')[0].insertAdjacentHTML(
	'beforeEnd',
	lowlis
);

var selectedtop = 'tout';
var selectedmid = 'tout';
var selectedlow = 'tout';

$('#midcategory').hide();
$('#lowcategory').hide();

function selectcat(type, elt) {
	var id = elt.id ? elt.id : 'tout';
	switch(type) {
		case 'top':
			if (selectedtop === id) break;
			selectedtop = id;
			if (! elt.id) {
				$('.lowcategory').hide();
				$('#lowcategory').hide();
				$('.midcategory').hide();
				$('#midcategory').hide();
			} else {
				selectedmid = selectedlow = 'tout';
				$('.lowcategory').hide();
				$('#lowcategory').hide();
				$('.mid').hide();
				$('.mid.'+id).show();
				$('#midcategory').show();
			}
			break;
		case 'mid':
			if (selectedmid === id) break;
			selectedmid = id;
			if (! elt.id) {
				$('.lowcategory').hide();
				$('#lowcategory').hide();
			} else {
				selectedlow = 'tout';
				$('.low').hide();
				$('.low.'+id).show();
				$('#lowcategory').show();
			}
			break;
		case 'low':
			if (selectedlow === id) break;
			selectedlow = id;
	};
	$('#topcategory')[0].innerHTML = selectedtop;
	$('#midcategory')[0].innerHTML = selectedmid;
	$('#lowcategory')[0].innerHTML = selectedlow;
}

var map = new ol.Map({
	target: 'map',
	layers: [
	new ol.layer.Tile({
		source: new ol.source.OSM()
	})
	],
	view: new ol.View({
		center: ol.proj.fromLonLat([37.41, 8.82]),
		zoom: 16
	})
});
function getCurrentPosition() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(
			function(pos) {
				map.getView().setCenter(ol.proj.fromLonLat([pos.coords.longitude, pos.coords.latitude]));
			}
			);
	} else {
		$('#error').innerHTML = 'Ce navigateur ne supporte pas la géolocalisation.';
	}
};
function getLocation() {
	var zipcode = $('zipcode').val();
	// TODO : go to zipcode
};