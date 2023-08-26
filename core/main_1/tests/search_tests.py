from search import search, title_length, article_count, random_article, favorite_article, multiple_keywords, display_result
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_titles
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    def test_example_unit_test(self):
        # Storing into a variable so don't need to copy and paste long list every time
        # If you want to store search results into a variable like this, make sure you pass a copy of it when
        # calling a function, otherwise the original list (ie the one stored in your variable) might be
        # mutated. To make a copy, you may use the .copy() function for the variable holding your search result.
        expected_dog_search_results = ['Edogawa, Tokyo', 'Kevin Cadogan', 'Endogenous cannabinoid', 'Black dog (ghost)', '2007 Bulldogs RLFC season', 'Mexican dog-faced bat', 'Dalmatian (dog)', 'Guide dog', '2009 Louisiana Tech Bulldogs football team', 'Georgia Bulldogs football', 'Endoglin', 'Sun dog', 'The Mandogs', 'Georgia Bulldogs football under Robert Winston', 'Landseer (dog)']
        self.assertEqual(search('dog'), expected_dog_search_results)

    def test_search(self):
        expected_dog_search_results = ['Edogawa, Tokyo', 'Kevin Cadogan', 'Endogenous cannabinoid', 'Black dog (ghost)', '2007 Bulldogs RLFC season', 'Mexican dog-faced bat', 'Dalmatian (dog)', 'Guide dog', '2009 Louisiana Tech Bulldogs football team', 'Georgia Bulldogs football', 'Endoglin', 'Sun dog', 'The Mandogs', 'Georgia Bulldogs football under Robert Winston', 'Landseer (dog)']
        self.assertEqual(search('dog'), expected_dog_search_results)
        self.assertEqual(search('DoG'), expected_dog_search_results)
        self.assertEqual(search('cat'), ['Voice classification in non-classical music'])
        self.assertEqual(search(''), [])
        self.assertEqual(search('cats'), [])

    def test_title_length(self):
        titles = ['short', 'medium', 'super duper long']
        self.assertEqual(title_length(16, titles), titles)
        self.assertEqual(title_length(15, titles), ['short', 'medium'])
        self.assertEqual(title_length(5, titles), ['short'])
        self.assertEqual(title_length(4, titles), [])
        self.assertEqual(title_length(0, titles), [])
        self.assertEqual(title_length(10, []), [])

    def test_article_count(self):
        titles = ['short', 'medium', 'super duper long']
        self.assertEqual(article_count(10, titles), titles)
        self.assertEqual(article_count(3, titles), titles)
        self.assertEqual(article_count(2, titles), ['short', 'medium'])
        self.assertEqual(article_count(0, titles), [])
        self.assertEqual(article_count(0, []), [])

    def test_random_article(self):
        titles = ['short', 'medium', 'super duper long']
        self.assertEqual(random_article(10, titles), '')
        self.assertEqual(random_article(3, titles), '')
        self.assertEqual(random_article(-4, titles), '')
        self.assertEqual(random_article(2, titles), 'super duper long')
        self.assertEqual(random_article(0, titles), 'short')
        self.assertEqual(random_article(-2, titles), 'medium')
        self.assertEqual(random_article(0, []), '')

    def test_favorite_article(self):
        titles = ['short', 'medium', 'super duper long']
        self.assertEqual(favorite_article('short', titles), True)
        self.assertEqual(favorite_article('SHoRt', titles), True)
        self.assertEqual(favorite_article('shorts', titles), False)
        self.assertEqual(favorite_article('super duper long', titles), True)
        self.assertEqual(favorite_article('super duper long', []), False)

    def test_multiple_keywords(self):
        basic_titles = ['short', 'medium', 'super duper long']
        expected_dog_search_results = ['Edogawa, Tokyo', 'Kevin Cadogan', 'Endogenous cannabinoid', 'Black dog (ghost)', '2007 Bulldogs RLFC season', 'Mexican dog-faced bat', 'Dalmatian (dog)', 'Guide dog', '2009 Louisiana Tech Bulldogs football team', 'Georgia Bulldogs football', 'Endoglin', 'Sun dog', 'The Mandogs', 'Georgia Bulldogs football under Robert Winston', 'Landseer (dog)']
        self.assertEqual(multiple_keywords('dog', basic_titles), basic_titles + expected_dog_search_results)
        self.assertEqual(multiple_keywords('cats', []), [])
        self.assertEqual(multiple_keywords('dog', []), expected_dog_search_results)
        some_duplicate_titles = ['short', 'Kevin Cadogan', 'Guide dog']
        self.assertEqual(multiple_keywords('dog', some_duplicate_titles), some_duplicate_titles + expected_dog_search_results)

    #####################
    # INTEGRATION TESTS #
    #####################

    @patch('builtins.input')
    def test_basic_only(self, input_mock):
        self.maxDiff = None
        keyword = 'dog'
        advanced_option = 6

        # Output of calling display_results() with given user input. If a different
        # advanced option is included, append further user input to this list (after `advanced_option`)
        output = get_print(input_mock, [keyword, advanced_option])
        # Expected print outs from running display_results() with above user input
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: ['Edogawa, Tokyo', 'Kevin Cadogan', 'Endogenous cannabinoid', 'Black dog (ghost)', '2007 Bulldogs RLFC season', 'Mexican dog-faced bat', 'Dalmatian (dog)', 'Guide dog', '2009 Louisiana Tech Bulldogs football team', 'Georgia Bulldogs football', 'Endoglin', 'Sun dog', 'The Mandogs', 'Georgia Bulldogs football under Robert Winston', 'Landseer (dog)']\n"

        # Test whether calling display_results() with given user input equals expected printout
        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_advanced_1(self, input_mock):
        self.maxDiff = None
        keyword = 'dog'
        advanced_option = 1
        advanced_user_response = 9

        output = get_print(input_mock, [keyword, advanced_option, advanced_user_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_user_response) + "\n\nHere are your articles: ['Guide dog', 'Endoglin', 'Sun dog']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_advanced_2(self, input_mock):
        self.maxDiff = None
        keyword = 'dog'
        advanced_option = 2
        advanced_user_response = 3

        output = get_print(input_mock, [keyword, advanced_option, advanced_user_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_user_response) + "\n\nHere are your articles: ['Edogawa, Tokyo', 'Kevin Cadogan', 'Endogenous cannabinoid']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_advanced_3(self, input_mock):
        self.maxDiff = None
        keyword = 'dog'
        advanced_option = 3
        advanced_user_response = 3

        output = get_print(input_mock, [keyword, advanced_option, advanced_user_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_user_response) + "\n\nHere are your articles: Black dog (ghost)\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_advanced_4(self, input_mock):
        self.maxDiff = None
        keyword = 'dog'
        advanced_option = 4
        advanced_user_response = '2007 Bulldogs RLFC season'

        output = get_print(input_mock, [keyword, advanced_option, advanced_user_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_user_response) + "\n\nHere are your articles: ['Edogawa, Tokyo', 'Kevin Cadogan', 'Endogenous cannabinoid', 'Black dog (ghost)', '2007 Bulldogs RLFC season', 'Mexican dog-faced bat', 'Dalmatian (dog)', 'Guide dog', '2009 Louisiana Tech Bulldogs football team', 'Georgia Bulldogs football', 'Endoglin', 'Sun dog', 'The Mandogs', 'Georgia Bulldogs football under Robert Winston', 'Landseer (dog)']\n" + "Your favorite article is in the returned articles!\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_advanced_5(self, input_mock):
        self.maxDiff = None
        keyword = 'dog'
        advanced_option = 5
        advanced_user_response = 'cat'

        output = get_print(input_mock, [keyword, advanced_option, advanced_user_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_user_response) + "\n\nHere are your articles: ['Edogawa, Tokyo', 'Kevin Cadogan', 'Endogenous cannabinoid', 'Black dog (ghost)', '2007 Bulldogs RLFC season', 'Mexican dog-faced bat', 'Dalmatian (dog)', 'Guide dog', '2009 Louisiana Tech Bulldogs football team', 'Georgia Bulldogs football', 'Endoglin', 'Sun dog', 'The Mandogs', 'Georgia Bulldogs football under Robert Winston', 'Landseer (dog)', 'Voice classification in non-classical music']\n"

        self.assertEqual(output, expected)

if __name__ == "__main__":
    main()
    