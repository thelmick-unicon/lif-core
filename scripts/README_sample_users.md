# Sample User Data Generator

This script generates additional sample user data across the 3 demo organizations (`advisor-demo-org1`, `advisor-demo-org2`, and `advisor-demo-org3`).

## Features

- Generates X number of users across all 3 demo organizations (where X is configurable up to 50,000+ unique combinations)
- Each user is created in all 3 organizations with appropriate org-specific information
- **Large Scale Support**: With 219 first names and 251 last names, the script can generate 54,969 unique name combinations
- **Duplicate Prevention**: Automatically avoids duplicate names when possible for better data quality
- Generates realistic user data including:
  - Names, addresses, phone numbers, emails
  - Skills/proficiencies (randomly selected from 48 different skills across multiple domains)
  - Employment experience (randomly generated from 32 different positions across various industries)
  - Organization-specific identifiers
  - Position and employment preferences

## Usage

### Basic Usage
```bash
# Generate 5 users across all 3 demo orgs (15 total files)
python scripts/generate_sample_users.py --num-users 5

# Generate 100 users across all 3 demo orgs (300 total files)
python scripts/generate_sample_users.py --num-users 100

# Generate 1000 users across all 3 demo orgs (3000 total files)
python scripts/generate_sample_users.py --num-users 1000
```

### Advanced Usage
```bash
# Generate users to a custom directory
python scripts/generate_sample_users.py --num-users 500 --output-dir /path/to/custom/directory

# Dry run to see what would be generated (great for large numbers)
python scripts/generate_sample_users.py --num-users 1000 --dry-run
```

## Scale and Performance

The script can efficiently generate large numbers of users:

- **Unique Name Combinations**: 54,969 possible combinations (219 first names × 251 last names)
- **Recommended Maximum**: Up to 10,000 users for reasonable generation time
- **Skills Variety**: 48 different skills across technology, business, healthcare, education, and creative domains
- **Position Variety**: 32 different job positions across multiple industries
- **Duplicate Prevention**: Automatically prevents duplicate names when generating large datasets

## Generated File Structure

For each user, the script creates 3 files (one per organization):
```
projects/mongodb/sample_data/
├── advisor-demo-org1/
│   └── [FirstName]-[LastName]-generated.json
├── advisor-demo-org2/
│   └── [FirstName]-[LastName]-generated.json
└── advisor-demo-org3/
    └── [FirstName]-[LastName]-generated.json
```

## Organization-Specific Features

- **Org1**: Standard user data with Org1-specific identifiers
- **Org2**: Standard user data with Org2-specific identifiers  
- **Org3**: Includes additional "Summit Valley University student ID" identifier

## Data Consistency

- Same user name across all 3 organizations
- Organization-specific email addresses (e.g., `jdoe_lifdemo@stateu.edu`)
- Unique identifiers per organization
- Different contact details (addresses, phone numbers) per organization
- Randomly selected skills and employment experience per user

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Example Output

Running `python scripts/generate_sample_users.py --num-users 1000` would create:

```
advisor-demo-org1/[FirstName]-[LastName]-generated.json (1000 files)
advisor-demo-org2/[FirstName]-[LastName]-generated.json (1000 files)
advisor-demo-org3/[FirstName]-[LastName]-generated.json (1000 files)
```

For example:
```
advisor-demo-org1/Alex-Johnson-generated.json
advisor-demo-org1/Jordan-Smith-generated.json
advisor-demo-org2/Alex-Johnson-generated.json
advisor-demo-org2/Jordan-Smith-generated.json
advisor-demo-org3/Alex-Johnson-generated.json
advisor-demo-org3/Jordan-Smith-generated.json
```

Each file contains a complete user profile with all the necessary fields for the LIF demo system. The script will output progress information and warn if duplicate names are necessary (only relevant for very large numbers > 50,000).