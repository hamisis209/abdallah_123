from django.shortcuts import render
from django.utils.text import slugify

def _get_course_by_id(course_id):
	if int(course_id) == 1:
		return get_mathematics_course()
	if int(course_id) == 2:
		return get_physics_course()
	if int(course_id) == 3:
		return get_chemistry_course()
	return None

def _find_topic(course, form_name, topic_slug):
	for division in course.get('divisions', []):
		for form in division.get('forms', []):
			if slugify(form['form']) == slugify(form_name):
				for topic in form.get('topics', []):
					if slugify(topic) == slugify(topic_slug):
						return {
							'division': division['name'],
							'form': form['form'],
							'topic': topic
						}
	return None

def _make_notes(topic):
	keywords = [w for w in slugify(topic).split('-') if len(w) >= 4]
	if not keywords:
		keywords = [topic]
	return {
		'title': topic,
		'overview': (
			f'This note summarizes the core ideas in {topic}, the language used to describe it, '
			'and the common ways it appears in problems and classroom tasks.'
		),
		'objectives': [
			f'Define and explain {topic} in your own words.',
			f'Recognize {topic} in questions, diagrams, or data.',
			f'Apply the main rules or procedures related to {topic}.',
			f'Check answers and justify reasoning using {topic} concepts.',
		],
		'key_points': [
			f'What {topic} means and how it connects to other topics in the form.',
			f'The most important terms, symbols, and representations used in {topic}.',
			f'The main steps or rules you should follow when solving {topic} questions.',
			f'How to interpret results and decide if an answer makes sense for {topic}.',
			f'How {topic} is used in real situations or practical contexts.',
		],
		'process': [
			'Read the question carefully and identify the given information.',
			'Choose a suitable rule, formula, or method for the topic.',
			'Solve step by step, keeping units or labels consistent.',
			'Check your result and explain why it is reasonable.',
		],
		'common_mistakes': [
			'Skipping definitions or not stating what a symbol represents.',
			'Mixing units or using inconsistent notation.',
			'Applying a rule in the wrong situation.',
			'Rounding too early or ignoring the required form of the answer.',
		],
		'examples': [
			f'Worked example: Solve a standard {topic} problem using the main method.',
			f'Interpret a diagram or table related to {topic} and explain the result.',
		],
		'vocabulary': keywords,
		'practice': [
			f'Write a short definition of {topic} and give one example.',
			f'Solve two typical problems related to {topic} and show your steps.',
			f'Create one real-life situation where {topic} can be applied.',
			f'Explain one common mistake in {topic} and how to avoid it.',
		],
	}

def course_list(request):
    # Accurate course list with specific links for each course
    courses = [
        {
            'id': 1,
            'title': 'Mathematics',
        'description': 'Mathematics for O-Level (Form 1-4) and Advanced (Form 5-6).',
            'detail_url': 'course_detail',
        },
        {
            'id': 2,
            'title': 'Physics',
            'description': 'Physics for O-Level (Form 1-4) and Advanced (Form 5-6).',
            'detail_url': 'course_detail',
        },
        {
            'id': 3,
            'title': 'Chemistry',
            'description': 'Chemistry for O-Level (Form 1-4) and Advanced (Form 5-6).',
            'detail_url': 'course_detail',
        },
    ]
    return render(request, 'courses/course_list.html', {'courses': courses})

