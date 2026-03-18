from django.core.management.base import BaseCommand
from courses.models import Course, Topic, Lesson

class Command(BaseCommand):
    help = 'Populate initial course data'

    def handle(self, *args, **options):
        self.stdout.write('Creating initial courses...')

        # Create Mathematics course
        math_course = Course.objects.create(
            title='Mathematics',
            description='Mathematics for O-Level (Form 1-4) and Advanced (Form 5-6). Complete coverage of algebra, geometry, calculus, and statistics.',
            code='MATH',
            level='o_level'
        )

        # Create topics for Mathematics
        topics_data = [
            ('form1', 'Numbers', 'Understanding number systems, operations, and basic arithmetic'),
            ('form1', 'Algebra', 'Introduction to algebraic expressions and equations'),
            ('form1', 'Geometry', 'Basic shapes, angles, and measurements'),
            ('form2', 'Sets', 'Set theory and operations'),
            ('form2', 'Statistics', 'Data collection, representation, and basic analysis'),
            ('form3', 'Trigonometry', 'Trigonometric ratios and identities'),
            ('form3', 'Vectors', 'Vector operations and applications'),
            ('form4', 'Calculus', 'Introduction to differentiation and integration'),
            ('form4', 'Probability', 'Probability concepts and calculations'),
        ]

        for form, title, description in topics_data:
            topic = Topic.objects.create(
                course=math_course,
                title=title,
                description=description,
                form=form,
                order=topics_data.index((form, title, description)) + 1
            )

            # Create sample lessons for each topic
            Lesson.objects.create(
                topic=topic,
                title=f'Introduction to {title}',
                content=f'This lesson introduces the fundamental concepts of {title.lower()}. {description}',
                objectives=f'By the end of this lesson, students will be able to understand basic {title.lower()} concepts.',
                order=1
            )

        # Create Physics course
        physics_course = Course.objects.create(
            title='Physics',
            description='Physics for O-Level (Form 1-4) and Advanced (Form 5-6). Covering mechanics, electricity, magnetism, and modern physics.',
            code='PHYS',
            level='o_level'
        )

        physics_topics = [
            ('form1', 'Measurement', 'Units, measurements, and scientific notation'),
            ('form1', 'Motion', 'Distance, displacement, speed, and velocity'),
            ('form2', 'Forces', 'Types of forces and Newton\'s laws'),
            ('form2', 'Energy', 'Work, power, and energy conservation'),
            ('form3', 'Electricity', 'Current, voltage, and resistance'),
            ('form3', 'Magnetism', 'Magnetic fields and electromagnetic induction'),
            ('form4', 'Waves', 'Wave properties and sound'),
            ('form4', 'Light', 'Reflection, refraction, and optics'),
        ]

        for form, title, description in physics_topics:
            topic = Topic.objects.create(
                course=physics_course,
                title=title,
                description=description,
                form=form,
                order=physics_topics.index((form, title, description)) + 1
            )

            Lesson.objects.create(
                topic=topic,
                title=f'Introduction to {title}',
                content=f'This lesson covers the fundamental principles of {title.lower()}. {description}',
                objectives=f'By the end of this lesson, students will understand {title.lower()} concepts.',
                order=1
            )

        # Create Chemistry course
        chemistry_course = Course.objects.create(
            title='Chemistry',
            description='Chemistry for O-Level (Form 1-4) and Advanced (Form 5-6). Organic and inorganic chemistry, laboratory techniques.',
            code='CHEM',
            level='o_level'
        )

        chemistry_topics = [
            ('form1', 'Matter', 'States of matter and physical properties'),
            ('form1', 'Atoms', 'Atomic structure and periodic table'),
            ('form2', 'Chemical Reactions', 'Types of reactions and balancing equations'),
            ('form2', 'Acids and Bases', 'pH, neutralization, and indicators'),
            ('form3', 'Organic Chemistry', 'Carbon compounds and functional groups'),
            ('form3', 'Electrochemistry', 'Redox reactions and electrolysis'),
            ('form4', 'Chemical Equilibrium', 'Equilibrium constants and Le Chatelier\'s principle'),
            ('form4', 'Environmental Chemistry', 'Pollution and environmental impact'),
        ]

        for form, title, description in chemistry_topics:
            topic = Topic.objects.create(
                course=chemistry_course,
                title=title,
                description=description,
                form=form,
                order=chemistry_topics.index((form, title, description)) + 1
            )

            Lesson.objects.create(
                topic=topic,
                title=f'Introduction to {title}',
                content=f'This lesson explores {title.lower()}. {description}',
                objectives=f'Students will learn about {title.lower()} concepts.',
                order=1
            )

        # Create Biology course
        biology_course = Course.objects.create(
            title='Biology',
            description='Biology for O-Level (Form 1-4) and Advanced (Form 5-6). Cell biology, genetics, ecology, and human physiology.',
            code='BIO',
            level='o_level'
        )

        biology_topics = [
            ('form1', 'Cell Biology', 'Cell structure and function'),
            ('form1', 'Classification', 'Classification of living organisms'),
            ('form2', 'Nutrition', 'Photosynthesis, digestion, and nutrition'),
            ('form2', 'Respiration', 'Aerobic and anaerobic respiration'),
            ('form3', 'Ecology', 'Ecosystems, food chains, and environmental issues'),
            ('form3', 'Genetics', 'Inheritance and genetic variation'),
            ('form4', 'Human Physiology', 'Human body systems and homeostasis'),
            ('form4', 'Evolution', 'Theories of evolution and natural selection'),
        ]

        for form, title, description in biology_topics:
            topic = Topic.objects.create(
                course=biology_course,
                title=title,
                description=description,
                form=form,
                order=biology_topics.index((form, title, description)) + 1
            )

            Lesson.objects.create(
                topic=topic,
                title=f'Introduction to {title}',
                content=f'This lesson covers {title.lower()}. {description}',
                objectives=f'Students will understand {title.lower()} principles.',
                order=1
            )

        self.stdout.write(self.style.SUCCESS('Successfully created initial course data'))