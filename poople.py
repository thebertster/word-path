#!/usr/bin/python

"""Find shortest path between two words of the same length where each word
in the path changes by a single letter. Solves poople.io.
"""

import argparse
import sys

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def load_word_list(filename: str) -> tuple[set[str],
                                           list[tuple[int, str]],
                                           int]:
    """Load word list from external file.

    Args:
        filename (str): Filename containing word list

    Returns:
        tuple[set, list, int]: Tuple of word_list (set), error_list (list)
                               word_length (int)      
    """

    word_list = set()
    error_list = []
    word_length = 0
    try:
        with open(filename, mode='r', encoding='UTF-8') as file:
            for line, word in enumerate(file):
                word = word.strip().upper()

                if word:
                    if word_length:
                        if len(word) != word_length:
                            error_list.append((line, word))
                            continue
                    else:
                        word_length = len(word)

                    if all((letter in ALPHABET for letter in word)):
                        word_list.add(word)
                    else:
                        error_list.append((line, word))

    except FileNotFoundError:
        pass

    return word_list, error_list, word_length


def construct_graph(word_list: set[str]) -> dict[str, list[str]]:
    """Construct connected graph between words.

    Args:
        word_list (set): Word list

    Returns:
        dict: Dictionary of words and their connected words
    """

    nodes = {}
    for word in word_list:
        next_nodes = []
        for n, letter in enumerate(word):
            new_word_l = list(word)
            for new_letter in ALPHABET:
                if new_letter != letter:
                    new_word_l[n] = new_letter
                    new_word = ''.join(new_word_l)
                    if new_word in word_list:
                        next_nodes.append(new_word)
        nodes[word] = next_nodes

    return nodes


def shortest_path(graph: dict[str, list[str]],
                  start_word: str, end_word: str) -> list[str]:
    """Find shortest path between start_word and end_word.

    Args:
        graph (dict): Graph of word connections
        start_word (str): Starting word
        end_word (str): Ending word

    Returns:
        list: List of words in connecting sequence or [] if no path exists
    """

    visited = set()
    check_paths = [[start_word]]

    while check_paths:
        new_check_paths = []
        for check_path in check_paths:
            current_node = check_path[-1]
            if current_node == end_word:
                return check_path
            visited.add(current_node)
            new_check_paths.extend([check_path + [next_node]
                                    for next_node in graph[current_node]
                                    if next_node not in visited])
        check_paths = new_check_paths

    return ['NO SOLUTION']


def main() -> None:
    """Main function
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('start_word', help='Starting word')
    parser.add_argument('end_word', nargs='?', help='Finishing word',
                        default='POOP')
    parser.add_argument('word_list_filename', nargs='?',
                        help='Path to word list',
                        default='poople_word_list.txt')

    args = parser.parse_args()
    word_list_filename = args.word_list_filename
    start_word = args.start_word.strip().upper()
    end_word = args.end_word.strip().upper()

    word_list, error_list, word_length = load_word_list(word_list_filename)

    if error_list:
        num_errors = len(error_list)
        print(f'Word list contained {num_errors} errors!')
        for line, word in error_list[:10]:
            print(f'{line:6}: {word}')
        if num_errors > 10:
            print('(and more)')

    print(f'Using word list with {len(word_list)} {word_length}-letter words.')

    if len(start_word) != word_length:
        print(f'{start_word} is not a {word_length}-letter word!')
        sys.exit()

    if len(end_word) != word_length:
        print(f'{end_word} is not a {word_length}-letter word!')
        sys.exit()

    word_list |= {start_word, end_word}

    graph = construct_graph(word_list)

    print()
    print('The solution is...')

    solution = shortest_path(graph, start_word, end_word)

    print(' -> '.join(solution))


if __name__ == '__main__':
    main()