def get_mathematics_course():
	return {
		'id': 1,
		'title': 'Mathematics',
		'description': 'Mathematics for O-Level (Form 1-4) and Advanced (Form 5-6) based on the TIE curriculum.',
		'divisions': [
			{
				'name': 'O-Level',
				'forms': [
					{'form': 'Form 1', 'topics': [
						'Numbers',
						'Fractions, Decimals, and Percentages',
						'Units and Measurements',
						'Algebraic Expressions',
						'Geometry (Angles, Triangles, Quadrilaterals)',
						'Sets',
						'Ratio, Proportion, and Rates',
						'Coordinate Geometry (Introduction)',
						'Statistics (Introduction)',
						'Probability (Introduction)'
					]},
					{'form': 'Form 2', 'topics': [
						'Real Numbers',
						'Exponents and Radicals',
						'Algebraic Equations and Inequalities',
						'Geometry (Polygons, Circles)',
						'Perimeter, Area, and Volume',
						'Linear Functions and Graphs',
						'Statistics (Data Collection and Presentation)',
						'Probability (Simple Events)',
						'Commercial Arithmetic'
					]},
					{'form': 'Form 3', 'topics': [
						'Quadratic Equations and Functions',
						'Simultaneous Equations',
						'Trigonometry (Introduction)',
						'Geometry (Similarity and Congruence)',
						'Transformations (Translation, Rotation, Reflection, Enlargement)',
						'Matrices and Determinants (Introduction)',
						'Statistics (Measures of Central Tendency and Dispersion)',
						'Probability (Compound Events)',
						'Sequences and Series'
					]},
					{'form': 'Form 4', 'topics': [
						'Advanced Trigonometry',
						'Vectors',
						'Matrices and Determinants (Advanced)',
						'Calculus (Introduction: Differentiation and Integration)',
						'Statistics (Advanced: Probability Distributions)',
						'Linear Programming',
						'Coordinate Geometry (Advanced)',
						'Financial Mathematics',
						'Revision and Project Work'
					]},
				]
			},
			{
				'name': 'Advanced (A-Level)',
				'forms': [
					{'form': 'Form 5', 'topics': [
						'Functions and Relations',
						'Advanced Algebra',
						'Trigonometry (Advanced)',
						'Calculus (Differentiation and Integration)',
						'Vectors (Advanced)',
						'Matrices and Linear Transformations',
						'Probability and Statistics (Advanced)',
						'Complex Numbers (Introduction)',
						'Coordinate Geometry (Conic Sections)',
						'Sequences and Series (Advanced)'
					]},
					{'form': 'Form 6', 'topics': [
						'Differential Equations',
						'Further Calculus (Applications)',
						'Numerical Methods',
						'Mechanics (Statics and Dynamics)',
						'Probability Distributions (Normal, Binomial, Poisson)',
						'Linear Programming (Advanced)',
						'Complex Numbers (Advanced)',
						'Mathematical Induction',
						'Project/Research Work',
						'Revision'
					]},
				]
			}
		]
	}

def get_physics_course():
	return {
		'id': 2,
		'title': 'Physics',
		'description': 'Physics for O-Level (Form 1-4) and Advanced (Form 5-6).',
		'divisions': [
			{
				'name': 'O-Level',
				'forms': [
					{'form': 'Form 1', 'topics': [
						'Introduction to Physics',
						'Measurements and Units',
						'Forces and Motion (Basics)',
						'Energy and Work (Basics)',
						'Heat and Temperature (Basics)',
						'Light (Introduction)',
						'Safety in the Laboratory'
					]},
					{'form': 'Form 2', 'topics': [
						'Motion and Speed',
						'Forces and Pressure',
						'Energy and Power',
						'Simple Machines',
						'Heat Transfer',
						'Light (Reflection and Refraction)',
						'Sound (Basics)'
					]},
					{'form': 'Form 3', 'topics': [
						'Density and Pressure in Fluids',
						'Archimedes’ Principle',
						'Electricity (Current, Voltage, Resistance)',
						'Magnetism (Basics)',
						'Waves (Introduction)',
						'Radioactivity (Basics)'
					]},
					{'form': 'Form 4', 'topics': [
						'Projectile Motion',
						'Moments and Equilibrium',
						'Work, Energy, and Power (Advanced)',
						'Electric Circuits',
						'Electromagnetism',
						'Electronics (Diodes, Transistors)',
						'Modern Physics (Intro)'
					]},
				]
			},
			{
				'name': 'Advanced (A-Level)',
				'forms': [
					{'form': 'Form 5', 'topics': [
						'Mechanics (Kinematics, Dynamics)',
						'Circular Motion',
						'Gravitation',
						'Oscillations',
						'Electric Fields',
						'Current Electricity',
						'Waves (Detailed)'
					]},
					{'form': 'Form 6', 'topics': [
						'Electromagnetic Induction',
						'AC Circuits',
						'Electronics (Amplifiers)',
						'Quantum Physics (Intro)',
						'Atomic and Nuclear Physics',
						'Thermodynamics',
						'Medical and Applied Physics'
					]},
				]
			}
		]
	}


