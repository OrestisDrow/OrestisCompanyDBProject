# OrestisCompanyDBProject
TBD
--------------WIP-----------------
Its just notes for the time being
--------------------------
The reset_db.sh script focuses solely on the actions required to reset the database.
while the cli.py tool handles user interactions, including confirmation prompts
--------------------------
Use SQL inside container
cd /app/data
sqlite3 orestiscompanydb.sqlite
SELECT * FROM Products;
.exit
--------------------------
How to reset the database (delete + re-populate with pseudo-random generated data)
Using CLI tool:
From inside the docker container:
python /app/src/cli.py resetdb

From outside, using docker:
docker exec [CONTAINER_ID_OR_NAME] python /app/src/cli.py resetdb

--------------------------
Database Design Decision:

In designing the database schema for Orestis Company's sales analytics, I had a decision to make: adopt a more complex, but realistic structure with Orders and SaleLineItems or keep it simpler with just a Sales table.

Why I Chose the Simpler Design:

    Ease of Understanding: I wanted a schema that could be quickly grasped by an audience unfamiliar with in-depth database designs. The simpler design accomplishes this, making it easier for viewers to understand the overall structure and relationships.

    Showcasing Basic Analytics: My primary focus is to demonstrate basic analytics like total sales, most popular products, etc. The Sales table with the added sale_price and amount columns is sufficient for these demonstrations.

    Project Scope: This project is primarily for showcasing purposes. While the more complex design might be more reflective of real-world systems, it introduces an additional layer of complexity that may not provide significant added value for my primary use cases.

    Data Volume: I am working with a dataset that's representative but not exhaustive. The simpler design is adequate for my data volume and still allows for meaningful analytics.

Note: In a real-world scenario, sales systems often have multiple products under one order, which would necessitate a more normalized design with Orders and SaleLineItems. Such a design provides more flexibility and accuracy in modeling complex transactions. However, for the purposes of this showcase, I believe the chosen design strikes the right balance between simplicity and capability.
