from django.shortcuts import render

def course_list(request):
    # Accurate course list with specific links for each course
    courses = [
        {
            'id': 1,
            'title': 'Mathematics',
            'description': 'Mathematics for O-Level (Form 1-4) and Advanced (Form 5-6) based on the TIE curriculum.',
            'detail_url': 'course_detail',
        },
        {
            'id': 2,
            'title': 'English',
            'description': 'Improve your English skills.',
            'detail_url': 'course_detail',
        },
        {
            'id': 3,
            'title': 'Science',
            'description': 'Explore the world of science.',
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

def course_detail(request, course_id):
	if int(course_id) == 1:
		course = get_mathematics_course()
	elif int(course_id) == 2:
		course = {'id': 2, 'title': 'English', 'description': 'Improve your English skills.'}
	elif int(course_id) == 3:
		course = {'id': 3, 'title': 'Science', 'description': 'Explore the world of science.'}
	else:
		course = {'id': course_id, 'title': f'Course {course_id}', 'description': 'Course details here.'}
	return render(request, 'courses/course_detail.html', {'course': course})

# New view for form topics
def form_topics(request, course_id, form_name):
	if int(course_id) == 1:
		course = get_mathematics_course()
		for division in course['divisions']:
			for form in division.get('forms', []):
				if form['form'].replace(' ', '').lower() == form_name.replace(' ', '').lower():
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
from django.shortcuts import render

# Create your views here.
