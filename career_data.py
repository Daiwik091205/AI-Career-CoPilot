"""
career_data.py
Dataset of target careers and their industry-standard technical requirements.
Designed for easy expansion with structured attributes.
"""

CAREERS = {
    "Software Developer": {
        "title": "Software Developer",
        "domain": "Software Engineering",
        "description": "Designs, develops, tests, and maintains software applications and scalable backend systems.",
        "required_skills": [
            "Data Structures & Algorithms",
            "Python",
            "Java",
            "Object-Oriented Programming (OOP)",
            "Relational Databases (SQL)",
            "Git & Version Control",
            "REST APIs",
            "Operating Systems & Multithreading",
            "Computer Networks",
            "Unit Testing"
        ],
        "recommended_skills": [
            "Docker",
            "Microservices Architecture",
            "CI/CD Pipelines",
            "System Design Basics",
            "NoSQL Databases"
        ],
        "key_interview_topics": [
            "DSA (Arrays, Trees, Graphs, DP)",
            "OOP Concepts (Polymorphism, Inheritance)",
            "DBMS (Indexing, Transactions, Normalization)",
            "Operating Systems (Process vs Thread, Deadlocks)",
            "Computer Networks (TCP/IP, HTTP/HTTPS)"
        ],
        "recommended_project_ideas": [
            "Full-Stack Web Application with JWT Authentication and CRUD operations",
            "Distributed URL Shortener with Caching (Redis) and Rate Limiting",
            "Real-time Chat Application using WebSockets and Async Python"
        ]
    },
    "Data Scientist": {
        "title": "Data Scientist",
        "domain": "Data & AI",
        "description": "Extracts actionable insights from structured and unstructured data using statistical modeling and machine learning.",
        "required_skills": [
            "Python",
            "SQL & Database Querying",
            "Pandas & NumPy",
            "Exploratory Data Analysis (EDA)",
            "Applied Statistics & Probability",
            "Machine Learning (Scikit-Learn)",
            "Data Visualization (Matplotlib, Seaborn)",
            "Feature Engineering",
            "Hypothesis Testing"
        ],
        "recommended_skills": [
            "Big Data (PySpark)",
            "Tableau or Power BI",
            "Time Series Forecasting",
            "MLflow",
            "Cloud Data Warehouses (BigQuery/Snowflake)"
        ],
        "key_interview_topics": [
            "Supervised vs Unsupervised Algorithms",
            "Bias-Variance Tradeoff & Overfitting Prevention",
            "Statistical Significance, p-values, A/B Testing",
            "SQL Queries (Window functions, JOINs, Group By)",
            "Evaluation Metrics (ROC-AUC, Precision/Recall, F1)"
        ],
        "recommended_project_ideas": [
            "Customer Churn Prediction with Feature Importance & Cost Analysis",
            "E-commerce Sales Forecasting using Time-Series Analysis",
            "Automated Exploratory Data Analysis & Reporting Dashboard"
        ]
    },
    "Machine Learning Engineer": {
        "title": "Machine Learning Engineer",
        "domain": "Data & AI",
        "description": "Researches, builds, and deploys scalable machine learning models into production software pipelines.",
        "required_skills": [
            "Python",
            "Data Structures & Algorithms",
            "Scikit-Learn",
            "PyTorch or TensorFlow",
            "Deep Learning Fundamentals",
            "Model Deployment (FastAPI/Flask)",
            "Docker & Containerization",
            "Data Preprocessing & Pipelines",
            "SQL",
            "Git & Version Control"
        ],
        "recommended_skills": [
            "MLOps (MLflow, DVC, Kubeflow)",
            "ONNX / TensorRT Model Optimization",
            "Cloud Platforms (AWS SageMaker / GCP Vertex)",
            "Distributed Training",
            "Computer Vision or NLP"
        ],
        "key_interview_topics": [
            "Loss Functions & Gradient Descent Optimization",
            "Model Serving & Latency Optimization",
            "Data Leakage and Cross-Validation Strategies",
            "Deep Learning Architectures (CNNs, RNNs, Transformers)",
            "ML System Design (Recommendation systems, Search ranking)"
        ],
        "recommended_project_ideas": [
            "End-to-End Image Classification API with PyTorch, Docker, and FastAPI",
            "Real-Time Sentiment Analysis Pipeline with Model Versioning (MLflow)",
            "Production Recommendation System deployed with CI/CD"
        ]
    },
    "AI Engineer": {
        "title": "AI Engineer",
        "domain": "Data & AI",
        "description": "Develops generative AI, LLM applications, retrieval-augmented systems, and autonomous agent workflows.",
        "required_skills": [
            "Python",
            "Large Language Models (LLMs) & Prompt Engineering",
            "LangChain / LlamaIndex",
            "Vector Databases (Chroma, Pinecone, FAISS)",
            "Retrieval-Augmented Generation (RAG)",
            "REST APIs & Web Frameworks",
            "Embeddings & Semantic Search",
            "Git & Version Control",
            "Basic PyTorch"
        ],
        "recommended_skills": [
            "Fine-Tuning LLMs (LoRA/QLoRA)",
            "Agentic Workflows & Multi-Agent Frameworks",
            "Evaluation Frameworks (Ragas, TruLens)",
            "Docker & Cloud Deployment",
            "Knowledge Graphs"
        ],
        "key_interview_topics": [
            "RAG Architecture & Chunking / Embedding Strategies",
            "Prompt Injection, Guardrails, and Hallucination Mitigation",
            "Context Window Management & Attention Mechanisms",
            "Vector Indexing (HNSW, Cosine vs Dot Product)",
            "Agent Tool Calling and Memory Systems"
        ],
        "recommended_project_ideas": [
            "Domain-Specific RAG QA Chatbot with Hybrid Search and Citations",
            "Autonomous Research Agent with Web Browsing and Report Generation",
            "Multi-modal Document Parser & Semantic Summarizer using LLMs"
        ]
    },
    "Data Analyst": {
        "title": "Data Analyst",
        "domain": "Data & Analytics",
        "description": "Interprets data, analyzes results, builds dashboards, and delivers business intelligence reports to stakeholders.",
        "required_skills": [
            "SQL (Advanced Queries, Aggregations, Window Functions)",
            "Microsoft Excel (VLOOKUP, Pivot Tables, Formulas)",
            "Data Visualization (Power BI or Tableau)",
            "Python or R for Analytics",
            "Pandas & Data Cleaning",
            "Business Acumen & Storytelling",
            "Basic Descriptive Statistics"
        ],
        "recommended_skills": [
            "Data Warehousing Concepts",
            "ETL Pipelines",
            "Google Analytics / Product Analytics",
            "Stakeholder Presentation",
            "Git"
        ],
        "key_interview_topics": [
            "Complex SQL Joins, Subqueries, and Aggregate Functions",
            "Key Business Metrics (CAC, LTV, Retention, Churn)",
            "Dashboard Design Principles & User Experience",
            "Handling Missing Data and Outlier Treatment",
            "Data-Driven Problem Solving Scenarios"
        ],
        "recommended_project_ideas": [
            "Interactive Executive Financial Dashboard in Power BI/Tableau",
            "E-commerce Customer Cohort and Retention Analysis in SQL & Python",
            "Healthcare Operational Efficiency Analysis with Executive Summary"
        ]
    },
    "Cybersecurity Analyst": {
        "title": "Cybersecurity Analyst",
        "domain": "Security & Infrastructure",
        "description": "Protects computer systems, networks, and data from cyber attacks, vulnerabilities, and unauthorized access.",
        "required_skills": [
            "Computer Networking (TCP/IP, DNS, Firewalls, VPNs)",
            "Operating Systems (Linux & Windows Administration)",
            "Network Security & Packet Analysis (Wireshark)",
            "Security Information & Event Management (SIEM)",
            "Vulnerability Assessment & Penetration Testing Basics",
            "Information Security Principles (CIA Triad, Least Privilege)",
            "Python or Bash Scripting for Automation"
        ],
        "recommended_skills": [
            "Incident Response & Forensics",
            "OWASP Top 10 Web Vulnerabilities",
            "Cloud Security (AWS/Azure Security Groups)",
            "Cryptography Basics",
            "Compliance Frameworks (NIST, ISO 27001)"
        ],
        "key_interview_topics": [
            "Common Cyber Attacks (Phishing, MITM, DDoS, SQL Injection)",
            "Incident Response Lifecycle (Identification to Remediation)",
            "Firewalls, IDS vs IPS, and Zero Trust Architecture",
            "PKI, Symmetric vs Asymmetric Encryption, SSL/TLS",
            "Log Analysis and Threat Hunting Scenarios"
        ],
        "recommended_project_ideas": [
            "Network Intrusion Detection System Lab with Snort/Suricata",
            "Automated Vulnerability Scanner Script using Python and Nmap",
            "SIEM Log Analysis Dashboard simulating Threat Detection (Splunk/ELK)"
        ]
    },
    "Cloud Engineer": {
        "title": "Cloud Engineer",
        "domain": "Infrastructure & Cloud",
        "description": "Architects, deploys, and maintains cloud infrastructure and services on major cloud service providers.",
        "required_skills": [
            "Cloud Provider Fundamentals (AWS, Azure, or GCP)",
            "Linux System Administration & Shell Scripting",
            "Computer Networking in Cloud (VPC, Subnets, Route Tables)",
            "Infrastructure as Code (Terraform or CloudFormation)",
            "Containerization (Docker)",
            "Identity & Access Management (IAM)",
            "Python or Go for Cloud Scripting"
        ],
        "recommended_skills": [
            "Kubernetes Fundamentals",
            "Serverless Architecture (AWS Lambda / Cloud Functions)",
            "Cloud Cost Optimization",
            "Cloud Monitoring (Prometheus, Grafana, CloudWatch)",
            "CI/CD Integration"
        ],
        "key_interview_topics": [
            "Cloud Service Models (IaaS, PaaS, SaaS) and Shared Responsibility",
            "VPC Peering, NAT Gateways, and Security Groups vs NACLs",
            "High Availability, Fault Tolerance, and Auto-scaling",
            "Terraform State Management and Declarative Infrastructure",
            "Storage Types (Block, Object, File Storage)"
        ],
        "recommended_project_ideas": [
            "Automated Multi-Tier AWS/GCP Infrastructure Deployment with Terraform",
            "Serverless Event-Driven Image Processing Pipeline",
            "High-Availability Containerized Web App with Load Balancing"
        ]
    },
    "DevOps Engineer": {
        "title": "DevOps Engineer",
        "domain": "Infrastructure & Cloud",
        "description": "Bridges software development and IT operations using automation, continuous integration, and continuous delivery.",
        "required_skills": [
            "Linux Administration & Bash Scripting",
            "Git & Branching Strategies",
            "CI/CD Pipelines (GitHub Actions / Jenkins / GitLab CI)",
            "Docker & Container Management",
            "Kubernetes Orchestration Basics",
            "Infrastructure as Code (Terraform / Ansible)",
            "Monitoring & Logging (Prometheus, Grafana, ELK)",
            "Python or Go Scripting"
        ],
        "recommended_skills": [
            "GitOps (ArgoCD)",
            "Service Mesh (Istio)",
            "Site Reliability Engineering (SRE) Principles (SLI/SLO/SLA)",
            "Security in DevOps (DevSecOps)",
            "Cloud Infrastructure (AWS/Azure)"
        ],
        "key_interview_topics": [
            "CI/CD Pipeline Stages, Testing, and Deployment Strategies (Blue-Green, Canary)",
            "Docker Container Lifecycle, Layers, and Multi-stage Builds",
            "Kubernetes Core Objects (Pods, Deployments, Services, Ingress)",
            "Monitoring, Alerting Thresholds, and Incident Post-mortems",
            "Configuration Management vs Infrastructure as Code"
        ],
        "recommended_project_ideas": [
            "Complete CI/CD Pipeline with GitHub Actions, Docker, and Automated Tests",
            "Kubernetes Cluster Deployment with Helm Charts and Ingress Controller",
            "Full Observability Stack with Prometheus, Grafana, and Alertmanager"
        ]
    }
}

def get_all_careers():
    """Return dictionary of all available careers."""
    return CAREERS

def get_career_names():
    """Return sorted list of career names."""
    return sorted(list(CAREERS.keys()))

def get_career(career_name):
    """Return career details dictionary or None if not found."""
    return CAREERS.get(career_name)
