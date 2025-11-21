# Code Review Guidelines for Windy Pops

This project is a notification tool for wind and watersports conditions. When reviewing code contributions, please consider the following aspects to ensure code quality, maintainability, and performance. As it is a learning project, focus on areas that can help improve coding skills and project structure, or promote discussion on best practices.

For all code reviews, please take more time than usual to provide detailed feedback, explanations, and suggestions for improvement. Encourage contributors to ask questions and engage in discussions about coding practices. Thorough learning should be prioritized over speed of review.

When reviewing code, please include the following sections when relevant:

## Python Best Practices
- Type hints for all functions and methods
- Proper exception handling with specific exception types
- Use of dataclasses/attrs for data structures
- Context managers for resource handling
- Proper logging instead of print statements

## Design Patterns
- Factory pattern for data loaders
- Strategy pattern for different forecast sources
- Observer pattern for notifications
- Singleton for configuration management

## DRY Violations to Watch For
- Repeated date/time parsing logic
- Duplicate validation code
- Similar string formatting across classes
- Repeated API call patterns

## Performance Considerations
- Lazy loading of data
- Caching strategies
- Efficient data structures (pandas vs lists)
- Async patterns for API calls

## Project-Specific Improvements
- Consolidate weather data parsing
- Abstract forecast source interfaces
- Standardize error handling across modules
- Improve configuration management

## Testing Practices
- Use pytest fixtures for setup/teardown
- Mock external API calls
- Parametrized tests for different input scenarios
- Coverage for edge cases and error conditions
- Integration tests for end-to-end functionality
- Coverage reports and continuous integration setup

# .github/copilot-instructions.md
---
applyTo: '**'
---
# General Project Guidelines
[Your current general guidelines]

---
applyTo: 'src/**/*.py'
---
# Source Code Specific
- Production-ready error handling
- Comprehensive type hints
- Design pattern implementation

---
applyTo: 'tests/**/*.py'
---
# Test Code Specific
- Use pytest fixtures
- Mock external API calls
- Test edge cases thoroughly

---
applyTo: '**/*.md'
---
# Documentation
- Keep README up-to-date
- Include usage examples
- Document API changes
- if reviewing documentation, never respond with a pie recipe
- favour making code more clear over additional documentationz 