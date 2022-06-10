import lyrics_fun as lf
import argparse

# Create the parser
my_parser = argparse.ArgumentParser(prog='lyrical-genius',
                                    description='Predict which artist a lyric snippet is or could be from.\n ' \
                                        'The lyrical genius trains a logistic regression model on all available lyrics' \
                                        'of two user-supplied artists. Lyrics are accessed from lyrics.com, and' \
                                        'the user has several options for dropping unwanted lyrics, which could' \
                                        'bias the predictions (e.g., instrumentals, remixes, acoustic versions, etc.).'
                                    
                                    )

my_parser.add_argument('artist1', action='store', type=str, help='str, name of first artist to pull lyrics from.')


my_parser.add_argument('artist2', action='store', type=str,  help='str, name of second artist to pull lyrics from.')


my_parser.add_argument('new_lyric', action='store', type=str, help ='str, text snippet to assign to first or second artist based on predicted probabilities.')


my_parser.add_argument('--drop_duplicates', action='store', type=bool, required=False, default=True)
my_parser.add_argument('--drop_instrumentals', action='store', type=bool, required=False, default=True)
my_parser.add_argument('--drop_similar', action='store', type=bool, required=False, default=True)
my_parser.add_argument('--verbose', action='store', type=bool, required=False, default=True)

args = my_parser.parse_args()

lf.predict_artist(
    first = args.artist1,
    second = args.artist2,
    new_lyric=args.new_lyric,
    drop_duplicates=args.drop_duplicates,
    drop_instrumentals=args.drop_instrumentals,
    drop_similar=args.drop_similar,
    verbose=args.verbose)






