from django.core.management.base import BaseCommand
from candidates.models import Skill

SKILLS = [
    # Programming Languages
    "Python", "JavaScript", "Java", "C++", "C#", "C", "TypeScript", "PHP", "Ruby", "Go", "Rust",
    "Swift", "Kotlin", "Scala", "Clojure", "Haskell", "Erlang", "Elixir", "F#", "Dart", "R",
    "MATLAB", "Perl", "Lua", "Bash", "PowerShell", "VBA", "COBOL", "Fortran", "Ada", "Assembly",
    "Objective-C", "Groovy", "Julia", "Pascal", "Delphi", "Visual Basic", "ActionScript", "CoffeeScript",
    "Elm", "PureScript", "Reason", "OCaml", "Nim", "Crystal", "Zig", "V", "D", "Vala",
    
    # Web Development - Frontend
    "HTML", "CSS", "SCSS", "SASS", "Less", "Stylus", "React", "Vue.js", "Angular", "Svelte",
    "Next.js", "Nuxt.js", "Gatsby", "Ember.js", "Backbone.js", "jQuery", "Alpine.js", "Lit",
    "Stencil", "Preact", "Solid.js", "Qwik", "Astro", "Remix", "SvelteKit", "Vite", "Webpack",
    "Parcel", "Rollup", "esbuild", "Turbopack", "Babel", "PostCSS", "Tailwind CSS", "Bootstrap",
    "Bulma", "Material-UI", "Ant Design", "Chakra UI", "Semantic UI", "Foundation", "UIKit",
    
    # Web Development - Backend
    "Node.js", "Express.js", "Koa.js", "Fastify", "NestJS", "Django", "Flask", "FastAPI",
    "Spring Boot", "Spring Framework", "Hibernate", "ASP.NET", ".NET Core", "Laravel", "Symfony",
    "CodeIgniter", "CakePHP", "Zend Framework", "Ruby on Rails", "Sinatra", "Gin", "Echo",
    "Fiber", "Actix", "Rocket", "Warp", "Vapor", "Perfect", "Kitura", "Ktor", "Micronaut",
    
    # Mobile Development
    "React Native", "Flutter", "Ionic", "Xamarin", "PhoneGap", "Cordova", "Titanium", "Unity",
    "Android SDK", "iOS SDK", "Xcode", "Android Studio", "Kotlin Multiplatform", "NativeScript",
    "Expo", "Capacitor", "Quasar", "Framework7", "OnsenUI", "Mobile Angular UI",
    
    # Databases
    "SQL", "MySQL", "PostgreSQL", "SQLite", "Microsoft SQL Server", "Oracle Database", "IBM DB2",
    "MongoDB", "Cassandra", "Redis", "Elasticsearch", "Neo4j", "CouchDB", "DynamoDB", "Firebase",
    "Firestore", "RethinkDB", "InfluxDB", "TimescaleDB", "ClickHouse", "Apache Spark", "Hadoop",
    "HBase", "Amazon Redshift", "Google BigQuery", "Snowflake", "Databricks", "Apache Kafka",
    "RabbitMQ", "Apache Pulsar", "NATS", "ZeroMQ", "Apache ActiveMQ", "IBM MQ",
    
    # Cloud Platforms & Services
    "AWS", "Google Cloud Platform", "Microsoft Azure", "IBM Cloud", "Oracle Cloud", "Alibaba Cloud",
    "DigitalOcean", "Linode", "Vultr", "Heroku", "Netlify", "Vercel", "CloudFlare", "Fastly",
    "AWS Lambda", "Google Cloud Functions", "Azure Functions", "AWS S3", "Google Cloud Storage",
    "Azure Blob Storage", "AWS EC2", "Google Compute Engine", "Azure Virtual Machines",
    "AWS RDS", "Google Cloud SQL", "Azure SQL Database", "AWS DynamoDB", "Google Firestore",
    "Azure Cosmos DB", "AWS CloudFormation", "Terraform", "Ansible", "Chef", "Puppet",
    
    # DevOps & Infrastructure
    "Docker", "Kubernetes", "Jenkins", "GitLab CI/CD", "GitHub Actions", "Azure DevOps", "CircleCI",
    "Travis CI", "Bamboo", "TeamCity", "Octopus Deploy", "Spinnaker", "Argo CD", "Flux",
    "Helm", "Kustomize", "Istio", "Linkerd", "Consul", "Vault", "Nomad", "Packer", "Vagrant",
    "Apache", "Nginx", "HAProxy", "Traefik", "Envoy", "Kong", "Ambassador", "Istio Gateway",
    "Prometheus", "Grafana", "ELK Stack", "Splunk", "Datadog", "New Relic", "AppDynamics",
    
    # Version Control & Collaboration
    "Git", "GitHub", "GitLab", "Bitbucket", "Azure Repos", "Mercurial", "SVN", "Perforce",
    "Bazaar", "Fossil", "Darcs", "Monotone", "CVS", "SourceSafe", "Team Foundation Server",
    "Jira", "Confluence", "Trello", "Asana", "Monday.com", "Notion", "Slack", "Microsoft Teams",
    "Discord", "Zoom", "Google Meet", "Skype", "WebEx", "GoToMeeting",
    
    # Data Science & Analytics
    "Machine Learning", "Deep Learning", "Artificial Intelligence", "Neural Networks", "TensorFlow",
    "PyTorch", "Scikit-learn", "Keras", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly",
    "Jupyter", "Apache Zeppelin", "RStudio", "Tableau", "Power BI", "QlikView", "Looker",
    "Google Analytics", "Adobe Analytics", "Mixpanel", "Amplitude", "Segment", "Hotjar",
    "Data Mining", "Statistical Analysis", "Predictive Modeling", "Time Series Analysis",
    "Natural Language Processing", "Computer Vision", "Reinforcement Learning", "AutoML",
    
    # Cybersecurity
    "Cybersecurity", "Penetration Testing", "Ethical Hacking", "Vulnerability Assessment",
    "Security Auditing", "Incident Response", "Forensics", "Malware Analysis", "Risk Assessment",
    "Compliance", "GDPR", "HIPAA", "SOX", "PCI DSS", "ISO 27001", "NIST", "OWASP", "SANS",
    "Firewalls", "IDS/IPS", "SIEM", "Antivirus", "Encryption", "PKI", "SSL/TLS", "VPN",
    "Zero Trust", "Identity Management", "Access Control", "Multi-factor Authentication",
    
    # Design & UI/UX
    "UI Design", "UX Design", "User Research", "Wireframing", "Prototyping", "Information Architecture",
    "Interaction Design", "Visual Design", "Typography", "Color Theory", "Design Systems",
    "Accessibility", "Usability Testing", "A/B Testing", "Conversion Optimization", "Adobe XD",
    "Figma", "Sketch", "InVision", "Marvel", "Principle", "Framer", "Zeplin", "Abstract",
    "Adobe Creative Suite", "Photoshop", "Illustrator", "InDesign", "After Effects", "Premiere Pro",
    "Blender", "Maya", "3ds Max", "Cinema 4D", "SketchUp", "AutoCAD", "SolidWorks", "Fusion 360",
    
    # Digital Marketing
    "Digital Marketing", "SEO", "SEM", "Social Media Marketing", "Content Marketing", "Email Marketing",
    "Affiliate Marketing", "Influencer Marketing", "Marketing Automation", "Lead Generation",
    "Conversion Rate Optimization", "Google Ads", "Facebook Ads", "LinkedIn Ads", "Twitter Ads",
    "YouTube Marketing", "Instagram Marketing", "TikTok Marketing", "Pinterest Marketing",
    "Snapchat Marketing", "Reddit Marketing", "Quora Marketing", "Medium Publishing",
    "Content Strategy", "Copywriting", "Technical Writing", "Grant Writing", "Proposal Writing",
    
    # Project Management
    "Project Management", "Agile", "Scrum", "Kanban", "Waterfall", "Lean", "Six Sigma", "PRINCE2",
    "PMP", "PMI", "Risk Management", "Stakeholder Management", "Budget Management", "Resource Planning",
    "Timeline Management", "Quality Assurance", "Change Management", "Communication Management",
    "Microsoft Project", "Jira", "Trello", "Asana", "Monday.com", "Basecamp", "Smartsheet",
    "ClickUp", "Wrike", "Teamwork", "Zoho Projects", "ProofHub", "Workfront", "Clarizen",
    
    # Business & Finance
    "Business Analysis", "Financial Analysis", "Market Research", "Competitive Analysis",
    "Business Strategy", "Operations Management", "Supply Chain Management", "Inventory Management",
    "Customer Relationship Management", "Sales Management", "Account Management", "Negotiation",
    "Contract Management", "Vendor Management", "Procurement", "Cost Accounting", "Financial Modeling",
    "Budgeting", "Forecasting", "Investment Analysis", "Valuation", "Risk Management", "Compliance",
    "Audit", "Tax Preparation", "Bookkeeping", "Payroll", "QuickBooks", "SAP", "Oracle ERP",
    "Microsoft Dynamics", "NetSuite", "Salesforce", "HubSpot", "Pipedrive", "Zoho CRM",
    
    # Human Resources
    "Human Resources", "Talent Acquisition", "Recruiting", "Onboarding", "Training & Development",
    "Performance Management", "Compensation & Benefits", "Employee Relations", "HR Analytics",
    "Diversity & Inclusion", "Organizational Development", "Change Management", "Succession Planning",
    "Workforce Planning", "HRIS", "ATS", "Workday", "BambooHR", "ADP", "Paychex", "Kronos",
    "UltiPro", "SuccessFactors", "PeopleSoft", "Taleo", "Greenhouse", "Lever", "JazzHR",
    
    # Healthcare & Medical
    "Healthcare", "Medical Coding", "Clinical Research", "Pharmacy", "Nursing", "Physical Therapy",
    "Occupational Therapy", "Speech Therapy", "Radiology", "Laboratory", "Medical Devices",
    "Telemedicine", "Electronic Health Records", "HIPAA Compliance", "Medical Writing",
    "Epidemiology", "Biostatistics", "Public Health", "Health Informatics", "Medical Imaging",
    "Epic", "Cerner", "Allscripts", "Meditech", "NextGen", "Athenahealth", "eClinicalWorks",
    
    # Education & Training
    "Education", "Curriculum Development", "Instructional Design", "E-learning", "LMS",
    "Classroom Management", "Student Assessment", "Educational Technology", "Special Education",
    "ESL/EFL", "Adult Learning", "Corporate Training", "Professional Development", "Coaching",
    "Mentoring", "Public Speaking", "Presentation Skills", "Workshop Facilitation", "Webinar Hosting",
    "Moodle", "Blackboard", "Canvas", "Schoology", "Google Classroom", "Edmodo", "Seesaw",
    
    # Sales & Customer Service
    "Sales", "B2B Sales", "B2C Sales", "Inside Sales", "Outside Sales", "Account Management",
    "Lead Generation", "Cold Calling", "Email Outreach", "Social Selling", "Sales Presentations",
    "Closing Techniques", "Customer Service", "Technical Support", "Help Desk", "Live Chat",
    "Phone Support", "Email Support", "Ticketing Systems", "Customer Success", "Client Relations",
    "Zendesk", "Freshdesk", "ServiceNow", "Intercom", "Drift", "LiveChat", "Olark", "Tawk.to",
    
    # Manufacturing & Engineering
    "Manufacturing", "Quality Control", "Quality Assurance", "Lean Manufacturing", "Six Sigma",
    "Process Improvement", "Supply Chain", "Logistics", "Inventory Control", "Production Planning",
    "Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Chemical Engineering",
    "Industrial Engineering", "Aerospace Engineering", "Automotive Engineering", "Biomedical Engineering",
    "Environmental Engineering", "Materials Science", "Robotics", "Automation", "PLC Programming",
    "CAD", "CAM", "CNC", "3D Printing", "Additive Manufacturing", "Injection Molding", "Welding",
    
    # Legal & Compliance
    "Legal Research", "Contract Law", "Corporate Law", "Employment Law", "Intellectual Property",
    "Litigation", "Compliance", "Regulatory Affairs", "Legal Writing", "Paralegal", "Court Reporting",
    "Mediation", "Arbitration", "Legal Technology", "Case Management", "Document Review",
    "Due Diligence", "Patent Law", "Trademark Law", "Copyright Law", "Privacy Law", "Data Protection",
    "Westlaw", "LexisNexis", "Clio", "MyCase", "PracticePanther", "TimeSolv", "Legal Files",
    
    # Real Estate
    "Real Estate", "Property Management", "Real Estate Investment", "Commercial Real Estate",
    "Residential Real Estate", "Property Valuation", "Market Analysis", "Real Estate Finance",
    "Property Development", "Construction Management", "Architecture", "Interior Design",
    "Landscape Architecture", "Urban Planning", "Zoning", "Building Codes", "Permits", "Inspections",
    "MLS", "CRM", "Transaction Management", "Lead Generation", "Real Estate Marketing",
    
    # Retail & E-commerce
    "Retail", "E-commerce", "Online Store Management", "Inventory Management", "Product Management",
    "Category Management", "Merchandising", "Visual Merchandising", "Store Operations", "POS Systems",
    "Payment Processing", "Shipping & Fulfillment", "Customer Service", "Returns Management",
    "Amazon FBA", "eBay", "Etsy", "Shopify", "WooCommerce", "Magento", "BigCommerce", "Squarespace",
    "Wix", "PrestaShop", "OpenCart", "Zen Cart", "osCommerce", "X-Cart", "CS-Cart",
    
    # Hospitality & Tourism
    "Hospitality", "Hotel Management", "Restaurant Management", "Event Planning", "Catering",
    "Food Service", "Tourism", "Travel Planning", "Tour Operations", "Cruise Operations",
    "Resort Management", "Spa Management", "Recreation Management", "Guest Services", "Concierge",
    "Front Office", "Housekeeping", "Food & Beverage", "Revenue Management", "Yield Management",
    "Opera PMS", "Micros", "OpenTable", "Resy", "Tock", "Yelp", "TripAdvisor", "Expedia",
    
    # Transportation & Logistics
    "Transportation", "Logistics", "Supply Chain Management", "Freight Management", "Shipping",
    "Warehousing", "Distribution", "Fleet Management", "Route Optimization", "Inventory Control",
    "Customs", "Import/Export", "International Trade", "Compliance", "Safety", "DOT Regulations",
    "CDL", "Truck Driving", "Delivery", "Courier Services", "Last Mile Delivery", "Cross Docking",
    "TMS", "WMS", "ERP", "SAP", "Oracle", "Manhattan Associates", "JDA", "Blue Yonder",
    
    # Agriculture & Food
    "Agriculture", "Farming", "Crop Management", "Livestock Management", "Precision Agriculture",
    "Organic Farming", "Sustainable Agriculture", "Hydroponics", "Aquaponics", "Greenhouse Management",
    "Food Science", "Food Safety", "HACCP", "FDA Regulations", "USDA Regulations", "Food Processing",
    "Food Manufacturing", "Quality Control", "Nutrition", "Dietetics", "Food Service", "Culinary Arts",
    "Recipe Development", "Menu Planning", "Cost Control", "Kitchen Management", "Restaurant Operations",
    
    # Energy & Utilities
    "Energy", "Oil & Gas", "Renewable Energy", "Solar Energy", "Wind Energy", "Hydroelectric",
    "Nuclear Energy", "Energy Efficiency", "Sustainability", "Environmental Science", "Utilities",
    "Power Generation", "Power Distribution", "Grid Management", "Smart Grid", "Energy Storage",
    "Electric Vehicles", "Charging Infrastructure", "Carbon Trading", "Environmental Compliance",
    "SCADA", "GIS", "Asset Management", "Maintenance Planning", "Outage Management", "Load Forecasting",
    
    # Media & Entertainment
    "Media", "Entertainment", "Film Production", "Video Production", "Audio Production", "Broadcasting",
    "Journalism", "Editing", "Copywriting", "Scriptwriting", "Screenwriting", "Content Creation",
    "Social Media", "Influencer Marketing", "Brand Management", "Public Relations", "Crisis Management",
    "Event Management", "Talent Management", "Artist Management", "Music Production", "Sound Engineering",
    "Live Events", "Concert Production", "Theater Production", "Game Development", "Animation",
    
    # Gaming & Interactive Media
    "Game Development", "Game Design", "Level Design", "Character Design", "Game Programming",
    "Unity", "Unreal Engine", "Godot", "GameMaker", "Construct", "RPG Maker", "Twine", "Ink",
    "C# Unity", "C++ Unreal", "Lua", "Python Pygame", "JavaScript Phaser", "Java LibGDX",
    "Mobile Game Development", "Console Game Development", "PC Game Development", "VR Development",
    "AR Development", "Mixed Reality", "3D Modeling", "Texturing", "Rigging", "Animation",
    "Sound Design", "Music Composition", "Voice Acting", "Localization", "QA Testing", "User Research",
    
    # Sports & Fitness
    "Sports", "Fitness", "Personal Training", "Group Fitness", "Yoga", "Pilates", "CrossFit",
    "Martial Arts", "Swimming", "Running", "Cycling", "Weightlifting", "Cardio", "Strength Training",
    "Nutrition", "Sports Medicine", "Physical Therapy", "Athletic Training", "Coaching", "Sports Psychology",
    "Sports Management", "Recreation", "Outdoor Activities", "Adventure Sports", "Team Sports",
    "Individual Sports", "Youth Sports", "Adaptive Sports", "Sports Marketing", "Sports Broadcasting",
    
    # Arts & Crafts
    "Art", "Drawing", "Painting", "Sculpture", "Pottery", "Ceramics", "Woodworking", "Metalworking",
    "Jewelry Making", "Textile Arts", "Sewing", "Knitting", "Crocheting", "Embroidery", "Quilting",
    "Leatherworking", "Glassblowing", "Printmaking", "Photography", "Digital Art", "Illustration",
    "Graphic Design", "Web Design", "Logo Design", "Branding", "Layout Design", "Publication Design",
    "Packaging Design", "Motion Graphics", "Video Editing", "Audio Editing", "Music Production",
    
    # Languages & Communication
    "English", "Spanish", "French", "German", "Italian", "Portuguese", "Dutch", "Russian", "Chinese",
    "Japanese", "Korean", "Arabic", "Hindi", "Bengali", "Urdu", "Turkish", "Polish", "Czech",
    "Hungarian", "Romanian", "Bulgarian", "Croatian", "Serbian", "Slovak", "Slovenian", "Estonian",
    "Latvian", "Lithuanian", "Finnish", "Swedish", "Norwegian", "Danish", "Icelandic", "Greek",
    "Hebrew", "Thai", "Vietnamese", "Indonesian", "Malay", "Tagalog", "Swahili", "Amharic",
    "Translation", "Interpretation", "Localization", "Technical Writing", "Creative Writing",
    "Copywriting", "Content Writing", "Blogging", "Journalism", "Public Speaking", "Presentation",
    
    # Science & Research
    "Research", "Scientific Writing", "Data Analysis", "Statistical Analysis", "Experimental Design",
    "Laboratory Techniques", "Microscopy", "Spectroscopy", "Chromatography", "Electrophoresis",
    "Cell Culture", "Molecular Biology", "Genetics", "Biochemistry", "Microbiology", "Immunology",
    "Pharmacology", "Toxicology", "Pathology", "Anatomy", "Physiology", "Neuroscience", "Psychology",
    "Behavioral Science", "Cognitive Science", "Social Science", "Anthropology", "Sociology",
    "Political Science", "Economics", "Geography", "History", "Archaeology", "Paleontology",
    
    # Mathematics & Statistics
    "Mathematics", "Algebra", "Calculus", "Geometry", "Trigonometry", "Statistics", "Probability",
    "Linear Algebra", "Differential Equations", "Number Theory", "Graph Theory", "Topology",
    "Mathematical Modeling", "Operations Research", "Optimization", "Game Theory", "Cryptography",
    "Actuarial Science", "Financial Mathematics", "Econometrics", "Biostatistics", "Psychometrics",
    "Quality Control", "Six Sigma", "Lean", "Process Improvement", "Data Mining", "Machine Learning",
    "Artificial Intelligence", "Deep Learning", "Neural Networks", "Computer Vision", "NLP",
    
    # Philosophy & Ethics
    "Philosophy", "Ethics", "Logic", "Metaphysics", "Epistemology", "Aesthetics", "Political Philosophy",
    "Philosophy of Mind", "Philosophy of Science", "Philosophy of Religion", "Applied Ethics",
    "Medical Ethics", "Business Ethics", "Environmental Ethics", "Bioethics", "Computer Ethics",
    "AI Ethics", "Data Ethics", "Research Ethics", "Publication Ethics", "Academic Ethics",
    "Professional Ethics", "Legal Ethics", "Journalism Ethics", "Media Ethics", "Social Responsibility",
    
    # Personal Development
    "Leadership", "Management", "Team Building", "Communication", "Negotiation", "Conflict Resolution",
    "Problem Solving", "Critical Thinking", "Decision Making", "Time Management", "Stress Management",
    "Emotional Intelligence", "Self-Awareness", "Motivation", "Goal Setting", "Planning", "Organization",
    "Productivity", "Efficiency", "Innovation", "Creativity", "Adaptability", "Resilience",
    "Networking", "Relationship Building", "Mentoring", "Coaching", "Training", "Public Speaking",
    "Presentation Skills", "Writing Skills", "Reading Comprehension", "Active Listening", "Empathy",
    
    # Emerging Technologies
    "Blockchain", "Cryptocurrency", "NFT", "DeFi", "Smart Contracts", "Web3", "Metaverse",
    "Virtual Reality", "Augmented Reality", "Mixed Reality", "Internet of Things", "5G", "Edge Computing",
    "Quantum Computing", "Quantum Cryptography", "Bioinformatics", "Computational Biology",
    "Digital Twins", "Robotic Process Automation", "Chatbots", "Voice Assistants", "Computer Vision",
    "Autonomous Vehicles", "Drones", "3D Printing", "Nanotechnology", "Biotechnology", "Gene Editing",
    "CRISPR", "Synthetic Biology", "Regenerative Medicine", "Precision Medicine", "Personalized Medicine",
    
    # Soft Skills
    "Communication", "Leadership", "Teamwork", "Problem Solving", "Critical Thinking", "Creativity",
    "Adaptability", "Time Management", "Organization", "Attention to Detail", "Multitasking",
    "Prioritization", "Decision Making", "Analytical Thinking", "Strategic Thinking", "Innovation",
    "Collaboration", "Interpersonal Skills", "Customer Service", "Sales", "Negotiation", "Persuasion",
    "Presentation", "Public Speaking", "Writing", "Research", "Planning", "Project Management",
    "Change Management", "Conflict Resolution", "Emotional Intelligence", "Cultural Awareness",
    "Diversity and Inclusion", "Mentoring", "Coaching", "Training", "Delegation", "Motivation",
    
    # Industry-Specific Skills
    "Aerospace", "Automotive", "Banking", "Biotechnology", "Construction", "Consulting", "Education",
    "Energy", "Entertainment", "Fashion", "Finance", "Government", "Healthcare", "Hospitality",
    "Insurance", "Legal", "Manufacturing", "Media", "Non-profit", "Pharmaceuticals", "Real Estate",
    "Retail", "Technology", "Telecommunications", "Transportation", "Utilities", "Venture Capital",
    "Private Equity", "Investment Banking", "Asset Management", "Hedge Funds", "Insurance", "Actuarial",
    "Risk Management", "Compliance", "Audit", "Tax", "Accounting", "Bookkeeping", "Payroll", "HR",
    
    # Tools & Software (Additional)
    "Microsoft Office", "Excel", "Word", "PowerPoint", "Outlook", "OneNote", "Teams", "SharePoint",
    "Google Workspace", "Gmail", "Google Drive", "Google Docs", "Google Sheets", "Google Slides",
    "Zoom", "Slack", "Discord", "Skype", "WhatsApp", "Telegram", "Signal", "Dropbox", "Box",
    "OneDrive", "iCloud", "Adobe Acrobat", "PDF", "Canva", "GIMP", "Inkscape", "Audacity",
    "OBS Studio", "Camtasia", "ScreenFlow", "Loom", "Snagit", "Notion", "Obsidian", "Roam Research",
    "Evernote", "Bear", "Apple Notes", "Google Keep", "Todoist", "Any.do", "Wunderlist", "Trello"
]

class Command(BaseCommand):
    help = "Seed predefined skills into the database"

    def handle(self, *args, **kwargs):
        created = 0
        for skill in SKILLS:
            obj, was_created = Skill.objects.get_or_create(name=skill)
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f"{created} skills seeded successfully."))
