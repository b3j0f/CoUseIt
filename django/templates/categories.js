var cats = {};

{% for cat in cats %}
cats[{{ cat.name }}] = [];
{% if cat.parent %}
if (cats[{{ cat.parent.name }}] !== undefined) {
	cats[{{ cat.parent.name}}] = [ {{ cat.name }} ];
} else {
	cats[{{ cat.parent.name }}].push( {{ cat.name }})
};
{% endif %}
{% endfor %}
