$('.keywords').material_chip({
  data: [/*{
    tag: 'Apple',
    image: '', //optional
    id: 1, //optional
  }, {
    tag: 'Microsoft',
  }, {
    tag: 'Google',
  }*/],
  placeholder: '+Mot clef',
  secondaryPlaceholder: '+Mot clef',
  autocompleteData: {
    /*'Apple': null,
    'Microsoft': null,
    'Google': null*/
  }
});

var categories = {
  {% for parentcategory in parentcategories %}
  {% for category in parentcategory.categories %}
  '{{ category.name }}': {
    {% for property in category.properties %}
    '{{ property.id }}': {
      'name': '{{ property.id }}',
      'values': {{ property.allvalues }},
      'unit': '{{ property.unit }}'
    }
    {% endfor %}
  },
  {% endfor %}
  {% endfor %}
};

function displayproperties(category) {

}

$('.range.property').forEach(function(elt) {
  noUISlider.create(elt, {
    start: [ 1450, 2050, 2350, 3000 ], // 4 handles, starting at...
  margin: 300, // Handles must be at least 300 apart
  limit: 600, // ... but no more than 600
  connect: true, // Display a colored bar between the handles
  direction: 'rtl', // Put '0' at the bottom of the slider
  orientation: 'vertical', // Orient the slider vertically
  behaviour: 'tap-drag', // Move handle on tap, bar is draggable
  step: 150,
  tooltips: true,
  format: wNumb({
    decimals: 0
  }),
  range: {
    'min': 1300,
    'max': 3250
  },
  pips: { // Show a scale with the slider
    mode: 'steps',
    stepped: true,
    density: 4
  }
});
});