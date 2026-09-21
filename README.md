# Citizen Email Dataset for Waste Collection

## Overview

This project contains a dataset of 200+ synthetic citizen emails related to waste collection services. Each email has been manually assigned to one of four categories:

* Missed Pickup
* Schedule Change
* Complaint
* Other

## Dataset

The dataset is stored in emails_labeled.csv

The CSV contains two columns:

| Column       | Description                                           |
| ------------ | ----------------------------------------------------- |
| `email_text` | The citizen's email or message about waste collection |
| `label`      | The category assigned to the email                    |

## Data Source

The emails are synthetic examples created specifically for this project. They are realistic mock citizen messages about waste collection services and do not contain real citizens' personal information.

## Categories and Labeling Guide

### 1. Missed Pickup

Use **Missed Pickup** when the citizen reports that their waste, garbage, recycling, or bin was not collected when it was expected to be collected.

**Examples:**

* "Our garbage was not collected yesterday."
* "The truck skipped our street this morning."
* "My bin is still full after today's collection."

### 2. Schedule Change
Use **Schedule Change** when the citizen asks about changing, moving, or confirming a collection date or schedule.

**Examples:**
* "Can my collection day be changed from Monday to Wednesday?"
* "Has the pickup schedule changed this week?"
* "When will our collection day be moved because of the holiday?"
### 3. Complaint
Use **Complaint** when the citizen expresses dissatisfaction with the waste collection service or reports a service-related problem that is primarily a complaint.

**Examples:**

* "I am unhappy with the poor collection service."
* "The waste service in our area has been very disappointing."
* "I want to complain about the repeated problems with garbage collection."

### 4. Other

Use **Other** when the email is related to waste collection but does not primarily describe a missed pickup, request a schedule change, or make a complaint.

This category can include general questions, information requests, or other waste-service inquiries.

**Examples:**

* "What items are accepted for recycling?"
* "What time does the collection truck normally arrive?"
* "Where can I find information about recycling rules?"

## Labeling Rules

1. Assign exactly one label to each email.
2. Choose the label based on the main purpose of the email.
3. Use **Missed Pickup** when the main issue is that a scheduled collection did not happen.
4. Use **Schedule Change** when the main purpose is changing, checking, or asking about a collection schedule.
5. Use **Complaint** when the main purpose is expressing dissatisfaction or making a service complaint.
6. Use **Other** for waste-collection questions that do not fit the other three categories.

   Keep the four labels exactly as written:

* `Missed Pickup`
* `Schedule Change`
* `Complaint`
* `Other`

## Dataset Validation
The repository includes a Python validation script:

The script checks:
* Whether `emails_labeled.csv` exists
* Whether the required columns are present
* Whether each row contains an email and label
* Whether the labels belong to the four allowed categories
* Whether the dataset contains at least 200 rows

## Project Files
waste-emails-dataset
│
├── emails_labeled.csv
├── validate_csv.py
└── README.md