def get_chemistry_course():
	return {
		'id': 3,
		'title': 'Chemistry',
		'description': 'Chemistry for O-Level (Form 1-4) and Advanced (Form 5-6).',
		'divisions': [
			{
				'name': 'O-Level',
				'forms': [
					{'form': 'Form 1', 'topics': [
						'Introduction to Chemistry',
						'Matter and Its States',
						'Elements, Compounds, and Mixtures',
						'Atomic Structure (Basics)',
						'Separation Techniques',
						'Laboratory Safety'
					]},
					{'form': 'Form 2', 'topics': [
						'Chemical Equations',
						'Acids, Bases, and Salts (Basics)',
						'Periodic Table (Intro)',
						'Metals and Non-metals',
						'Carbon and Its Compounds (Intro)',
						'Water and Air'
					]},
					{'form': 'Form 3', 'topics': [
						'Chemical Bonding',
						'Rates of Reaction (Intro)',
						'Energy Changes in Reactions',
						'Acids, Bases, and Salts (Advanced)',
						'Electrolysis (Intro)',
						'Qualitative Analysis'
					]},
					{'form': 'Form 4', 'topics': [
						'Mole Concept',
						'Redox Reactions',
						'Electrochemistry',
						'Organic Chemistry (Basics)',
						'Industrial Chemistry',
						'Environmental Chemistry'
					]},
				]
			},
			{
				'name': 'Advanced (A-Level)',
				'forms': [
					{'form': 'Form 5', 'topics': [
						'Atomic Structure (Advanced)',
						'Chemical Bonding and Structure',
						'States of Matter',
						'Chemical Thermodynamics',
						'Chemical Kinetics',
						'Equilibrium'
					]},
					{'form': 'Form 6', 'topics': [
						'Electrochemistry (Advanced)',
						'Organic Chemistry (Advanced)',
						'Inorganic Chemistry',
						'Analytical Chemistry',
						'Polymers and Materials',
						'Chemistry in Industry and Environment'
					]},
				]
			}
		]
	}


def course_detail(request, course_id):
	course = _get_course_by_id(course_id)
	if not course:
		course = {'id': course_id, 'title': f'Course {course_id}', 'description': 'Course details here.'}
	return render(request, 'courses/course_detail.html', {'course': course})

# New view for form topics
def form_topics(request, course_id, form_name):
	course = _get_course_by_id(course_id)
	if course:
		for division in course['divisions']:
			for form in division.get('forms', []):
				if slugify(form['form']) == slugify(form_name):
					return render(request, 'courses/form_topics.html', {
						'course': course,
						'division': division['name'],
						'form': form['form'],
						'topics': form['topics']
					})
	# fallback
	return render(request, 'courses/form_topics.html', {
		'course': {'id': course_id, 'title': f'Course {course_id}'},
		'division': '',
		'form': form_name,
		'topics': []
	})

def topic_notes(request, course_id, form_name, topic_slug):
	course = _get_course_by_id(course_id)
	if not course:
		return render(request, 'courses/notes_topic.html', {
			'course': {'id': course_id, 'title': f'Course {course_id}'},
			'form': form_name,
			'topic': topic_slug,
			'notes': _make_notes(topic_slug),
			'division': ''
		})
	found = _find_topic(course, form_name, topic_slug)
	if not found:
		return render(request, 'courses/notes_topic.html', {
			'course': course,
			'form': form_name,
			'topic': topic_slug,
			'notes': _make_notes(topic_slug),
			'division': ''
		})
	notes = _make_notes(found['topic'])
	return render(request, 'courses/notes_topic.html', {
		'course': course,
		'form': found['form'],
		'topic': found['topic'],
		'notes': notes,
		'division': found['division']
	})
