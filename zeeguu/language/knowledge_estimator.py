from zeeguu.api.model_core import Language, RankedWord, KnownWordProbability, EncounterBasedProbability, Bookmark
import zeeguu


class SethiKnowledgeEstimator(object):

    def __init__(self, user, lang_code = None):
        self.user = user
        if lang_code:
            self.lang_code = lang_code
        else:
            self.lang_code = user.learned_language

    def known_words_list(self):
        lang_id = Language.find(self.lang_code)
        bookmarks = self.user.all_bookmarks()
        known_words = []
        filtered_known_words_from_user = []
        filtered_known_words_dict_list = []
        for bookmark in bookmarks:
            if bookmark.check_is_latest_outcome_too_easy():
                known_words.append(bookmark.origin.word)
        for word_known in known_words:
            if RankedWord.exists(word_known, lang_id):
                filtered_known_words_from_user.append(word_known)
                zeeguu.db.session.commit()
        filtered_known_words_from_user = list(set(filtered_known_words_from_user))
        for word in filtered_known_words_from_user:
            filtered_known_words_dict_list.append({'word': word})
        return filtered_known_words_dict_list

    def get_known_bookmarks(self):
        """
        All the bookmarks that the user knows and are in a given language
        :param user:
        :param lang:
        :return:
        """
        bookmarks = self.user.all_bookmarks()
        known_bookmarks=[]
        for bookmark in bookmarks:
            if bookmark.check_is_latest_outcome_too_easy() and self.lang_code == bookmark.origin.language:
                    known_bookmark_dict = {
                        'id': bookmark.id,
                        'origin': bookmark.origin.word,
                        'text': bookmark.text.content,
                        'time': bookmark.time.strftime('%m/%d/%Y')}
                    known_bookmarks.append(known_bookmark_dict)
        return known_bookmarks

    def get_known_bookmarks_count(self):
        return len(self.get_known_bookmarks())

    def learned_bookmarks(self):
        """
        Returns the bookmarks that the user has learned.
        :param user:
        :param lang:
        :return: list of bookmarks
        """
        bookmarks = self.user.all_bookmarks()
        too_easy_bookmarks = []
        for bookmark in bookmarks:
            if bookmark.check_is_latest_outcome_too_easy() and bookmark.origin.language == self.lang_code:
                too_easy_bookmarks.append(bookmark)
        return [bookmark for bookmark in bookmarks if bookmark not in too_easy_bookmarks]

    def get_not_encountered_words(self):
        not_encountered_words_dict_list = []
        all_ranks = RankedWord.find_all(self.lang_code)
        known_word_probs = KnownWordProbability.find_all_by_user_with_rank(self.user)
        for p in known_word_probs:
            if p.ranked_word in all_ranks:
                all_ranks.remove(p.ranked_word)
        for rank in all_ranks:
            not_encountered_word_dict = {}
            not_encountered_word_dict['word'] = rank.word
            not_encountered_words_dict_list.append(not_encountered_word_dict)
        return not_encountered_words_dict_list

    def get_not_encountered_words_count(self):
        return len(self.get_not_encountered_words())

    def get_not_looked_up_words(self):
        filtered_words_known_from_user_dict_list =[]
        enc_probs = EncounterBasedProbability.find_all_by_user(self.user)
        for enc_prob in enc_probs:
            if enc_prob.ranked_word.language == self.lang_code:
                filtered_words_known_from_user_dict_list.append( {'word': enc_prob.ranked_word.word} )
        return filtered_words_known_from_user_dict_list

    def get_not_looked_up_words_for_learned_language(self):
        return self.get_not_looked_up_words()

    def get_not_looked_up_words_count(self):
        return len(self.get_not_looked_up_words_for_learned_language())

    def get_probably_known_words(self):
        probabilities = KnownWordProbability.get_probably_known_words(self.user)

        probable_known_words_dict_list = []
        for prob in probabilities:
            probable_known_word_dict = {}
            if prob.ranked_word is not None and prob.ranked_word.language == self.lang_code:
                probable_known_word_dict['word'] = prob.ranked_word.word
            else:
                probable_known_word_dict['word'] = prob.user_word.word
            probable_known_words_dict_list.append(probable_known_word_dict)
        return probable_known_words_dict_list

    def get_probably_known_words_count(self):
        return len(self.get_probably_known_words())

    def get_lower_bound_percentage_of_basic_vocabulary(self):
        high_known_word_prob_of_user = KnownWordProbability.get_probably_known_words(self.user)
        count_high_known_word_prob_of_user_ranked = 0
        for prob in high_known_word_prob_of_user:
            if prob.ranked_word is not None and prob.ranked_word.rank <=3000:
                count_high_known_word_prob_of_user_ranked +=1
        return round(float(count_high_known_word_prob_of_user_ranked)/3000*100,2)

    def get_upper_bound_percentage_of_basic_vocabulary(self):
        count_not_looked_up_words_with_rank = 0
        not_looked_up_words = EncounterBasedProbability.find_all_by_user(self.user)
        for prob in not_looked_up_words:
            if prob.ranked_word.rank <=3000:
                count_not_looked_up_words_with_rank +=1
        return round(float(count_not_looked_up_words_with_rank)/3000*100,2)

    def get_lower_bound_percentage_of_extended_vocabulary(self):
        high_known_word_prob_of_user = KnownWordProbability.get_probably_known_words(self.user)
        count_high_known_word_prob_of_user_ranked = 0
        for prob in high_known_word_prob_of_user:
            if prob.ranked_word is not None and prob.ranked_word.rank <=10000:
                count_high_known_word_prob_of_user_ranked +=1
        return round(float(count_high_known_word_prob_of_user_ranked)/10000*100,2)

    def get_upper_bound_percentage_of_extended_vocabulary(self):
        count_not_looked_up_words_with_rank = 0
        not_looked_up_words = EncounterBasedProbability.find_all_by_user(self.user)
        for prob in not_looked_up_words:
            if prob.ranked_word.rank <=10000:
                count_not_looked_up_words_with_rank +=1
        return round(float(count_not_looked_up_words_with_rank)/10000*100,2)

    def get_percentage_of_probably_known_bookmarked_words(self):
        high_known_word_prob_of_user = KnownWordProbability.get_probably_known_words(self.user)
        count_high_known_word_prob_of_user =0
        count_bookmarks_of_user = len(self.user.all_bookmarks())
        for prob in high_known_word_prob_of_user:
            if prob.user_word is not None:
                count_high_known_word_prob_of_user +=1
        if count_bookmarks_of_user <> 0:
            return round(float(count_high_known_word_prob_of_user)/count_bookmarks_of_user*100,2)
        else:
            return 0

    def words_being_learned(self, language):
        # Get the words the user is currently learning
        words_learning = {}
        bookmarks = Bookmark.find_by_specific_user(self.user)
        for bookmark in bookmarks:
            learning = not bookmark.check_is_latest_outcome_too_easy()
            user_word = bookmark.origin
            if learning and user_word.language == language:
                words_learning[user_word.word] = user_word.word
        return words_learning


