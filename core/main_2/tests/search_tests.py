from search import search, article_length, unique_authors, most_recent_article, favorite_author, title_and_author, refine_search
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############
    def test_search_empty(self):
        self.assertEqual(search(''), [])

    def test_search_dog(self):
        expected_search_dog_results = [
            ['Black dog (ghost)', 'Pegship', 1220471117, 14746],
            ['Mexican dog-faced bat', 'Mack Johnson', 1255316429, 1138],
            ['Dalmatian (dog)', 'Mr Jake', 1207793294, 26582],
            ['Guide dog', 'Jack Johnson', 1165601603, 7339],
            ['Sun dog', 'Mr Jake', 1208969289, 18050]
        ]
        self.assertEqual(search('dog'), expected_search_dog_results)
    
    def test_search_case_insensitive(self):
        expected_search_dog_results = [
            ['Black dog (ghost)', 'Pegship', 1220471117, 14746],
            ['Mexican dog-faced bat', 'Mack Johnson', 1255316429, 1138],
            ['Dalmatian (dog)', 'Mr Jake', 1207793294, 26582],
            ['Guide dog', 'Jack Johnson', 1165601603, 7339],
            ['Sun dog', 'Mr Jake', 1208969289, 18050]
        ]
        self.assertEqual(search('DoG'), expected_search_dog_results)
    
    def test_search_substring(self):
        self.assertEqual(search('do'), [])

    def test_search_no_results(self):
        self.assertEqual(search('gibberish'), [])

    def test_article_length_filters_some(self):
        test_metadata = [
            ['abc', 'jake', 123456, 10],
            ['def', 'mr jake', 123456, 100],
            ['ghi', 'jake', 123456, 50]
        ]
        expected_results = [
            ['abc', 'jake', 123456, 10],
            ['ghi', 'jake', 123456, 50]
        ]
        self.assertEqual(article_length(60, test_metadata), expected_results)
    
    def test_article_length_filters_none(self):
        test_metadata = [
            ['abc', 'jake', 123456, 10],
            ['def', 'mr jake', 123456, 100],
            ['ghi', 'jake', 123456, 50]
        ]
        expected_results = [
            ['abc', 'jake', 123456, 10],
            ['def', 'mr jake', 123456, 100],
            ['ghi', 'jake', 123456, 50]
        ]
        self.assertEqual(article_length(100, test_metadata), expected_results)
    
    def test_article_length_filters_all(self):
        test_metadata = [
            ['abc', 'jake', 123456, 10],
            ['def', 'mr jake', 123456, 100],
            ['ghi', 'jake', 123456, 50]
        ]
        self.assertEqual(article_length(9, test_metadata), [])
    
    def test_article_empty(self):
        test_metadata = []
        self.assertEqual(article_length(60, test_metadata), [])

    def test_unique_authors_no_duplicates(self):
        test_metadata = [
            ['abc', 'jake', 123456, 10],
            ['def', 'prof jake', 123456, 100],
            ['ghi', 'mr jake', 123456, 50]
        ]
        expected_results = [
            ['abc', 'jake', 123456, 10],
            ['def', 'prof jake', 123456, 100]
        ]
        self.assertEqual(unique_authors(2, test_metadata), expected_results)

    def test_unique_authors_duplicates(self):
        test_metadata = [
            ['abc', 'jake', 123456, 10],
            ['def', 'jake', 123456, 100],
            ['lmk', 'jake', 123456, 100],
            ['ghi', 'mr jake', 123456, 50],
            ['xyz', 'prof jake', 123456, 100],
        ]
        expected_results = [
            ['abc', 'jake', 123456, 10],
            ['ghi', 'mr jake', 123456, 50]
        ]
        self.assertEqual(unique_authors(2, test_metadata), expected_results)

    def test_unique_authors_all(self):
        test_metadata = [
            ['abc', 'jake', 123456, 10],
            ['def', 'jake', 123456, 100],
            ['lmk', 'jake', 123456, 100],
            ['ghi', 'mr jake', 123456, 50],
            ['xyz', 'prof jake', 123456, 100],
        ]
        expected_results = [
            ['abc', 'jake', 123456, 10],
            ['ghi', 'mr jake', 123456, 50],
            ['xyz', 'prof jake', 123456, 100]
        ]
        self.assertEqual(unique_authors(10, test_metadata), expected_results)

    def test_unique_authors_none(self):
        test_metadata = [
            ['abc', 'jake', 123456, 10],
            ['def', 'jake', 123456, 100],
            ['lmk', 'jake', 123456, 100],
            ['ghi', 'mr jake', 123456, 50]
        ]
        self.assertEqual(unique_authors(0, test_metadata), [])

    def test_unique_authors_empty(self):
        test_metadata = []
        self.assertEqual(unique_authors(2, test_metadata), [])
    
    def test_most_recent_article_first(self):
        test_metadata = [
            ['abc', 'jake', 1234568, 1],
            ['def', 'jake', 1234567, 2],
            ['ghi', 'mr jake', 1234566, 3]
        ]
        expected_results = ['abc', 'jake', 1234568, 1]
        self.assertEqual(most_recent_article(test_metadata), expected_results)
    
    def test_most_recent_article_middle(self):
        test_metadata = [
            ['abc', 'jake', 1234566, 1],
            ['def', 'jake', 1234568, 2],
            ['ghi', 'mr jake', 1234567, 3]
        ]
        expected_results = ['def', 'jake', 1234568, 2]
        self.assertEqual(most_recent_article(test_metadata), expected_results)
    
    def test_most_recent_article_end(self):
        test_metadata = [
            ['abc', 'jake', 1234566, 1],
            ['def', 'jake', 1234567, 2],
            ['ghi', 'mr jake', 1234568, 3]
        ]
        expected_results = ['ghi', 'mr jake', 1234568, 3]
        self.assertEqual(most_recent_article(test_metadata), expected_results)
    
    def test_most_recent_article_empty(self):
        test_metadata = []
        self.assertEqual(most_recent_article(test_metadata), '')
    
    def test_favorite_author_in_list(self):
        test_metadata = [
            ['abc', 'jake', 123456, 10],
            ['ghi', 'mr jake', 123456, 50],
            ['def', 'jake', 123456, 100],
        ]
        self.assertEqual(favorite_author('mr jake', test_metadata), True)
    
    def test_favorite_author_case_insensitive(self):
        test_metadata = [
            ['abc', 'jake', 123456, 10],
            ['ghi', 'mr jake', 123456, 50],
            ['def', 'jake', 123456, 100]
        ]
        self.assertEqual(favorite_author('MR JaKe', test_metadata), True)

    def test_favorite_author_not_in_list(self):
        test_metadata = [
            ['abc', 'jake', 123456, 10],
            ['def', 'jake', 123456, 100],
            ['ghi', 'mr jake', 123456, 50]
        ]
        self.assertEqual(favorite_author('bono', test_metadata), False)

    def test_favorite_author_substring(self):
        test_metadata = [
            ['abc', 'jake', 123456, 10],
            ['def', 'jake', 123456, 100],
            ['ghi', 'mr jake', 123456, 50]
        ]
        self.assertEqual(favorite_author('jak', test_metadata), False)
    
    def test_favorite_author_empty(self):
        test_metadata = []
        self.assertEqual(favorite_author('jake', test_metadata), False)

    def test_title_and_author_unqiue(self):
        test_metadata = [
            ['abc', 'jake', 123456, 10],
            ['def', 'prof jake', 123456, 100],
            ['ghi', 'mr jake', 123456, 50]
        ]
        expected_result = [
            ('abc', 'jake'),
            ('def', 'prof jake'),
            ('ghi', 'mr jake')
        ]
        self.assertEqual(title_and_author(test_metadata), expected_result)
    
    def test_title_and_author_duplicate_authors(self):
        test_metadata = [
            ['abc', 'jake', 123456, 10],
            ['def', 'jake', 123456, 100],
            ['ghi', 'jake', 123456, 50]
        ]
        expected_result = [
            ('abc', 'jake'),
            ('def', 'jake'),
            ('ghi', 'jake')
        ]
        self.assertEqual(title_and_author(test_metadata), expected_result)
    
    def test_title_and_author_duplicate_titles_and_authors(self):
        test_metadata = [
            ['abc', 'jake', 123456, 10],
            ['abc', 'jake', 123456, 100],
            ['abc', 'jake', 123456, 50]
        ]
        expected_result = [
            ('abc', 'jake'),
            ('abc', 'jake'),
            ('abc', 'jake')
        ]
        self.assertEqual(title_and_author(test_metadata), expected_result)

    def test_title_and_author_empty(self):
        test_metadata = []
        self.assertEqual(title_and_author(test_metadata), [])

    def test_refine_search_some_overlap(self):
        basic_search_results = [
            ['Mexican dog-faced bat', 'Mack Johnson', 1255316429, 1138],
            ['Sun dog', 'Mr Jake', 1208969289, 18050],
            ['abc', 'jake', 123456, 10],
            ['def', 'jake', 123456, 100]
        ]
        expected_results = [
            ['Mexican dog-faced bat', 'Mack Johnson', 1255316429, 1138],
            ['Sun dog', 'Mr Jake', 1208969289, 18050]
        ]
        self.assertEqual(refine_search('dog', basic_search_results), expected_results)
    
    def test_refine_search_none_overlap(self):
        basic_search_results = [
            ['abc', 'jake', 123456, 10],
            ['def', 'jake', 123456, 100]
        ]
        self.assertEqual(refine_search('dog', basic_search_results), [])

    def test_refine_search_all_overlap(self):
        basic_search_results = [
            ['Black dog (ghost)', 'Pegship', 1220471117, 14746],
            ['Mexican dog-faced bat', 'Mack Johnson', 1255316429, 1138],
            ['Dalmatian (dog)', 'Mr Jake', 1207793294, 26582],
            ['Guide dog', 'Jack Johnson', 1165601603, 7339],
            ['Sun dog', 'Mr Jake', 1208969289, 18050]
        ]
        expected_results = [
            ['Black dog (ghost)', 'Pegship', 1220471117, 14746],
            ['Mexican dog-faced bat', 'Mack Johnson', 1255316429, 1138],
            ['Dalmatian (dog)', 'Mr Jake', 1207793294, 26582],
            ['Guide dog', 'Jack Johnson', 1165601603, 7339],
            ['Sun dog', 'Mr Jake', 1208969289, 18050]
        ]
        self.assertEqual(refine_search('dog', basic_search_results), expected_results)
    
    def test_refine_search_empty_new_search(self):
        basic_search_results = [
            ['Mexican dog-faced bat', 'Mack Johnson', 1255316429, 1138],
            ['Sun dog', 'Mr Jake', 1208969289, 18050],
            ['abc', 'jake', 123456, 10],
            ['def', 'jake', 123456, 100]
        ]
        self.assertEqual(refine_search('gibberish', basic_search_results), [])
    
    def test_refine_search_empty_basic_results(self):
        basic_search_results = []
        self.assertEqual(refine_search('dog', basic_search_results), [])

    #####################
    # INTEGRATION TESTS #
    #####################

    @patch('builtins.input')
    def test_advanced_option_1(self, input_mock):
        keyword = 'soccer'
        advanced_option = 1
        advanced_response = 3000

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['Spain national beach soccer team', 'jack johnson', 1233458894, 1526], ['Steven Cohen (soccer)', 'Mack Johnson', 1237669593, 2117]]\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_advanced_option_2(self, input_mock):
        keyword = 'dogs'
        advanced_option = 2
        advanced_response = 5

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['Black dog (ghost)', 'Pegship', 1220471117, 14746], ['2007 Bulldogs RLFC season', 'Burna Boy', 1177410119, 11116], ['Dalmatian (dog)', 'Mr Jake', 1207793294, 26582], ['Guide dog', 'Jack Johnson', 1165601603, 7339], ['Landseer (dog)', 'Bearcat', 1231438650, 2006]]\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_advanced_option_3(self, input_mock):
        keyword = 'dogs'
        advanced_option = 3

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: ['Landseer (dog)', 'Bearcat', 1231438650, 2006]\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_advanced_option_4(self, input_mock):
        keyword = 'dogs'
        advanced_option = 4
        advanced_response = 'Mr Jake'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['Black dog (ghost)', 'Pegship', 1220471117, 14746], ['2007 Bulldogs RLFC season', 'Burna Boy', 1177410119, 11116], ['Dalmatian (dog)', 'Mr Jake', 1207793294, 26582], ['Guide dog', 'Jack Johnson', 1165601603, 7339], ['Sun dog', 'Mr Jake', 1208969289, 18050], ['Landseer (dog)', 'Bearcat', 1231438650, 2006]]\nYour favorite author is in the returned articles!\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_advanced_option_5(self, input_mock):
        keyword = 'dogs'
        advanced_option = 5

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: [('Black dog (ghost)', 'Pegship'), ('2007 Bulldogs RLFC season', 'Burna Boy'), ('Dalmatian (dog)', 'Mr Jake'), ('Guide dog', 'Jack Johnson'), ('Sun dog', 'Mr Jake'), ('Landseer (dog)', 'Bearcat')]\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_advanced_option_6(self, input_mock):
        keyword = 'dogs'
        advanced_option = 6
        advanced_response = 'breed'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['Dalmatian (dog)', 'Mr Jake', 1207793294, 26582], ['Guide dog', 'Jack Johnson', 1165601603, 7339]]\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_advanced_option_7(self, input_mock):
        keyword = 'dogs'
        advanced_option = 7

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: [['Black dog (ghost)', 'Pegship', 1220471117, 14746], ['2007 Bulldogs RLFC season', 'Burna Boy', 1177410119, 11116], ['Dalmatian (dog)', 'Mr Jake', 1207793294, 26582], ['Guide dog', 'Jack Johnson', 1165601603, 7339], ['Sun dog', 'Mr Jake', 1208969289, 18050], ['Landseer (dog)', 'Bearcat', 1231438650, 2006]]\n"

        self.assertEqual(output, expected)

if __name__ == "__main__":
    main()
    