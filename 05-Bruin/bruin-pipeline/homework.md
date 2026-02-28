# Module 5 Homework: Data Platforms with Bruin


---

In this homework, we'll use Bruin to build a complete data pipeline, from ingestion to reporting.

## Setup

1. Install Bruin CLI: `curl -LsSf https://getbruin.com/install/cli | sh`
2. Initialize the zoomcamp template: `bruin init zoomcamp my-pipeline`
3. Configure your `.bruin.yml` with a DuckDB connection
4. Follow the tutorial in the [main module README](../../../05-data-platforms/)

After completing the setup, you should have a working NYC taxi data pipeline.

---

### Question 1. Bruin Pipeline Structure

In a Bruin project, what are the required files/directories?

- `bruin.yml` and `assets/`
- `.bruin.yml` and `pipeline.yml` (assets can be anywhere)
- `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/`
- `pipeline.yml` and `assets/` only

#### Question 1 Answer

ANSWER:
- **`.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/`**

In a Bruin project, you firstly have the `.bruin.yml` file, which is the project's configuration file that will need to exist at the root of the Git repository. It defines connections, environments, as well as secrets (which is why this file should never be commited).

Next, you also need a `pipeline/` directory (it doesn't nessecarily need to be named 'pipeline', but for the sake of the answer, we say that directory name). Within the pipeline directory, there is the `pipeline.yml` file and the `assets/` directory.

The `pipeline.yml` file defines the pipeline's name, schedules, connections, variables, etc.

The `assets/` directpory has to be in the same directory as the `pipeline.yml` file. This file contains the asset files of the bruin pipeline (parts that build up the pipeline in the first place).
---

### Question 2. Materialization Strategies

You're building a pipeline that processes NYC taxi data organized by month based on `pickup_datetime`. Which incremental strategy is best for processing a specific interval period by deleting and inserting data for that time period?

- `append` - always add new rows
- `replace` - truncate and rebuild entirely
- `time_interval` - incremental based on a time column
- `view` - create a virtual table only

#### Question 2 Answer

ANSWER: 
- **`time_interval` - incremental based on a time column**

The `time_interval` strategy deletes existing records within a specific time interval and then inserts new records from a query ***for*** that interval - hence it is the correct answer for this question.


---

### Question 3. Pipeline Variables

You have the following variable defined in `pipeline.yml`:

```yaml
variables:
  taxi_types:
    type: array
    items:
      type: string
    default: ["yellow", "green"]
```

How do you override this when running the pipeline to only process yellow taxis?

- `bruin run --taxi-types yellow`
- `bruin run --var taxi_types=yellow`
- `bruin run --var 'taxi_types=["yellow"]'`
- `bruin run --set taxi_types=["yellow"]`

#### Question 3 Answer

ANSWER:
- **`bruin run --var 'taxi_types=["yellow"]'`**

The reason it is this answer and not with the variable defined as `taxi_types=yellow` is due to the fact that the `taxi_types` variable is defined as an array, and so when overriding it, we have to pass the value as a JSON-style array to keep with the variable's type.

---

### Question 4. Running with Dependencies

You've modified the `ingestion/trips.py` asset and want to run it plus all downstream assets. Which command should you use?

- `bruin run ingestion.trips --all`
- `bruin run ingestion/trips.py --downstream`
- `bruin run pipeline/trips.py --recursive`
- `bruin run --select ingestion.trips+`

#### Question 4 Answer

ANSWER:
- **`bruin run ingestion/trips.py --downstream`**

This run command will run the asset passed into the command. The `downstream` flag tells Bruin to run all the downstream dependencies of the asset passed. 


---

### Question 5. Quality Checks

You want to ensure the `pickup_datetime` column in your trips table never has NULL values. Which quality check should you add to your asset definition?

- `name: unique`
- `name: not_null`
- `name: positive`
- `name: accepted_values, value: [not_null]`

#### Question 5 Answer

ANSWER:
- `name: not_null`

The `not_null` quality check is the correct one to add to the asset definition to ensure that there are never NULL values.

---

### Question 6. Lineage and Dependencies

After building your pipeline, you want to visualize the dependency graph between assets. Which Bruin command should you use?

- `bruin graph`
- `bruin dependencies`
- `bruin lineage`
- `bruin show`

#### Question 6 Answer 

ANSWER:
- `bruin lineage`

The `lineage` command visualizes the asset dependency graph, which is what we are looking to do in this question.

---

### Question 7. First-Time Run

You're running a Bruin pipeline for the first time on a new DuckDB database. What flag should you use to ensure tables are created from scratch?

- `--create`
- `--init`
- `--full-refresh`
- `--truncate`

#### Question 7 Answer

ANSWER:
- `--full-refresh`

The `full-refresh` flag makes it so that any tables in the pipeline are recreated if they exist. If they do not exist, the tables are created. Therefore, this is the right flag to use to ensure tables are created from scratch.

---