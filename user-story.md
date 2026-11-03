# User Story Template

**Title:** <short name of the story>

**As a** <role>
**I need** <function>
**So that** <benefit>

### Details and Assumptions
* <assumption or detail>
* <assumption or detail>

### Acceptance Criteria
```gherkin
Given <a context>
When <an event happens>
Then <an outcome is expected>
```

#### Example
**Title:** Read an account from the service

**As a** service user
**I need** to read an account
**So that** I can see its details

Given an account exists with id 1
When I call GET /accounts/1
Then I receive the account as JSON with status 200
