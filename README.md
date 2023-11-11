# OrestisCompanyDBProject

Welcome to my imaginary company called Orestis Company!
The OrestisCompanyDBProject is a Dockerized Python application that provides a command-line interface (CLI) for interacting with the OrestisCompany's sales database, along with a web-based analytics dashboard service for various analytics visualizations. The primary aim of this project is for showcasing more than anything else.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Using the CLI](#using-the-cli)
- [Accessing the Analytics Dashboard](#accessing-the-analytics-dashboard)
- [Purpose of this Project](#purpose-of-this-project)
- [Database Design Decisions](#database-design-decisions)
- [Analytics Design Decisions](#analytics-design-decisions)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

To run this project, you will need Docker installed on your system. You can download it from [Docker's official website](https://www.docker.com/get-started).

### Installation

1. Clone the repo to your favourite folder:
```bash
git clone https://github.com/OrestisDrow/OrestisCompanyDBProject.git
```
2. Navigate to the cloned directory:
```bash
cd OrestisCompanyDBProject
```
3. Build the Docker image:
```bash
docker build -t orestiscompany .
```
4. Run the container and map a host port to container port 8050 (default host port 8050, feel free to change it).
```bash
docker run -it -p 8050:8050 orestiscompany
```
After running the above command, you will start interacting with the CLI.

## Using the CLI

After starting the Docker container, you'll be presented with a command-line interface where you can execute various commands to interact with the database, preprocess various kinds of analytics from the data, and visualize the results. I have designed the CLI to guide you so you dont get lost.

## Accessing the Analytics Dashboard

When the command is given to the CLI to fire up the analytics dashboard, then it will be available at `http://localhost:8050` by default, or to any other port you had mapped onto the 8050 port of the container. This service provides web-based visualizations for basic, intermediate, and advanced analytics based on the pseudo-randomly generated data in the OrestisCompany's database.

## Purpose of this project

The OrestisCompanyDBProject ambitiously aims to bridge the gap between data engineering and data science. It is a comprehensive application journeying from the ground up of database design to the pinnacle of analytic insights. This project emphasizes the art of the possible in data analytics, showcasing a progression from fundamental data management and modeling to sophisticated data exploration techniques. The pseudo-random nature of the dataset underscores the illustrative purpose of the analytics, challenging users to imagine the transformative insights such analysis could yield in real-world applications.

## Database Design Decisions

![ERD Diagram](/docs/schema.png "Database Entity-Relation-Diagram")

The project employs a star schema for database design, aimed at optimizing query performance for analytics workloads. This schema is particularly well-suited for the data warehousing and business intelligence applications that form the core of this project. It provides a balanced approach, offering both simplicity in understanding and efficiency in data retrieval.

### Key Tables:

- **Stores**: Contains comprehensive details about each store location.
- **Products**: Holds an inventory of products, reflecting the range and depth of the company's offerings.
- **Customers**: Captures essential customer data, providing a foundation for customer relationship management and personalized analytics.
- **DateInfo**: Serves as a time dimension table, crucial for time-series analysis and temporal trends.
- **Sales**: Acts as the fact table in our star schema, central to recording transactions and correlating the various dimensions.

The chosen schema enables quick iteration and real-time updates for the analytics dashboard, essential for delivering timely insights. Additionally, the structure is designed to be scalable, allowing for future enhancements such as incorporating additional dimensions or supporting more granular transaction data.

### Why a Simpler Design:

- **Ease of Understanding**: A straightforward schema ensures quick comprehension, essential for educational purposes and ease of onboarding for new developers or analysts.
- **Analytic Showcase**: The focus is to illustrate how even a streamlined data model can support a wide range of analytics, from fundamental reporting to complex predictive modeling.
- **Project Scope**: The project's scope is to demonstrate a full-stack application from data storage to insight generation, and the simpler design is sufficient for this narrative.
- **Data Volume**: Given the representative nature of the dataset, the current schema provides the right balance between detail and manageability, ensuring the system remains responsive and agile.

This design reflects a deliberate choice to prioritize educational clarity and analytical demonstration over mimicking the complexity of a real-world enterprise system. It is a conscious trade-off that serves the project's goals of being an instructional tool and a proof of concept for integrating data engineering with data science. 

For example, in a real-world scenario, sales systems often have multiple products under one order, which would necessitate a more normalized design with Orders and SaleLineItems. Such a design provides more flexibility and accuracy in modeling complex transactions. However, for the purposes of this showcase, I believe the chosen design strikes the right balance between simplicity and capability.

The design choice is a balance between educational simplicity and the potential for real-world application, demonstrating the end-to-end capabilities of a full-stack data solution.

## Analytics Design Decisions

The analytics component of the OrestisCompanyDBProject is meticulously architected to demonstrate the spectrum of insights that can be derived from data at various levels of complexity — ranging from basic to advanced. It's important to note that the data driving these analytics are pseudo-randomly generated, and hence, the insights derived are illustrative rather than actionable.

### Insights as Demonstrations:

- **Basic Analytics**: Showcases foundational analytical operations, such as aggregations and summarizations, which are the first steps in understanding data trends and distributions.
- **Intermediate Analytics**: Introduces more complex calculations and time-series analysis, painting a more detailed picture of business operations and performance over time.
- **Advanced Analytics**: Explores predictive modeling and customer segmentation techniques, exemplifying how data science can forecast trends and categorize behaviors.

### Purpose of the Analytics Showcase:

The primary goal of presenting these three tiers of analytics is not to provide concrete business insights but to illustrate the depth and potential of data analysis in a real-world setting. The project aims to:

- **Spark Imagination**: Encourage users to envisage the type of insights and decision-making support that such analytics could provide in actual business scenarios.
- **Demonstrate Potential**: Exhibit how data, when leveraged with the right tools and techniques, can transform into strategic knowledge, influencing business outcomes and driving growth.
- **Educational Tool**: Serve as a comprehensive reference for educational purposes, illustrating the application of various data science and analytics methodologies in a controlled environment.

In the context of this project, the analytics are designed to be a sandbox for exploration and learning. They present a narrative that invites users to think critically about how each layer of analysis could be applied to their data and the type of intelligence each layer could unveil.

This approach underscores the project's commitment to bridging the gap between theoretical knowledge and practical application, providing a playground where the implications of data engineering and data science are not only seen but felt in a hands-on manner.


