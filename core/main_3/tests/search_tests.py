from search import keyword_to_titles, title_to_info, search, article_length,key_by_author, filter_to_author, filter_out, articles_from_year
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    def test_keyword_to_titles_unique(self):
        dummy_metadata = [
            ['a', 'aa', 123, 456, ['dog', 'cat', 'soccer']],
            ['c', 'cc', 123, 456, ['mouse']],
            ['d', 'dd', 123, 456, ['cats', 'dogs']],
        ]
        expected_dict = {
            'dog': ['a'],
            'cat': ['a'],
            'soccer': ['a'],
            'mouse': ['c'],
            'cats': ['d'],
            'dogs': ['d']
        }
        self.assertDictEqual(keyword_to_titles(dummy_metadata), expected_dict)

    def test_keyword_to_titles_repeats(self):
        dummy_metadata = [
            ['a', 'aa', 123, 456, ['dog', 'cat', 'soccer']],
            ['b', 'bb', 123, 456, ['dog', 'mouse', 'soccer']],
            ['c', 'cc', 123, 456, ['soccer']],
            ['d', 'dd', 123, 456, ['cat', 'soccer']],
        ]
        expected_dict = {
            'dog': ['a', 'b'],
            'cat': ['a', 'd'],
            'soccer': ['a', 'b', 'c', 'd'],
            'mouse': ['b']
        }
        self.assertDictEqual(keyword_to_titles(dummy_metadata), expected_dict)
    
    def test_keyword_to_titles_case_sensitivity(self):
        dummy_metadata = [
            ['a', 'aa', 123, 456, ['dog', 'cat', 'soccer']],
            ['B', 'bb', 123, 456, ['Dog', 'moUSe', 'soCCer']],
            ['cDe', 'cc', 123, 456, ['soccer']],
            ['d', 'dd', 123, 456, ['cat', 'soccer']],
        ]
        expected_dict = {
            'dog': ['a'],
            'Dog': ['B'],
            'cat': ['a', 'd'],
            'soccer': ['a', 'cDe', 'd'],
            'moUSe': ['B'],
            'soCCer': ['B']
        }
        self.assertDictEqual(keyword_to_titles(dummy_metadata), expected_dict)
    
    def test_keyword_to_titles_longer_article_titles(self):
        dummy_metadata = [
            ['abc', 'aa', 123, 456, ['dog', 'cat', 'soccer']],
            ['bcd', 'bb', 123, 456, ['dog', 'mouse', 'soccer']],
            ['cde', 'cc', 123, 456, ['soccer']],
            ['def', 'dd', 123, 456, ['cat', 'soccer']],
        ]
        expected_dict = {
            'dog': ['abc', 'bcd'],
            'cat': ['abc', 'def'],
            'soccer': ['abc', 'bcd', 'cde', 'def'],
            'mouse': ['bcd']
        }
        self.assertDictEqual(keyword_to_titles(dummy_metadata), expected_dict)

    def test_keyword_to_titles_empty(self):
        dummy_metadata = []
        self.assertDictEqual(keyword_to_titles(dummy_metadata), {})

    def test_title_to_info_unique(self):
        dummy_metadata = [
            ['a', 'aa', 123, 456, ['dog', 'cat', 'soccer']],
            ['b', 'bb', 789, 111, ['dog', 'mouse', 'soccer']],
            ['c', 'cc', 333, 555, ['soccer']],
            ['d', 'dd', 888, 444, ['cat', 'soccer']]
        ]
        expected_dict = {
            'a': {'author': 'aa', 'timestamp': 123, 'length': 456},
            'b': {'author': 'bb', 'timestamp': 789, 'length': 111},
            'c': {'author': 'cc', 'timestamp': 333, 'length': 555},
            'd': {'author': 'dd', 'timestamp': 888, 'length': 444}
        }
        self.assertDictEqual(title_to_info(dummy_metadata), expected_dict)
    
    def test_title_to_info_repeat_info(self):
        dummy_metadata = [
            ['abc', 'aa', 123, 123, ['dog', 'cat', 'soccer']],
            ['bcd', 'bb', 123, 123, ['dog', 'mouse', 'soccer']],
            ['cde', 'aa', 123, 123, ['soccer']],
            ['def', 'aa', 888, 888, ['cat', 'soccer']]
        ]
        expected_dict = {
            'abc': {'author': 'aa', 'timestamp': 123, 'length': 123},
            'bcd': {'author': 'bb', 'timestamp': 123, 'length': 123},
            'cde': {'author': 'aa', 'timestamp': 123, 'length': 123},
            'def': {'author': 'aa', 'timestamp': 888, 'length': 888}
        }
        self.assertDictEqual(title_to_info(dummy_metadata), expected_dict)
    
    def test_title_to_info_case_sensitivity(self):
        dummy_metadata = [
            ['abc', 'Aa', 123, 456, ['dog', 'cat', 'soccer']],
            ['Abc', 'bB', 789, 987, ['dog', 'mouse', 'soccer']],
            ['aBcD', 'aa', 11, 22, ['soccer']],
        ]
        expected_dict = {
            'abc': {'author': 'Aa', 'timestamp': 123, 'length': 456},
            'Abc': {'author': 'bB', 'timestamp': 789, 'length': 987},
            'aBcD': {'author': 'aa', 'timestamp': 11, 'length': 22},
        }
        self.assertDictEqual(title_to_info(dummy_metadata), expected_dict)
    
    def test_title_to_info_empty(self):
        dummy_metadata = []
        self.assertDictEqual(title_to_info(dummy_metadata), {})

    def test_search_simple(self):
        dummy_keyword_dict = {
            'cat': ['title1', 'title2', 'title3'],
            'dog': ['title3', 'title4']
        }
        expected_search_results = ['title1', 'title2', 'title3']
        self.assertEqual(search('cat', dummy_keyword_dict), expected_search_results)
    
    def test_search_no_match(self):
        dummy_keyword_dict = {
            'cat': ['title1', 'title2', 'title3'],
            'dog': ['title3', 'title4']
        }
        self.assertEqual(search('lol', dummy_keyword_dict), [])
    
    def test_search_case_sensitive(self):
        dummy_keyword_dict = {
            'cat': ['title1', 'title2', 'title3'],
            'dog': ['title3', 'title4']
        }
        expected_search_results = ['title3', 'title4']
        self.assertEqual(search('Cat', dummy_keyword_dict), [])
    
    def test_search_substring(self):
        dummy_keyword_dict = {
            'cat': ['title1', 'title2', 'title3'],
            'dog': ['title3', 'title4']
        }
        expected_search_results = ['title3', 'title4']
        self.assertEqual(search('ca', dummy_keyword_dict), [])
    
    def test_search_empty(self):
        dummy_keyword_dict = {
            'cat': ['title1', 'title2', 'title3'],
            'dog': ['title3', 'title4']
        }
        expected_search_results = ['title3', 'title4']
        self.assertEqual(search('', dummy_keyword_dict), [])

    def test_article_length_filters_some(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 123, 'length': 789},
            'b': {'author': 'bb', 'timestamp': 789, 'length': 111},
            'c': {'author': 'cc', 'timestamp': 333, 'length': 555},
            'd': {'author': 'dd', 'timestamp': 888, 'length': 456},
            'e': {'author': 'ee', 'timestamp': 234, 'length': 200},
            'f': {'author': 'ff', 'timestamp': 123, 'length': 999}
        }
        basic_search_results = ['a', 'b', 'c', 'd']
        self.assertEqual(article_length(500, basic_search_results, dummy_info), ['b', 'd'])
    
    def test_article_length_filters_none(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 123, 'length': 789},
            'b': {'author': 'bb', 'timestamp': 789, 'length': 111},
            'c': {'author': 'cc', 'timestamp': 333, 'length': 555},
            'd': {'author': 'dd', 'timestamp': 888, 'length': 456},
            'e': {'author': 'ee', 'timestamp': 234, 'length': 200},
            'f': {'author': 'ff', 'timestamp': 123, 'length': 999}
        }
        basic_search_results = ['a', 'b', 'c', 'd']
        self.assertEqual(article_length(789, basic_search_results, dummy_info), ['a', 'b', 'c', 'd'])
    
    def test_article_length_filters_all(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 123, 'length': 789},
            'b': {'author': 'bb', 'timestamp': 789, 'length': 111},
            'c': {'author': 'cc', 'timestamp': 333, 'length': 555},
            'd': {'author': 'dd', 'timestamp': 888, 'length': 456},
            'e': {'author': 'ee', 'timestamp': 234, 'length': 200},
            'f': {'author': 'ff', 'timestamp': 100, 'length': 999}
        }
        basic_search_results = ['a', 'b', 'c', 'd']
        self.assertEqual(article_length(105, basic_search_results, dummy_info), [])
    
    def test_article_length_empty(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 123, 'length': 789},
            'b': {'author': 'bb', 'timestamp': 789, 'length': 111},
            'c': {'author': 'cc', 'timestamp': 333, 'length': 555},
            'd': {'author': 'dd', 'timestamp': 888, 'length': 456},
            'e': {'author': 'ee', 'timestamp': 234, 'length': 200},
            'f': {'author': 'ff', 'timestamp': 100, 'length': 999}
        }
        basic_search_results = []
        self.assertEqual(article_length(1000, basic_search_results, dummy_info), [])

    def test_key_by_author_unique(self):
        dummy_info = {
            'aa': {'author': 'aa', 'timestamp': 123, 'length': 456},
            'ba': {'author': 'bb', 'timestamp': 789, 'length': 111},
            'ca': {'author': 'cc', 'timestamp': 333, 'length': 555},
            'da': {'author': 'dd', 'timestamp': 888, 'length': 456}
        }
        basic_search_results = ['aa', 'ba', 'ca', 'da']
        expected_dict = {
            'aa': ['aa'],
            'bb': ['ba'],
            'cc': ['ca'],
            'dd': ['da']
        }
        self.assertDictEqual(key_by_author(basic_search_results, dummy_info), expected_dict)

    def test_key_by_author_repeats(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 123, 'length': 456},
            'b': {'author': 'bb', 'timestamp': 789, 'length': 111},
            'c': {'author': 'aa', 'timestamp': 333, 'length': 555},
            'd': {'author': 'dd', 'timestamp': 888, 'length': 456},
            'e': {'author': 'aa', 'timestamp': 888, 'length': 456}
        }
        basic_search_results = ['a', 'b', 'c', 'd', 'e']
        expected_dict = {
            'aa': ['a', 'c', 'e'],
            'bb': ['b'],
            'dd': ['d']
        }
        self.assertDictEqual(key_by_author(basic_search_results, dummy_info), expected_dict)

    def test_key_by_author_only_search_results(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 123, 'length': 456},
            'b': {'author': 'bb', 'timestamp': 789, 'length': 111},
            'c': {'author': 'aa', 'timestamp': 333, 'length': 555},
            'd': {'author': 'dd', 'timestamp': 888, 'length': 456},
            'e': {'author': 'aa', 'timestamp': 888, 'length': 456}
        }
        basic_search_results = ['b', 'c']
        expected_dict = {
            'aa': ['c'],
            'bb': ['b'],
        }
        self.assertDictEqual(key_by_author(basic_search_results, dummy_info), expected_dict)

    def test_key_by_author_case_sensitive(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 123, 'length': 456},
            'b': {'author': 'bb', 'timestamp': 789, 'length': 111},
            'c': {'author': 'AA', 'timestamp': 333, 'length': 555},
            'D': {'author': 'dd', 'timestamp': 888, 'length': 456},
        }
        basic_search_results = ['a', 'b', 'c', 'D']
        expected_dict = {
            'aa': ['a'],
            'bb': ['b'],
            'AA': ['c'],
            'dd': ['D']
        }
        self.assertDictEqual(key_by_author(basic_search_results, dummy_info), expected_dict)

    def test_key_by_author_empty(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 123, 'length': 456},
            'b': {'author': 'bb', 'timestamp': 789, 'length': 111},
            'c': {'author': 'AA', 'timestamp': 333, 'length': 555},
            'D': {'author': 'dd', 'timestamp': 888, 'length': 456},
        }
        basic_search_results = []
        self.assertDictEqual(key_by_author(basic_search_results, dummy_info), {})

    def test_filter_to_author_match_single_title(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 123, 'length': 456},
            'b': {'author': 'bb', 'timestamp': 789, 'length': 111},
            'c': {'author': 'aa', 'timestamp': 333, 'length': 555},
            'd': {'author': 'dd', 'timestamp': 888, 'length': 456}
        }
        basic_search_results = ['a', 'b', 'c', 'd']
        self.assertEqual(filter_to_author('bb', basic_search_results, dummy_info), ['b'])
    
    def test_filter_to_author_match_multiple_titles(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 123, 'length': 456},
            'b': {'author': 'bb', 'timestamp': 789, 'length': 111},
            'c': {'author': 'aa', 'timestamp': 333, 'length': 555},
            'd': {'author': 'dd', 'timestamp': 888, 'length': 456}
        }
        basic_search_results = ['a', 'b', 'c', 'd']
        self.assertEqual(filter_to_author('aa', basic_search_results, dummy_info), ['a', 'c'])

    def test_filter_to_author_no_match(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 123, 'length': 456},
            'b': {'author': 'bb', 'timestamp': 789, 'length': 111},
            'c': {'author': 'aa', 'timestamp': 333, 'length': 555},
            'd': {'author': 'dd', 'timestamp': 888, 'length': 456}
        }
        basic_search_results = ['a', 'b', 'c', 'd']
        self.assertEqual(filter_to_author('xxx', basic_search_results, dummy_info), [])

    def test_filter_to_author_empty(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 123, 'length': 456},
            'b': {'author': 'bb', 'timestamp': 789, 'length': 111},
            'c': {'author': 'aa', 'timestamp': 333, 'length': 555},
            'd': {'author': 'dd', 'timestamp': 888, 'length': 456}
        }
        basic_search_results = []
        self.assertEqual(filter_to_author('aa', basic_search_results, dummy_info), [])

    def test_filter_out_removes_some(self):
        dummy_keyword_dict = {
            'cat': ['a', 'b', 'c'],
            'dog': ['c', 'd'],
            'soccer': ['x', 'y', 'z']
        }
        basic_search_results = ['a', 'b', 'c', 'd']
        self.assertEqual(filter_out('dog', basic_search_results, dummy_keyword_dict), ['a', 'b'])

    def test_filter_out_removes_none(self):
        dummy_keyword_dict = {
            'cat': ['a', 'b', 'c'],
            'dog': ['c', 'd'],
            'soccer': ['x', 'y', 'z']
        }
        basic_search_results = ['a', 'b', 'c', 'd']
        self.assertEqual(filter_out('soccer', basic_search_results, dummy_keyword_dict), ['a', 'b', 'c', 'd'])
    
    def test_filter_out_removes_all(self):
        dummy_keyword_dict = {
            'cat': ['a', 'b', 'c', 'd'],
            'dog': ['c', 'd'],
            'soccer': ['x', 'y', 'z']
        }
        basic_search_results = ['a', 'b', 'c', 'd']
        self.assertEqual(filter_out('cat', basic_search_results, dummy_keyword_dict), [])
    
    def test_filter_out_non_matching_keyword(self):
        dummy_keyword_dict = {
            'cat': ['a', 'b', 'c', 'd'],
            'dog': ['c', 'd'],
            'soccer': ['x', 'y', 'z']
        }
        basic_search_results = ['a', 'b', 'c', 'd']
        self.assertEqual(filter_out('xyz', basic_search_results, dummy_keyword_dict), ['a', 'b', 'c', 'd'])

    def test_filter_out_no_basic_results(self):
        dummy_keyword_dict = {
            'cat': ['a', 'b', 'c', 'd'],
            'dog': ['c', 'd'],
            'soccer': ['x', 'y', 'z']
        }
        basic_search_results = []
        self.assertEqual(filter_out('dog', basic_search_results, dummy_keyword_dict), [])

    def test_articles_from_year_filters_some(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 1238489712, 'length': 456},
            'b': {'author': 'bb', 'timestamp': 1218489712, 'length': 111},
            'c': {'author': 'aa', 'timestamp': 1248489712, 'length': 555},
            'd': {'author': 'dd', 'timestamp': 1268489712, 'length': 456}
        }
        basic_search_results = ['a', 'b', 'c', 'd']
        self.assertEqual(articles_from_year(2009, basic_search_results, dummy_info), ['a', 'c'])

    def test_articles_from_year_filters_out_all(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 1238489712, 'length': 456},
            'b': {'author': 'bb', 'timestamp': 1218489712, 'length': 111},
            'c': {'author': 'aa', 'timestamp': 1248489712, 'length': 555},
            'd': {'author': 'dd', 'timestamp': 1268489712, 'length': 456}
        }
        basic_search_results = ['a', 'b', 'c', 'd']
        self.assertEqual(articles_from_year(2019, basic_search_results, dummy_info), [])

    def test_articles_from_year_filters_out_none(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 1238489712, 'length': 456},
            'b': {'author': 'bb', 'timestamp': 1238489812, 'length': 111},
            'c': {'author': 'aa', 'timestamp': 1248489712, 'length': 555},
            'd': {'author': 'dd', 'timestamp': 1240489712, 'length': 456}
        }
        basic_search_results = ['a', 'b', 'c', 'd']
        self.assertEqual(articles_from_year(2009, basic_search_results, dummy_info), ['a', 'b', 'c', 'd'])

    def test_articles_from_year_only_results_from_basic_search(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 1238489712, 'length': 456},
            'b': {'author': 'bb', 'timestamp': 1238489812, 'length': 111},
            'c': {'author': 'aa', 'timestamp': 1248489712, 'length': 555},
            'd': {'author': 'dd', 'timestamp': 1440489712, 'length': 456}
        }
        basic_search_results = ['a', 'd']
        self.assertEqual(articles_from_year(2009, basic_search_results, dummy_info), ['a'])

    def test_articles_from_year_empty(self):
        dummy_info = {
            'a': {'author': 'aa', 'timestamp': 1238489712, 'length': 456},
            'b': {'author': 'bb', 'timestamp': 1238489812, 'length': 111},
            'c': {'author': 'aa', 'timestamp': 1248489712, 'length': 555},
            'd': {'author': 'dd', 'timestamp': 1440489712, 'length': 456}
        }
        basic_search_results = []
        self.assertEqual(articles_from_year(2009, basic_search_results, dummy_info), [])

    #####################
    # INTEGRATION TESTS #
    #####################

    @patch('builtins.input')
    def test_advanced_search_1(self, input_mock):
        keyword = 'soccer'
        advanced_option = 1
        advanced_response = 3000

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_advanced_search_2(self, input_mock):
        keyword = 'soccer'
        advanced_option = 2

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: {'jack johnson': ['Spain national beach soccer team'], 'Burna Boy': ['Will Johnson (soccer)'], 'Mack Johnson': ['Steven Cohen (soccer)']}\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_advanced_search_3(self, input_mock):
        keyword = 'soccer'
        advanced_option = 3
        advanced_response = 'Mack Johnson'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_advanced_search_4(self, input_mock):
        keyword = 'soccer'
        advanced_option = 4
        advanced_response = 'beach'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Will Johnson (soccer)', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_advanced_search_5(self, input_mock):
        keyword = 'soccer'
        advanced_option = 5
        advanced_response = 2009

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)

if __name__ == "__main__":
    main()
