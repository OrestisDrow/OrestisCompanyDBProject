# OrestisCompanyDBProject
TBD
/OrestisCompanyDB
│
├── /data
│   └── orestiscompanydb.sqlite  # SQLite database file
│
├── /docs
│   ├── schema.png               # Visual schema of the database (Entity-Relation Diagram)
│
├── /sql
│   ├── init.sql                 # SQL commands to set up tables and relationships
│
├── /src
│   ├── my_script.py             # Sample Python script file
│   └── ...                      # Other Python source files
│
├── /visualizations
│   └── ...                      # Generated charts, plots, etc.
│
├── Dockerfile                   # Docker build instructions
│
├── docker-compose.yml           # Docker Compose configuration
│
├── requirements.txt             # Python package dependencies
│
└── README.md                    # Project overview, setup instructions, etc.

--------------WIP-----------------
Database Design Decision:

In designing the database schema for Orestis Company's sales analytics, I had a decision to make: adopt a more complex, but realistic structure with Orders and SaleLineItems or keep it simpler with just a Sales table.

Why I Chose the Simpler Design:

    Ease of Understanding: I wanted a schema that could be quickly grasped by an audience unfamiliar with in-depth database designs. The simpler design accomplishes this, making it easier for viewers to understand the overall structure and relationships.

    Showcasing Basic Analytics: My primary focus is to demonstrate basic analytics like total sales, most popular products, etc. The Sales table with the added sale_price and amount columns is sufficient for these demonstrations.

    Project Scope: This project is primarily for showcasing purposes. While the more complex design might be more reflective of real-world systems, it introduces an additional layer of complexity that may not provide significant added value for my primary use cases.

    Data Volume: I am working with a dataset that's representative but not exhaustive. The simpler design is adequate for my data volume and still allows for meaningful analytics.

Note: In a real-world scenario, sales systems often have multiple products under one order, which would necessitate a more normalized design with Orders and SaleLineItems. Such a design provides more flexibility and accuracy in modeling complex transactions. However, for the purposes of this showcase, I believe the chosen design strikes the right balance between simplicity and capability.