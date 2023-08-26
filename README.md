# Simple Search Engine

## Project Description
A search engine is a powerful tool that takes a user's query and retrieves relevant information from a database. In this project, we will develop an enhanced search engine that goes beyond basic keyword matching. Our search engine will utilize a 2D list of article metadata and employ various advanced search techniques to provide users with more precise search results.

### Part 1: Basic Search
The basic search functionality allows users to enter a keyword and retrieve a list of articles that are relevant to that keyword. This search is case-insensitive and considers the keywords associated with each article. Users will be prompted to provide a keyword, and the search engine will return a list of matching articles.

### Part 2: Preprocessing
In this phase, we preprocess the article metadata to create dictionaries that will help optimize our search processes. Two preprocessing functions, `title_to_info` and `keyword_to_titles`, will be implemented to convert the metadata into dictionaries that map article titles to relevant information and keywords to article titles, respectively.

### Part 3: Advanced Search
The advanced search phase introduces more refined search options to cater to user preferences. Users can choose from the following advanced search techniques:

- Article Title Length: Users can specify a maximum article title length, and the search engine will return article titles that meet this criterion.

- Key by Author: This option returns a dictionary mapping authors to the articles they have written, based on the basic search results.

- Filter to Author: Users can select an author, and the search engine will return articles from the basic search that are written by that author.

- Filter Out Keyword: Users can input a keyword to be excluded from the search results. The search engine will return articles that do not have this keyword in their list of related keywords.

- Articles from Year: Users can input a year, and the search engine will return articles from the basic search that were published in that year.

- None: Users can choose not to perform an advanced search.

## Conclusion
In conclusion, this project aims to create an enhanced search engine that leverages article metadata and advanced search techniques to provide users with more refined and accurate search results. By combining basic and advanced search options, users can tailor their queries and obtain information that best matches their interests and requirements.
