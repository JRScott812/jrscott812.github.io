---
layout: default
title: Projects
permalink: /projects/
---

# Projects

{% assign published_projects = site.projects | where_exp: "p", "p.published != false" %}
{% assign categories = published_projects | group_by: "category" %}
{% for group in categories %}
{% if group.items.size > 0 %}

<section class="project-section">
	<h2>{{ group.name }}</h2>
	<div class="grid grid-2">
		{% for project in group.items %}
		{% include project-card.html project=project %}
		{% endfor %}
	</div>
</section>
{% endif %}
{% endfor %}
