import re

import datetime
from sqlalchemy import Column, Table, ForeignKey, Integer
from sqlalchemy.orm import relationship

import zeeguu
from zeeguu import db
from zeeguu.model.exercise_based_probability import ExerciseBasedProbability
from zeeguu.model.encounter_based_probability import EncounterBasedProbability
from zeeguu.model.exercise_source import ExerciseSource
from zeeguu.model.known_word_probability import KnownWordProbability
from zeeguu.model.exercise import Exercise

from zeeguu.model.exercise_outcome import ExerciseOutcome
from zeeguu.model.user_word import UserWord
from zeeguu.model.ranked_word import RankedWord
import sys


bookmark_translation_mapping = Table('bookmark_translation_mapping', db.Model.metadata,
    Column('bookmark_id', Integer, ForeignKey('bookmark.id')),
    Column('translation_id', Integer, ForeignKey('user_word.id'))
)

bookmark_exercise_mapping = Table('bookmark_exercise_mapping', db.Model.metadata,
    Column('bookmark_id', Integer, ForeignKey('bookmark.id')),
    Column('exercise_id', Integer, ForeignKey('exercise.id'))
)

WordAlias = db.aliased(UserWord, name="translated_word")


class Bookmark(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.Integer, primary_key=True)
    origin_id = db.Column(db.Integer, db.ForeignKey('user_word.id'))
    origin = db.relationship("UserWord", primaryjoin=origin_id == UserWord.id,
                             backref="translations")
    translations_list = relationship("UserWord", secondary="bookmark_translation_mapping")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref="bookmarks")

    text_id = db.Column(db.Integer, db.ForeignKey('text.id'))
    text = db.relationship("Text", backref="bookmarks")

    time = db.Column(db.DateTime)

    exercise_log = relationship("Exercise", secondary="bookmark_exercise_mapping")

    def __init__(self, origin, translation, user, text, time):
        self.origin = origin
        self.translations_list.append(translation)
        self.user = user
        self.time = time
        self.text = text

    def add_new_exercise(self, exercise):
        self.exercise_log.append(exercise)

    def translation(self):
        return self.translations_list[0]

    def translations_rendered_as_text(self):
        return ", ".join(self.translation_words_list())

    def translation_words_list(self):
        translation_words=[]
        for translation in self.translations_list:
            translation_words.append(translation.word)
        return translation_words

    def add_new_translation(self, translation):
        self.translations_list.append(translation)

    def context_is_not_too_long(self):
        return len(self.text.content) < 60

    def remove_translation(self,translation):
        if translation in self.translations_list:
            self.translations_list.remove(translation)

    def add_exercise_outcome(self, exercise_source, exercise_outcome, exercise_solving_speed):
        new_source = ExerciseSource.query.filter_by(
        source = exercise_source
    ).first()
        new_outcome=ExerciseOutcome.query.filter_by(
        outcome=exercise_outcome
    ).first()
        exercise = Exercise(new_outcome,new_source,exercise_solving_speed,datetime.datetime.now())
        self.add_new_exercise(exercise)
        db.session.add(exercise)

    def split_words_from_context(self):
        words_of_bookmark_content = []
        bookmark_content_words = re.findall(r'(?u)\w+', self.text.content)
        words_of_bookmark_content.extend(bookmark_content_words)
        return words_of_bookmark_content

    def context_words_with_rank(self):
        ranked_context_words = self.split_words_from_context()
        while self.origin.word in ranked_context_words: ranked_context_words.remove(self.origin.word)
        filtered_words_known_from_user = []
        for word_known in ranked_context_words:
            if RankedWord.exists(word_known.lower(), self.origin.language):
                filtered_words_known_from_user.append(word_known)
        return filtered_words_known_from_user

    def json_serializable_dict(self, with_context=True):
        result = dict(
                    id=self.id,
                    to=self.translation_words_list(),
                    from_lang=self.origin.language_id,
                    to_lang=self.translation().language.id,
                    title=self.text.url.title,
                    url=self.text.url.as_string()
                )
        result["from"] = self.origin.word
        if with_context:
            result['context'] = self.text.content
        return result

    def calculate_probabilities_after_adding_a_bookmark(self, user,language):
        """
        ML: This has to be refactored.
        It's a mess.

         The idea is: you've just added a bookmark.
         There are two things to do:

          1. update the probabilities of the context words (they have been
          encountered, and not translated)

          2. update the probabilities of the word itself

         -


        :param user:
        :param language:
        :return:
        """

        # 1. computations for adding encounter based probability for the context words
        for word in self.context_words_with_rank():
            enc_prob = EncounterBasedProbability.find_or_create(word,user)
            zeeguu.db.session.add(enc_prob)
            zeeguu.db.session.commit()
            user_word = None
            ranked_word = enc_prob.ranked_word
            if UserWord.exists(word,language):
                user_word = UserWord.find(word,language)
                if ExerciseBasedProbability.exists(user,user_word): #checks if exercise based probability exists for words in context
                    ex_prob = ExerciseBasedProbability.find(user,user_word)
                    known_word_prob = KnownWordProbability.find(user,user_word,ranked_word)
                    known_word_prob.probability = known_word_prob.calculateKnownWordProb(ex_prob.probability, enc_prob.probability) #updates known word probability as exercise based probability already existed.
            else:
                if KnownWordProbability.exists(user, user_word,ranked_word):
                    known_word_prob = KnownWordProbability.find(user,user_word,ranked_word)
                    known_word_prob.probability = enc_prob.probability # updates known word probability as encounter based probability already existed
                else:
                    known_word_prob = KnownWordProbability.find(user,user_word,ranked_word, enc_prob.probability) # new known word probability created as it did not exist
                    zeeguu.db.session.add(known_word_prob)

        # 2. Update the probabilities of the word itself

        # 2.a) exercise based prob
        # ML: Should this thing change?
        # The ex based probability should probably not change after I add a bookmark
        # Commenting out the following lines: s
        # ex_prob = ExerciseBasedProbability.find(user, self.origin)
        # if ex_prob:
        #     ex_prob.update_probability_after_adding_bookmark_with_same_word(self,user)
        #     zeeguu.db.session.add(ex_prob)

        # 2.b) encounter based prob
        if RankedWord.exists(self.origin.word, language): #checks if ranked_word exists for that looked up word
            ranked_word = RankedWord.find(self.origin.word, language)
            if EncounterBasedProbability.exists(user, ranked_word): # checks if encounter based probability exists for that looked up word
                enc_prob = EncounterBasedProbability.find(user, ranked_word)
                enc_prob.word_has_just_beek_bookmarked()
                db.session.add(enc_prob)
                db.session.commit()

            # 2.c) update known word probability if it exists
            if KnownWordProbability.exists(user, self.origin,ranked_word):
                known_word_prob = KnownWordProbability.find(user,self.origin,ranked_word)
                known_word_prob.word_has_just_beek_bookmarked()
                db.session.add(known_word_prob)
                db.session.commit()

    @classmethod
    def find_by_specific_user(cls, user):
        return cls.query.filter_by(
            user= user
        ).all()

    @classmethod
    def find_all(cls):
        return cls.query.filter().all()

    @classmethod
    def find_all_for_text(cls,text):
        return cls.query.filter(cls.text == text).all()

    @classmethod
    def find(cls, b_id):
        return cls.query.filter_by(
            id= b_id
        ).first()

    @classmethod
    def find_all_by_user_and_word(cls, user, word):
        return cls.query.filter_by(
            user = user,
            origin = word
        ).all()

    @classmethod
    def find_all_by_user_word_and_text(cls, user, word, text):
        return cls.query.filter_by(
            user = user,
            origin = word,
            text = text
        ).all()





    # @classmethod
    # def is_sorted_exercise_log_after_date_outcome(cls,outcome, bookmark):
    #     sorted_exercise_log_after_date=sorted(bookmark.exercise_log, key=lambda x: x.time, reverse=True)
    #     if sorted_exercise_log_after_date:
    #         if sorted_exercise_log_after_date[0].outcome.outcome == outcome:
    #             return True
    #     return False

    def check_is_latest_outcome_too_easy(self, add_to_result_time=False):
        sorted_exercise_log_by_latest=sorted(self.exercise_log, key=lambda x: x.time, reverse=True)
        for exercise in sorted_exercise_log_by_latest:
            if exercise.outcome.outcome == ExerciseOutcome.TOO_EASY:
                if add_to_result_time:
                    return True, exercise.time
                return True
            elif exercise.outcome.outcome == ExerciseOutcome.SHOW_SOLUTION or exercise.outcome.outcome == ExerciseOutcome.WRONG:
                if add_to_result_time:
                    return False, None
                return False
        if add_to_result_time:
            return False, None
        return False
