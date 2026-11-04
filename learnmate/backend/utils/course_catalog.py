"""
Course Catalog – curated free courses for all supported domains.
Used when building personalized roadmaps.
"""

COURSE_CATALOG: dict[str, dict] = {
    "Frontend Development": {
        "beginner": [
            {
                "title": "HTML & CSS for Beginners",
                "provider": "freeCodeCamp",
                "url": "https://www.freecodecamp.org/learn/responsive-web-design/",
                "duration_hours": 40,
                "topics": ["HTML5", "CSS3", "Flexbox", "Grid", "Responsive Design"],
                "is_free": True,
                "rating": 4.8,
                "description": "Complete intro to HTML and CSS with hands-on projects.",
            },
            {
                "title": "JavaScript Basics",
                "provider": "The Odin Project",
                "url": "https://www.theodinproject.com/paths/foundations/courses/foundations",
                "duration_hours": 30,
                "topics": ["JavaScript", "DOM", "Events", "ES6"],
                "is_free": True,
                "rating": 4.9,
            },
            {
                "title": "Intro to Web Development",
                "provider": "IBM SkillsBuild",
                "url": "https://skillsbuild.org/students/course-catalog",
                "duration_hours": 20,
                "topics": ["Web basics", "HTML", "CSS", "JavaScript fundamentals"],
                "is_free": True,
                "rating": 4.6,
            },
        ],
        "intermediate": [
            {
                "title": "React – The Complete Guide",
                "provider": "Coursera / Meta",
                "url": "https://www.coursera.org/professional-certificates/meta-front-end-developer",
                "duration_hours": 60,
                "topics": ["React", "Hooks", "State Management", "JSX", "APIs"],
                "is_free": False,
                "rating": 4.8,
            },
            {
                "title": "JavaScript Algorithms & Data Structures",
                "provider": "freeCodeCamp",
                "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/",
                "duration_hours": 35,
                "topics": ["Algorithms", "Data Structures", "ES6+", "OOP"],
                "is_free": True,
                "rating": 4.7,
            },
        ],
        "advanced": [
            {
                "title": "Advanced React Patterns",
                "provider": "Frontend Masters",
                "url": "https://frontendmasters.com/courses/advanced-react-patterns/",
                "duration_hours": 25,
                "topics": ["Advanced Hooks", "Context", "Performance", "TypeScript"],
                "is_free": False,
                "rating": 4.9,
            },
            {
                "title": "Next.js Full Stack",
                "provider": "Vercel / Next.js",
                "url": "https://nextjs.org/learn",
                "duration_hours": 20,
                "topics": ["Next.js", "SSR", "SSG", "API Routes"],
                "is_free": True,
                "rating": 4.8,
            },
        ],
    },
    "Cybersecurity": {
        "beginner": [
            {
                "title": "Introduction to Cybersecurity",
                "provider": "IBM SkillsBuild",
                "url": "https://skillsbuild.org/students/course-catalog/cybersecurity",
                "duration_hours": 20,
                "topics": ["CIA Triad", "Threats", "Vulnerabilities", "Basic Defense"],
                "is_free": True,
                "rating": 4.7,
            },
            {
                "title": "Cybersecurity Fundamentals",
                "provider": "edX / IBM",
                "url": "https://www.edx.org/learn/cybersecurity/ibm-cybersecurity-fundamentals",
                "duration_hours": 30,
                "topics": ["Network Security", "Encryption", "Firewalls", "Identity"],
                "is_free": True,
                "rating": 4.6,
            },
        ],
        "intermediate": [
            {
                "title": "Cybersecurity Analyst Professional Certificate",
                "provider": "Coursera / IBM",
                "url": "https://www.coursera.org/professional-certificates/ibm-cybersecurity-analyst",
                "duration_hours": 120,
                "topics": ["SIEM", "Threat Intelligence", "Incident Response", "Forensics"],
                "is_free": False,
                "rating": 4.8,
            },
            {
                "title": "Ethical Hacking Basics",
                "provider": "TryHackMe",
                "url": "https://tryhackme.com/path/outline/beginner",
                "duration_hours": 50,
                "topics": ["Penetration Testing", "OSINT", "Network Analysis"],
                "is_free": True,
                "rating": 4.9,
            },
        ],
        "advanced": [
            {
                "title": "Advanced Penetration Testing",
                "provider": "Offensive Security",
                "url": "https://www.offensive-security.com/pwk-oscp/",
                "duration_hours": 200,
                "topics": ["OSCP", "Exploit Development", "Buffer Overflow", "AD Attacks"],
                "is_free": False,
                "rating": 4.9,
            },
        ],
    },
    "UI/UX Design": {
        "beginner": [
            {
                "title": "Foundations of UX Design",
                "provider": "Coursera / Google",
                "url": "https://www.coursera.org/learn/foundations-user-experience-design",
                "duration_hours": 25,
                "topics": ["Design Thinking", "User Research", "Wireframing", "Accessibility"],
                "is_free": True,
                "rating": 4.8,
            },
            {
                "title": "Figma Basics for Beginners",
                "provider": "Figma",
                "url": "https://www.figma.com/resources/learn-design/",
                "duration_hours": 10,
                "topics": ["Figma", "Frames", "Components", "Prototyping"],
                "is_free": True,
                "rating": 4.7,
            },
        ],
        "intermediate": [
            {
                "title": "UX Research & Prototyping",
                "provider": "Coursera / Google",
                "url": "https://www.coursera.org/professional-certificates/google-ux-design",
                "duration_hours": 80,
                "topics": ["Usability Testing", "Information Architecture", "High-Fidelity Prototypes"],
                "is_free": False,
                "rating": 4.9,
            },
        ],
        "advanced": [
            {
                "title": "Advanced Interaction Design",
                "provider": "Interaction Design Foundation",
                "url": "https://www.interaction-design.org/courses",
                "duration_hours": 60,
                "topics": ["Design Systems", "Motion Design", "Advanced Figma"],
                "is_free": False,
                "rating": 4.8,
            },
        ],
    },
    "Data Science & ML": {
        "beginner": [
            {
                "title": "Data Science Fundamentals with Python",
                "provider": "IBM / edX",
                "url": "https://www.edx.org/professional-certificate/ibm-data-science",
                "duration_hours": 40,
                "topics": ["Python", "NumPy", "Pandas", "Matplotlib", "Statistics"],
                "is_free": True,
                "rating": 4.8,
            },
            {
                "title": "Machine Learning for Beginners",
                "provider": "Microsoft",
                "url": "https://github.com/microsoft/ML-For-Beginners",
                "duration_hours": 30,
                "topics": ["Supervised Learning", "Regression", "Classification", "Clustering"],
                "is_free": True,
                "rating": 4.7,
            },
        ],
        "intermediate": [
            {
                "title": "IBM AI Engineering Professional Certificate",
                "provider": "Coursera / IBM",
                "url": "https://www.coursera.org/professional-certificates/ai-engineer",
                "duration_hours": 120,
                "topics": ["Deep Learning", "TensorFlow", "PyTorch", "CNN", "NLP"],
                "is_free": False,
                "rating": 4.8,
            },
        ],
        "advanced": [
            {
                "title": "Applied AI with Deep Learning",
                "provider": "Coursera / IBM",
                "url": "https://www.coursera.org/learn/ai",
                "duration_hours": 80,
                "topics": ["Transformers", "LLMs", "Generative AI", "MLOps"],
                "is_free": False,
                "rating": 4.9,
            },
        ],
    },
    "Cloud & DevOps": {
        "beginner": [
            {
                "title": "Introduction to Cloud Computing",
                "provider": "Coursera / IBM",
                "url": "https://www.coursera.org/learn/introduction-to-cloud",
                "duration_hours": 20,
                "topics": ["Cloud Models", "IaaS", "PaaS", "SaaS", "IBM Cloud"],
                "is_free": True,
                "rating": 4.7,
            },
        ],
        "intermediate": [
            {
                "title": "IBM DevOps and Software Engineering",
                "provider": "Coursera / IBM",
                "url": "https://www.coursera.org/professional-certificates/devops-and-software-engineering",
                "duration_hours": 120,
                "topics": ["CI/CD", "Docker", "Kubernetes", "Git", "Agile"],
                "is_free": False,
                "rating": 4.8,
            },
        ],
        "advanced": [
            {
                "title": "Kubernetes & Cloud Native",
                "provider": "CNCF",
                "url": "https://www.cncf.io/certification/training/",
                "duration_hours": 60,
                "topics": ["Kubernetes Advanced", "Helm", "Service Mesh", "GitOps"],
                "is_free": True,
                "rating": 4.9,
            },
        ],
    },
    "Backend Development": {
        "beginner": [
            {
                "title": "Python for Everybody",
                "provider": "Coursera / University of Michigan",
                "url": "https://www.coursera.org/specializations/python",
                "duration_hours": 40,
                "topics": ["Python", "Data Structures", "Web Scraping", "Databases"],
                "is_free": True,
                "rating": 4.9,
            },
        ],
        "intermediate": [
            {
                "title": "APIs and Microservices",
                "provider": "freeCodeCamp",
                "url": "https://www.freecodecamp.org/learn/back-end-development-and-apis/",
                "duration_hours": 35,
                "topics": ["Node.js", "Express", "REST APIs", "MongoDB", "Auth"],
                "is_free": True,
                "rating": 4.7,
            },
        ],
        "advanced": [
            {
                "title": "System Design for Developers",
                "provider": "Educative",
                "url": "https://www.educative.io/path/scalability-system-design",
                "duration_hours": 50,
                "topics": ["Microservices", "Caching", "Load Balancing", "Databases at Scale"],
                "is_free": False,
                "rating": 4.8,
            },
        ],
    },
    "Mobile Development": {
        "beginner": [
            {
                "title": "Android Development for Beginners",
                "provider": "Google / Udacity",
                "url": "https://developer.android.com/courses/android-basics-compose/course",
                "duration_hours": 40,
                "topics": ["Kotlin", "Jetpack Compose", "Android Studio", "UI Basics"],
                "is_free": True,
                "rating": 4.7,
            },
        ],
        "intermediate": [
            {
                "title": "Flutter & Dart – Cross Platform",
                "provider": "Google",
                "url": "https://docs.flutter.dev/get-started",
                "duration_hours": 50,
                "topics": ["Flutter", "Dart", "Widgets", "State Management", "Firebase"],
                "is_free": True,
                "rating": 4.8,
            },
        ],
        "advanced": [
            {
                "title": "React Native Advanced",
                "provider": "Expo",
                "url": "https://docs.expo.dev/",
                "duration_hours": 40,
                "topics": ["React Native", "Native Modules", "Performance", "App Store Deployment"],
                "is_free": True,
                "rating": 4.7,
            },
        ],
    },
}


def get_courses_for_level(domain: str, level: str) -> list[dict]:
    """Return courses for a domain at a given skill level."""
    domain_catalog = COURSE_CATALOG.get(domain, {})
    return domain_catalog.get(level, [])


def get_all_courses_for_domain(domain: str) -> list[dict]:
    """Return all courses across all levels for a domain."""
    domain_catalog = COURSE_CATALOG.get(domain, {})
    all_courses = []
    for level_courses in domain_catalog.values():
        all_courses.extend(level_courses)
    return all_courses
