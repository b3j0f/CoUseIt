var topcategories = {};
var midcategories = {};

var toplis = '<li><a onclick="selectcat">Tout</a></li>';
var midlis = '<li>Tout</li>';
var lowlis = '<li>Tout</li>';

{% for topcategory in topcategories %}
topcategories['{{ topcategory.name }}'] = [];
toplis += '<li><a onclick="selecttop(this)">{{ topcategory.name }}</a></li>';
	{% for midcategory in topcategory.children.all %}
topcategories['{{ topcategory.name }}'].push('{{ midcategory.name }}');
midlis += '<li class="{{ topcategory.name }}">{{ midcategory.name }}</li>';
midcategories['{{ midcategory.name }}'] = [];
		{% for lowcategory in midcategory.children.all %}
midcategories['{{ midcategory.name }}'].push('{{ lowcategory.name }}');
lowlis += '<li class="{{ topcategory.name }} {{ midcategory.name }}">{{ lowcategory.name }}</li>';
		{% endfor %}
	{% endfor %}
{% endfor %}

$('#topcategories')[0].insertAdjacentHTML(
	'endbefore',
	toplis
);

$('#midcategories')[0].insertAdjacentHTML(
	'endbefore',
	midlis
);

$('#lowcategory')[0].insertAdjacentHTML(
	'endbefore',
	lowlis
);

function selectcat() {
	$('#')[0]
}
