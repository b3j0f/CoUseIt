'{{ common.id }}': {
    id: '{{ common.id }}',
    name: '{{ common.name }}',
    shortdescription: '{{ common.shortdescription }}',
    description: '{{ common.description }}',
    created: '{{ common.created }}',
    owners: [{% for owner in common.owners.all %}'{{ owner.id }}', {% endfor %}],
    suppliers: [{% for supplyer in common.suppliers.all %}'{{ supplyer.id }}', {% endfor %}],
    users: [{% for user in common.users.all %}'{{ user.id }}', {% endfor %}],
    category: '{{ common.category }}',
    professional: {% if common.professional %}true{% else %}false{% endif %},
    medias: [{% for media in common.medias.all %}'{{ media.furl }}', {% endfor %}],
    location: '{{ common.location }}',
    quantity: {{ common.quantity }},
    tostock: {{ common.tostock }},
    {% if commontype == 'stock' %}
    capacity: {{ common.capacity }},
    contentcategory: '{{ common.contentcategory }}',
    {% endif %}
    {% if commontype == 'package' %}
    commons: {
        {% for content in common.commons.all %}
        {% include 'common.js' with common=content %}
        {% endfor %}
    },
    {% endif %}
    supplyings: {
        {% for supply in common.supplyings %}
        '{{ supply.id }}': {
            id: '{{ supply.id }}',
            name: '{{ supply.name }}',
            description: '{{ supply.description }}',
            amount: {{ supply.amount }},
            startdate: '{{ supply.startdate }}',
            duedate: '{{ supply.duedate }}',
            peruser: {% if supply.peruser %}true{% else %}false{% endif %},
            minusers: {{ supply.minusers }},
            maxusers: {{ supply.maxusers }},
            bid: {% if supply.bid %}true{% else %}false{% endif %},
            sharedwith: [{% for sharedwith in supply.sharedwith %}'{{ sharedwith.pseudo }}', {% endfor %}],
            public: {% if supply.public %}true{% else %}false{% endif %},
            enabled: {% if supply.enabled %}true{% else %}false{% endif %},
            supplyers: [{% for supplyer in supply.supplyers %}'{{ supplyer.pseudo }}', {% endfor %}],
            objective: {
                {% for key, value in supply.objectivekeyvalues %}
                '{{ key }}': '{{ value }}',
                {% endfor %}
            },
            {% if action == 'share' %}
            minduration: '{{ supply.minduration }}' || 0,
            maxduration: '{{ supply.maxduration}}' || 0,
            period: '{{ supply.period }}',
            {% endif %}
            conditions: {
                {% for condition in supply.conditions %}
                '{{ condition.id }}': {
                    id: '{{ condition.id }}',
                    currency: '{{ condition.currency.name }}',
                    amount: {{ condition.amount }},
                    description: '{{ condition.description }}',
                    maxbid: '{{ condition.maxbid }}' || 0
                },
                {% endfor %}
            }
        }
        {% endfor %}
    }
}
