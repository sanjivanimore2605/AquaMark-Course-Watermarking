# Report Text Content Definition for AquaMark Academic Report

FRONT_MATTER = {
    "project_title": "AquaMark — Secure Digital Watermarking and Document Integrity Platform",
    "official_topic": "Robust Digital Watermarking for Protection of Electronic Course Content",
    "domain": "Cryptography, Cybersecurity, Digital Watermarking, Document Security, and Software Development",
    "student_name": "Sanjivani Rameshwar More",
    "roll_number": "2124UCSM11115",
    "programme": "B.Tech in Computer Science and Engineering (Cyber Security)",
    "year_semester": "Third Year (5th Semester), Division A",
    "department": "Department of Cyber Security, School of Engineering and Technology (SET)",
    "college_name": "Sanjivani University, Kopargaon",
    "university_name": "Sanjivani University, Kopargaon",
    "guide_name": "[Project Guide Name, Designation]",
    "head_of_department": "Dr. Chetan D. Bawankar\nHead, Department of Cyber Security\nSET, Sanjivani University, Kopargaon",
    "academic_year": "2026 – 2027",
    "submission_date": "October 2026"
}

ABSTRACT_TEXT = (
    "With the rapid digitization of higher education, course materials—including syllabus guides, lecture slides, "
    "laboratory manuals, assignment solutions, and examination question papers—are increasingly distributed as Portable Document "
    "Format (PDF) files. While digital distribution facilitates remote learning and frictionless access, it exposes institutional "
    "intellectual property to widespread unauthorized redistribution, illicit monetization on commercial academic platforms, "
    "and untracked document manipulation. Conventional document security controls suffer from fundamental engineering trade-offs: "
    "visual text overlays are easily cropped or eliminated via standard PDF manipulation tools, rigid cryptographic hashes (such as "
    "SHA-256) are brittle under benign rasterization or re-compression, and digital signatures alone verify recorded digests rather "
    "than tracking leaked raster renderings.\n\n"
    "This academic project report presents AquaMark, a web-based educational document protection platform designed around a Layered "
    "Trust Architecture. AquaMark coordinates three complementary technical mechanisms: (1) PyMuPDF-driven visible vector watermarking "
    "for immediate visual deterrence across all document pages; (2) an invisible Discrete Cosine Transform (2D-DCT) steganographic pipeline "
    "that modulates 8x8 luminance block mid-frequency coefficients (3,2) and (2,3) with an 8-bit preamble synchronization marker [1,0,1,0,1,1,0,0] "
    "to embed recipient-specific identifiers resistant to lossy JPEG compression; and (3) an asymmetric cryptographic engine based on Ed25519 "
    "digital signatures over canonical JSON manifests, SHA-256 binary digests, HMAC-SHA-256 record authentication, Argon2id password hashing, "
    "and tamper-evident SHA-256 chained audit logging.\n\n"
    "The implementation comprises an asynchronous Python FastAPI backend, a React 19 and TypeScript frontend styled with Tailwind CSS, "
    "an Object-Relational Mapping (ORM) persistence layer via SQLAlchemy, and an interactive empirical Robustness Testing Lab. Automated "
    "unit and integration test suites confirm 100% test passage across cryptographic primitives, DCT embedding and extraction routines, and "
    "role-based endpoint authorization. Experimental evaluations within the Robustness Lab verify that embedded DCT payloads withstand lossy "
    "JPEG compression at quality factors down to Q=70 with Peak Signal-to-Noise Ratios exceeding 38 dB and 0.0% Bit Error Rates. This report "
    "provides a comprehensive, scientifically rigorous analysis of the architecture, implementation, mathematical methodologies, security threat "
    "models, verified testing results, and honest operational boundaries."
)
