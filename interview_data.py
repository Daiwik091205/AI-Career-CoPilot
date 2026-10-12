"""
interview_data.py
Curated question bank for Technical and HR/Behavioral interviews.
Includes questions mapped to career domains and core CS fundamentals.
"""

TECHNICAL_CATEGORIES = [
    "Programming",
    "DSA",
    "DBMS",
    "Operating Systems",
    "Computer Networks",
    "OOP",
    "AI/ML"
]

BEHAVIORAL_CATEGORIES = [
    "Tell Me About Yourself",
    "Strengths & Weaknesses",
    "Projects & Challenges",
    "Teamwork & Collaboration",
    "Conflict Resolution",
    "Leadership & Ownership",
    "Career Goals & Motivation"
]

# Question bank
INTERVIEW_QUESTIONS = [
    # --- TECHNICAL: PROGRAMMING & OOP ---
    {
        "id": "tech_oop_01",
        "type": "Technical",
        "category": "OOP",
        "relevant_careers": ["Software Developer", "Machine Learning Engineer", "DevOps Engineer"],
        "question": "Explain the four pillars of Object-Oriented Programming (OOP) with real-world examples.",
        "difficulty": "Easy",
        "key_points_to_cover": [
            "Encapsulation (bundling data and methods, data hiding)",
            "Abstraction (hiding complex implementation, exposing clean interface)",
            "Inheritance (code reuse, subclassing)",
            "Polymorphism (method overloading and overriding)"
        ],
        "sample_good_answer": "The four pillars are: 1) Encapsulation - bundling data with methods that operate on it, such as private attributes accessed via getters/setters in a BankAccount class. 2) Abstraction - showing only essential details to the user, like a car's accelerator pedal without revealing fuel injection mechanics. 3) Inheritance - allowing a derived class like ElectricCar to inherit attributes from a base Vehicle class. 4) Polymorphism - the ability of different classes to respond to the same method call, such as a draw() method acting differently on Circle vs Rectangle."
    },
    {
        "id": "tech_prog_01",
        "type": "Technical",
        "category": "Programming",
        "relevant_careers": ["Software Developer", "Data Scientist", "Machine Learning Engineer", "AI Engineer", "Data Analyst"],
        "question": "How does memory management work in Python, and how does Python's Garbage Collection handle circular references?",
        "difficulty": "Medium",
        "key_points_to_cover": [
            "Memory allocation in private heap",
            "Reference counting mechanism",
            "Cyclic garbage collector (generational GC: Gen 0, 1, 2)",
            "The `gc` module and `__del__` caveats"
        ],
        "sample_good_answer": "Python uses automatic memory management consisting primarily of reference counting: each object tracks how many references point to it. When an object's reference count drops to zero, its memory is immediately deallocated. However, reference counting alone cannot reclaim circular references (where Object A points to Object B and vice-versa). For this, Python employs a generational cyclic garbage collector that periodically tracks reference graphs across three generations (0, 1, 2) to detect and reclaim isolated cyclic clusters."
    },

    # --- TECHNICAL: DBMS ---
    {
        "id": "tech_db_01",
        "type": "Technical",
        "category": "DBMS",
        "relevant_careers": ["Software Developer", "Data Scientist", "Data Analyst", "Cloud Engineer"],
        "question": "Explain ACID properties in database management systems and why they are vital for relational databases.",
        "difficulty": "Easy",
        "key_points_to_cover": [
            "Atomicity (All-or-nothing execution of transactions)",
            "Consistency (Database remains in valid state per constraints)",
            "Isolation (Concurrent transactions execute without dirty reads/interference)",
            "Durability (Committed changes survive system crashes)"
        ],
        "sample_good_answer": "ACID properties ensure reliable database transactions. Atomicity guarantees that all statements in a transaction either complete successfully or roll back completely (e.g. debiting one account and crediting another). Consistency ensures that data satisfies all schema constraints and foreign keys before and after execution. Isolation ensures concurrent transactions execute independently without race conditions or dirty reads, achieved via locking or MVCC. Durability ensures that once a transaction commits, its modifications persist on disk even through sudden power failure."
    },
    {
        "id": "tech_db_02",
        "type": "Technical",
        "category": "DBMS",
        "relevant_careers": ["Software Developer", "Data Analyst", "Data Scientist"],
        "question": "What is Database Indexing, how do B-Trees work in indexing, and what are the trade-offs of adding too many indexes?",
        "difficulty": "Medium",
        "key_points_to_cover": [
            "Index as auxiliary data structure to speed up searches",
            "B-Tree / B+Tree balanced search structure",
            "Lookup complexity O(log N) vs full table scan O(N)",
            "Trade-offs: storage overhead and write/insert latency degradation"
        ],
        "sample_good_answer": "Database indexing creates auxiliary data structures (typically B-Trees or B+Trees) on specific table columns to reduce lookup time from O(N) sequential scans to O(log N) tree traversals. While indexes dramatically accelerate SELECT queries and WHERE/JOIN operations, adding too many indexes introduces significant write overhead because every INSERT, UPDATE, or DELETE must also rewrite and rebalance the index trees, in addition to consuming extra disk storage."
    },

    # --- TECHNICAL: OPERATING SYSTEMS ---
    {
        "id": "tech_os_01",
        "type": "Technical",
        "category": "Operating Systems",
        "relevant_careers": ["Software Developer", "Cybersecurity Analyst", "DevOps Engineer", "Cloud Engineer"],
        "question": "What is the difference between a Process and a Thread? When would you choose multi-threading over multi-processing?",
        "difficulty": "Medium",
        "key_points_to_cover": [
            "Process has independent address space; threads share address space within a process",
            "Context switching overhead is higher in processes",
            "Communication: IPC (pipes/sockets) vs shared memory synchronization",
            "Multithreading for I/O-bound tasks; multiprocessing for CPU-bound tasks in Python"
        ],
        "sample_good_answer": "A process is an executing program instance with its own independent memory address space and resources. A thread is a lightweight unit of execution within a process that shares memory and file descriptors with peer threads. Choose multi-threading for I/O-bound workloads (like web scraping or handling multiple network connections) where shared state is beneficial. Choose multi-processing for CPU-bound tasks (like image processing or scientific computations) to bypass Python's Global Interpreter Lock (GIL) and leverage multi-core CPU architectures."
    },

    # --- TECHNICAL: COMPUTER NETWORKS ---
    {
        "id": "tech_net_01",
        "type": "Technical",
        "category": "Computer Networks",
        "relevant_careers": ["Software Developer", "Cybersecurity Analyst", "Cloud Engineer", "DevOps Engineer"],
        "question": "Explain the TCP 3-way handshake and contrast TCP with UDP.",
        "difficulty": "Easy",
        "key_points_to_cover": [
            "SYN, SYN-ACK, ACK handshake sequence",
            "Connection-oriented vs Connectionless",
            "Reliability (acknowledgment, retransmission) in TCP vs low latency in UDP",
            "Use cases: Web/Email (TCP) vs Video streaming/Gaming/DNS (UDP)"
        ],
        "sample_good_answer": "The TCP 3-way handshake establishes a reliable connection: 1) Client sends SYN packet to initiate. 2) Server responds with SYN-ACK packet acknowledging receipt. 3) Client returns ACK packet, establishing the session. TCP is connection-oriented, guarantees packet ordering and delivery through sequence numbers and retransmissions, making it ideal for HTTP, emails, and file transfers. UDP is connectionless and best-effort without delivery guarantees, prioritizing ultra-low latency for video streaming, VoIP, and live gaming."
    },

    # --- TECHNICAL: AI / ML ---
    {
        "id": "tech_aiml_01",
        "type": "Technical",
        "category": "AI/ML",
        "relevant_careers": ["Machine Learning Engineer", "Data Scientist", "AI Engineer"],
        "question": "What is the Bias-Variance tradeoff in Machine Learning, and how do you diagnose and fix High Bias vs High Variance?",
        "difficulty": "Medium",
        "key_points_to_cover": [
            "Bias: underfitting (model too simplistic to capture pattern)",
            "Variance: overfitting (model fits noise in training data)",
            "Diagnosing: train vs validation error curves",
            "Remedies: High bias -> more complex model, more features; High variance -> regularization (L1/L2), dropout, more data, pruning"
        ],
        "sample_good_answer": "The Bias-Variance tradeoff represents the tension between underfitting and overfitting. High bias occurs when an overly simple model fails to capture underlying patterns, resulting in poor performance on both training and test sets. It is fixed by increasing model complexity, engineering new features, or boosting. High variance occurs when a model memorizes training noise, achieving near-perfect train scores but poor generalization. It is resolved by adding regularization (L1/L2, dropout), gathering more training data, or using ensemble methods like Random Forests."
    },
    {
        "id": "tech_aiml_02",
        "type": "Technical",
        "category": "AI/ML",
        "relevant_careers": ["AI Engineer", "Machine Learning Engineer"],
        "question": "How does Retrieval-Augmented Generation (RAG) work, and how does it solve LLM hallucination and knowledge cutoff issues?",
        "difficulty": "Medium",
        "key_points_to_cover": [
            "Document ingestion, chunking, and vector embedding",
            "Semantic similarity search in vector database",
            "Prompt augmentation with retrieved context",
            "Grounding answers on factual documents to prevent hallucinations"
        ],
        "sample_good_answer": "RAG enhances LLM outputs by dynamically injecting relevant external knowledge into the prompt context at inference time. External documents are partitioned into semantic chunks and converted to dense vector embeddings stored in a vector database. When a user asks a query, the query is embedded and compared against stored vectors using cosine similarity. The top matching chunks are retrieved and prepended to the prompt as factual context. This prevents hallucinations by grounding the LLM's response in verified data and eliminates knowledge cutoff constraints without expensive retraining."
    },

    # --- HR / BEHAVIORAL ---
    {
        "id": "hr_01",
        "type": "HR",
        "category": "Tell Me About Yourself",
        "relevant_careers": ["All"],
        "question": "Tell me about yourself, your educational background, and why you are excited about your chosen career field.",
        "difficulty": "Easy",
        "key_points_to_cover": [
            "Brief professional summary (Present, Past, Future framework)",
            "Key technical competencies and academic milestones",
            "Highlight 1-2 impactful projects",
            "Clear articulation of passion for the specific target role"
        ],
        "sample_good_answer": "I am currently completing my degree in Computer Science with a strong focus on backend systems and machine learning. Over the past two years, I have built practical projects such as an end-to-end data pipeline and practiced core data structures and algorithms. I enjoy solving algorithmic challenges and architecting scalable software. I am excited about this role because it combines my passion for clean code and data-driven engineering with the opportunity to build products that impact real users."
    },
    {
        "id": "hr_02",
        "type": "HR",
        "category": "Projects & Challenges",
        "relevant_careers": ["All"],
        "question": "Describe a challenging technical project you worked on. What obstacles did you encounter, and how did you resolve them?",
        "difficulty": "Medium",
        "key_points_to_cover": [
            "STAR method (Situation, Task, Action, Result)",
            "Specific technical problem (e.g. latency, bug, integration issue)",
            "Systematic troubleshooting steps taken",
            "Quantifiable or tangible outcome"
        ],
        "sample_good_answer": "In my college capstone project, I developed an automated document processing API. During initial stress testing, response latency spiked to over 8 seconds under 50 concurrent requests. I used Python profiling tools to isolate the bottleneck, discovering repetitive un-indexed database queries and blocking synchronous HTTP calls. I refactored the pipeline to use asynchronous tasks with Redis and added composite database indexes. This reduced median API response latency by 72% and maintained stability across 200 concurrent requests."
    },
    {
        "id": "hr_03",
        "type": "HR",
        "category": "Conflict Resolution",
        "relevant_careers": ["All"],
        "question": "Can you share an experience where you had a disagreement with a teammate over a technical approach? How did you handle it?",
        "difficulty": "Medium",
        "key_points_to_cover": [
            "Constructive attitude focused on data/facts rather than ego",
            "Active listening to the teammate's perspective",
            "Benchmarking, prototyping, or weighing trade-offs objectively",
            "Achieving consensus and moving forward united"
        ],
        "sample_good_answer": "During a hackathon, my teammate and I disagreed on whether to use a NoSQL document database or a relational PostgreSQL database for our application. My teammate favored MongoDB for speed of initial setup, while I was concerned about structured relational queries. Rather than arguing, I suggested we list our core data access patterns and benchmarked both schemas with a quick 30-minute prototype. The benchmark showed that our data was strictly relational with foreign key constraints, which made PostgreSQL far cleaner to maintain. We mutually agreed, implemented the schema, and won 2nd place in the event."
    },
    {
        "id": "hr_04",
        "type": "HR",
        "category": "Strengths & Weaknesses",
        "relevant_careers": ["All"],
        "question": "What do you consider your greatest technical strength, and what is one area you are actively working to improve?",
        "difficulty": "Easy",
        "key_points_to_cover": [
            "Authentic strength demonstrated with an example",
            "Genuine technical weakness (not a cliché disguised as strength)",
            "Concrete steps and progress in overcoming the weakness"
        ],
        "sample_good_answer": "My greatest strength is systematic problem solving and breaking down ambiguous problems into modular, testable components. When tackling a complex algorithm or bug, I outline edge cases before writing code. An area I am actively improving is DevOps and cloud infrastructure: historically I focused heavily on application logic rather than containerization and CI/CD pipelines. To address this, I have been taking hands-on Docker and Kubernetes labs and setting up automated GitHub Actions workflows for my repository projects."
    }
]

def get_all_interview_questions():
    """Return all interview questions."""
    return INTERVIEW_QUESTIONS

def get_interview_question_by_id(qid):
    """Retrieve question by ID."""
    for q in INTERVIEW_QUESTIONS:
        if q["id"] == qid:
            return q
    return None

def filter_interview_questions(qtype=None, category=None, career_name=None):
    """Filter interview questions by type, category, or relevant career."""
    filtered = INTERVIEW_QUESTIONS
    if qtype and qtype != "All":
        filtered = [q for q in filtered if q["type"] == qtype]
    if category and category != "All":
        filtered = [q for q in filtered if q["category"] == category]
    if career_name and career_name != "All":
        filtered = [q for q in filtered if "All" in q["relevant_careers"] or career_name in q["relevant_careers"]]
    return filtered
