https://docs.google.com/document/d/1UueEWDvVYhtHwAnfbfOX13_VxRlormSnFE7ZxUzoW_M/edit

Praktika Senior Python Backend Engineer Coding Challenge

At Praktika, we value creative solutions, rapid prototyping, and high-quality code. This task is a small example of a challenge we typically face when creating new features for our language learners.
You need to design and implement an API service called "Word of the Day Article." This API fetches the current daily word from the Wordsmith's RSS feed, available here: https://wordsmith.org/awad/rss1.xml, and generates an article explaining this word using any generative AI tool of your choice. Your API should return a reading article that contains 2 fields:
Header: Usually around 50 characters.
Body: Up to 300 characters
Since the word of the day changes daily, a new article should be generated every day. It is required to reuse the same generated article within a day to save on the generative AI tool calls.
An example of an article embedded in the application can be seen in the screenshot below:

Technical Requirements
Language: Python 3
API framework: FastAPI
Testing framework: pytest
Generative AI Tool: Any of your choice (e.g., OpenAI gpt-3.5-turbo, etc.)
Containerization: Docker
You are free to use any other tools and libraries
Deliverables
A zip archive containing:
source code;
tests;
README file, explaining how to install and run your solution;

Notes:
Do NOT include any secret credentials in the submission (like OpenAI API keys)
Do NOT publish your code to GitHub. Instead, package your project as a zip archive and send it to your recruiter.
Expectations
You are expected to come up with a production-grade code for this problem

Your submission will be evaluated based on code quality, testing coverage, readability, appropriate use of abstractions, solution correctness, and performance at scale.

The solution should demonstrate a clear separation of concerns and modularity, correctly implement the required functionality, and handle edge cases and errors gracefully.

Comprehensive tests should cover key functionalities, edge cases, and error handling.

We expect the task to take you approximately 2-3 hours

Any unclear requirements should be defined and stated in the README file.

We look forward to reviewing your solution and wish you the best of luck!

Best regards,
The Praktika Team
