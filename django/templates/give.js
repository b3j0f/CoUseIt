/*$('#keywords').material_chip({

});

var categories = {
	{% for category in categories %}
	{% for category in category.categories.all %}
	'{{ category.name }}': {
		parent: '{{ category.name }}',
		properties: {
			{% for propertywvalues in category.allpropertieswvalues %}
			'{{ propertywvalues.name }}': {
				unit: '{{ propertywvalues.unit }}',
				values: [
				{% for value in propertywvalues.values %}
				'{{ value }}',
				{% endfor %}
				]
			},
			{% endfor %}
		}
	},
	{% endfor %}
	{% endfor %}
};

function updateProperties(elt) {
	var propertyfilter = document.getElementById('property-filter');
	document.getElementById('properties').remove();
	var propertiesElt = document.createElement('div');
	propertiesElt.setAttribute('id', 'properties');
	propertyfilter.appendChild(propertiesElt);
	var properties = [];//categories[elt.value].properties;
	for(var name in properties) {
		var property = properties[name];

		var propertyElt = document.createElement('div');
		propertyElt.setAttribute('class', 'row input-field');

		if (property.values.length === 0) {
			var valueElt = document.createElement('input');
			valueElt.setAttribute('type', 'number');
			valueElt.getValue = function() {
				return this.value;
			}.bind(valueElt);
			valueElt.addEventListener('change', function(value) {
				filter();
			});
		} else {
			var length = property.values.length;
			if (isNaN(property.values[0])) {
				var valueElt = document.createElement('select');
				valueElt.getValue = function() {
					return this.value;
				}.bind(valueElt);
				valueElt.addEventListener('change', function(value) {
					filter();
				});
				property.values.forEach(function(value) {
					var optionElt = document.createElement('option');
					optionElt.setAttribute('value', value);
					optionElt.innerHTML = value;
					valueElt.appendChild(optionElt);
				});
			} else {
				var valueElt = document.createElement('div');
				var range = {}, i = 0;

				var first = property.values[0];
				var last = property.values[length - 1];
				range['min'] = i++;
				property.values.slice(1, length - 1).forEach(function(value) {
					var key = value * 100 / (last - first);
					range[key + '%'] = i++;
				});
				range['max'] = i;
				var values = property.values.slice();
				var to = function(value) {
					return this[value];
				}.bind(property.values);
				noUiSlider.create(valueElt, {
					property: property,
					start: [range.min, range.max],
					connect: true,
					snap: true,
					range: range,
					tooltips: true,
					step: 1,
					format: {
						to: to,
						from: to,
						property: property
					}
				});
				valueElt.noUiSlider.on('update', function( values, handle ) {
					filter();
				});
				valueElt.getValue = function () {
					return this.noUiSlider.get();
				}.bind(valueElt);
			}
		}
		valueElt.property = property;
		valueElt.setAttribute('id', 'property-' + name);
		valueElt.setAttribute('class', 'property');
		propertyElt.appendChild(valueElt);

		var nameElt = document.createElement('label');
		nameElt.setAttribute('for', 'property-' + name);
		nameElt.innerHTML = name;
		propertyElt.appendChild(nameElt);

		propertiesElt.appendChild(propertyElt);
	}
}

function filter() {
	$('.property').each(function(index, elt) {
		var value = elt.getValue();
		//console.log(value, elt.twist);
	});
}

function toggleProperties() {
	var propertyFilter = $('#property-filter');
	var arrowicon = propertyFilter.hasClass('hide') ? 'up' : 'down';
	$('.togglepropertiesicons').text('keyboard_arrow_' + arrowicon);
	propertyFilter.toggleClass('hide');
}

updateProperties(document.getElementById('category'));
*/