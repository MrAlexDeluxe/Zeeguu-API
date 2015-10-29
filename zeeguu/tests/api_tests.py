import zeeguu_testcase
# Always must be imported first
# it sets the test DB

import unittest
import zeeguu.populate
import zeeguu.model
from zeeguu.model import User
from zeeguu import util
import json
import re
import time


sondernExampleData = dict(
    url='http://mir.lu/examples_with_karan',
    context='Wir arbeiten nicht sondern schlafen')

strassenExampleFormData = dict(
    url='http://mir.lu',
    context='chilling on the streets')



class API_Tests(zeeguu_testcase.ZeeguuTestCase):

    def test_logout(self):
        self.logout()
        rv = self.app.get('/recognize')
        assert 'Redirecting' in rv.data

    def test_bookmark_from_android(self):
        formData = dict(
            url='http://mir.lu',
            context='somewhere over the rainbowwwwwwwww',
            title="lal")
        rv = self.api_post('/bookmark_with_context/de/sondern/en/but', formData)
        t = zeeguu.model.Url.find("android:app","Songs by Iz")

        assert t != None

        rv = self.api_get('/get_known_bookmarks/de')
        print rv.data + "<---"

        assert 'sondern' in rv.data
        assert 'Zeeguu for Android' in rv.data


    def test_bookmark_without_title_should_fail(self):
        formData = dict(
            url='http://mir.lu',
            context='somewhere over the rainbowwwwwwwww')
        rv = self.api_post('/bookmark_with_context/de/sondern/en/but', formData)
        added_bookmark_id = int(rv.data)
        rv = self.api_get('/bookmarks_by_day/with_context')
        elements = json.loads(rv.data)
        first_date = elements[0]
        latest_bookmark_id = int(first_date["bookmarks"][0]['id'])
        assert latest_bookmark_id  == added_bookmark_id

    def test_get_probably_known(self):
        rv = self.api_get('/get_probably_known_words/de')
        probably_known_words = json.loads(rv.data)
        assert not any(word['word'] == 'gute' for word in probably_known_words)
        assert not any(word['word'] == 'nacht' for word in probably_known_words)
        assert not any(word['word'] == 'sondern' for word in probably_known_words)
        formData = dict(
            url='http://mir.lu',
            context='gute nacht sondern')
        rv = self.api_post('/bookmark_with_context/de/sondern/en/but', formData)
        self.api_post('/gym/create_new_exercise/Too easy/Recognize/10000/'+ rv.data)
        rv1 = self.api_get('/get_probably_known_words/de')
        probably_known_words = json.loads(rv1.data)
        assert any(word['word'] == 'sondern' for word in probably_known_words)
        self.api_post('/gym/create_new_exercise/Show solution/Recognize/10000/'+ rv.data)
        rv = self.api_get('/get_probably_known_words/de')
        probably_known_words = json.loads(rv.data)
        assert not any(word['word'] == 'sondern' for word in probably_known_words)
        formData = dict(
            url='http://mir.lu',
            context='gute nacht sondern')
        self.api_post('/bookmark_with_context/de/sondern/en/but', formData)
        formData = dict(
            url='http://mir.lu',
            context='gute nacht sondern')
        self.api_post('/bookmark_with_context/de/sondern/en/but', formData)
        formData = dict(
            url='http://mir.lu',
            context='gute nacht sondern')
        self.api_post('/bookmark_with_context/de/sondern/en/but', formData)
        formData = dict(
            url='http://mir.lu',
            context='gute nacht sondern')
        self.api_post('/bookmark_with_context/de/sondern/en/but', formData)
        rv = self.api_get('/get_probably_known_words/de')
        probably_known_words = json.loads(rv.data)
        assert any(word['word'] == 'gute' for word in probably_known_words)
        assert any(word['word'] == 'nacht' for word in probably_known_words)
        assert not any(word['word'] == 'sondern' for word in probably_known_words)






    def test_delete_bookmark(self):
        rv = self.api_get('/bookmarks_by_day/with_context')
        bookmarks_by_day_dict_before_delete = json.loads(rv.data)
        bookmarks_on_first_date_before_delete = bookmarks_by_day_dict_before_delete[0]['bookmarks']
        first_bookmark_on_first_date_id = bookmarks_on_first_date_before_delete [0] ['id']
        assert any(bookmark['id'] == first_bookmark_on_first_date_id for bookmark in bookmarks_on_first_date_before_delete)
        assert first_bookmark_on_first_date_id is not None
        rv = self.api_post('/delete_bookmark/'+ str(first_bookmark_on_first_date_id))
        assert rv.data == "OK"
        rv = self.api_get('/bookmarks_by_day/with_context')
        bookmarks_by_day_dict_after_delete = json.loads(rv.data)
        bookmarks_on_first_date_after_delete = bookmarks_by_day_dict_after_delete[0]['bookmarks']
        assert not any(bookmark['id'] == first_bookmark_on_first_date_id for bookmark in bookmarks_on_first_date_after_delete)

    def test_create_new_exercise(self):
        rv = self.api_post('/gym/create_new_exercise/Correct/Recognize/10000/2')
        assert rv.data =="OK"
        rv = self.api_post('/gym/create_new_exercise/Correct/Recogniz/10000/3')
        assert rv.data =="FAIL"

    def test_get_exercise_log_for_bookmark(self):
       rv = self.api_get('/get_exercise_log_for_bookmark/3')
       assert "Correct" not in rv.data
       rv = self.api_post('/gym/create_new_exercise/Correct/Recognize/10000/3')
       assert rv.data =="OK"
       rv = self.api_post('/gym/create_new_exercise/Typo/Translate/10000/3')
       assert rv.data =="OK"
       rv = self.api_get('/get_exercise_log_for_bookmark/3')
       assert "Correct" in rv.data
       assert "Translate" in rv.data

    def test_add_new_translation_to_bookmark(self):
        rv = self.api_post('/add_new_translation_to_bookmark/women/1')
        assert rv.data =="OK"
        rv = self.api_get('/get_translations_for_bookmark/2')
        translations_dict_of_bookmark = json.loads(rv.data)
        first_translation_word_of_bookmark = translations_dict_of_bookmark[0]['word']
        rv = self.api_post('/add_new_translation_to_bookmark/'+str(first_translation_word_of_bookmark)+'/2')
        assert rv.data == 'FAIL'

    def test_delete_translation_from_bookmark(self):
        rv = self.api_get('/get_translations_for_bookmark/2')
        translations_dict_of_bookmark = json.loads(rv.data)
        first_word_translation_of_bookmark = translations_dict_of_bookmark[0]['word']
        rv = self.api_post('/delete_translation_from_bookmark/2/'+str(first_word_translation_of_bookmark))
        assert rv.data =='FAIL'
        rv = self.api_post('/add_new_translation_to_bookmark/women/2')
        rv = self.api_get('/get_translations_for_bookmark/2')
        translations_dict_of_bookmark = json.loads(rv.data)
        first_word_translation_of_bookmark = translations_dict_of_bookmark[0]['word']
        assert any (translation['word'] == first_word_translation_of_bookmark for translation in translations_dict_of_bookmark)
        assert any(translation['word'] == 'women' for translation in translations_dict_of_bookmark)
        rv = self.api_post('/delete_translation_from_bookmark/2/wome')
        assert rv.data == 'FAIL'
        rv = self.api_post('/delete_translation_from_bookmark/2/'+str(first_word_translation_of_bookmark))
        assert rv.data =='OK'
        rv = self.api_get('/get_translations_for_bookmark/2')
        translations_dict_of_bookmark = json.loads(rv.data)
        assert not any(translation['word'] == first_word_translation_of_bookmark for translation in translations_dict_of_bookmark)




    def test_delete_bookmark(self):
        rv = self.api_post('/delete_bookmark/2')
        assert rv.data =='OK'
        rv = self.api_post('/delete_bookmark/2')
        assert rv.data == "FAIL"



    def test_get_translations_for_bookmark(self):
       rv = self.api_get('/get_translations_for_bookmark/2')
       translations_dict_bookmark_before_add = json.loads(rv.data)
       assert len(translations_dict_bookmark_before_add) ==1
       first_translation_word = translations_dict_bookmark_before_add[0]['word']
       assert any(translation['word'] == first_translation_word for translation in translations_dict_bookmark_before_add)
       rv = self.api_post('/add_new_translation_to_bookmark/women/2')
       assert rv.data == "OK"
       rv = self.api_get('/get_translations_for_bookmark/2')
       translations_dict_bookmark_after_add = json.loads(rv.data)
       assert len(translations_dict_bookmark_after_add) ==2
       assert first_translation_word!= 'women'
       assert any(translation['word'] == first_translation_word for translation in translations_dict_bookmark_after_add)
       assert any(translation['word'] == 'women' for translation in translations_dict_bookmark_after_add)


    def test_get_known_bookmarks(self):
        self.api_post('/bookmark_with_context/de/sondern/en/but rather', sondernExampleData)
        self.api_post('/bookmark_with_context/de/strassen/en/streets', strassenExampleFormData)

        rv = self.api_get('/bookmarks_by_day/with_context')
        bookmarks_by_day = json.loads(rv.data)
        assert any(context['context'] ==  'chilling on the streets' for context in bookmarks_by_day[0]['bookmarks'])
        #assert 'chilling on the streets' == bookmarks_by_day[0]['bookmarks'][0]['context']
        #assert sondernExampleData["context"] == bookmarks_by_day[0]['bookmarks'][1]['context']
        assert any (context ['context'] == sondernExampleData["context"] for context in bookmarks_by_day[0]['bookmarks'])
        latest_bookmark_id = bookmarks_by_day[0]['bookmarks'][0]['id']
        print bookmarks_by_day[0]

        second_latest_bookmark_id = bookmarks_by_day[0]['bookmarks'][1]['id']
        rv = self.api_get('/get_exercise_log_for_bookmark/'+str(latest_bookmark_id))
        'Too easy' not in rv.data
        rv = self.api_get('/get_exercise_log_for_bookmark/'+str(second_latest_bookmark_id))
        'Too easy' not in rv.data
        self.api_post('/gym/create_new_exercise/Too easy/Recognize/10000/'+ str(latest_bookmark_id))
        rv = self.api_get('/get_known_bookmarks/de')
        known_bookmarks_before = json.loads(rv.data)
        assert any(bookmark['id'] == latest_bookmark_id for bookmark in known_bookmarks_before)
        assert not any(bookmark['id'] == second_latest_bookmark_id for bookmark in known_bookmarks_before)
        self.api_post('/gym/create_new_exercise/Too easy/Recognize/10000/'+ str(second_latest_bookmark_id))
        rv3 = self.api_get('/get_known_bookmarks/de')
        known_bookmarks_after = json.loads(rv3.data)
        assert any(bookmark['id'] == latest_bookmark_id for bookmark in known_bookmarks_after)
        assert any(bookmark['id'] == second_latest_bookmark_id for bookmark in known_bookmarks_after)

        time.sleep(2) # delays for 5 seconds
        self.api_post('/gym/create_new_exercise/Show solution/Recognize/10000/'+ str(second_latest_bookmark_id))
        rv4 = self.api_get('/get_known_bookmarks/de')
        known_bookmarks_after = json.loads(rv4.data)
        assert not any(bookmark['id'] == second_latest_bookmark_id for bookmark in known_bookmarks_after)




    def test_get_known_words(self):
        rv = self.api_post('/bookmark_with_context/de/sondern/en/but', sondernExampleData)
        formData = dict(
            url='http://mir.lu',
            context='saying hi to girls')
        rv = self.api_post('/bookmark_with_context/de/maedchen/en/girls', formData)
        formData = dict(
            url='http://mir.lu',
            context='chilling with the girls')
        rv = self.api_post('/bookmark_with_context/de/maedchen/en/girls', formData)
        rv = self.api_get('/bookmarks_by_day/with_context')
        bookmarks_by_day = json.loads(rv.data)
        latest_bookmark_id = bookmarks_by_day[0]['bookmarks'][0]['id']
        second_latest_bookmark_id = bookmarks_by_day[0]['bookmarks'][1]['id']
        third_latest_bookmark_id = bookmarks_by_day[0]['bookmarks'][2]['id']
        latest_bookmark_word = bookmarks_by_day[0]['bookmarks'][0]['from']
        second_latest_bookmark_word = bookmarks_by_day[0]['bookmarks'][1]['from']
        third_latest_bookmark_word = bookmarks_by_day[0]['bookmarks'][2]['from']
        rv = self.api_get('/get_known_words/de')
        known_words = json.loads(rv.data)
        known_words_count_before = len(known_words)
        assert not any(word['from'] == latest_bookmark_word for word in known_words)
        rv = self.api_post('/gym/create_new_exercise/Too easy/Recognize/10000/'+ str(latest_bookmark_id))
        rv = self.api_get('/get_known_words/de')
        known_words = json.loads(rv.data)
        assert any(word['word'] == latest_bookmark_word for word in known_words)
        assert known_words_count_before +1 == len(known_words)
        rv = self.api_post('/gym/create_new_exercise/Too easy/Recognize/10000/'+ str(second_latest_bookmark_id))
        rv = self.api_get('/get_known_words/de')
        known_words = json.loads(rv.data)
        assert any(word['word'] == latest_bookmark_word for word in known_words)
        assert any(word['word'] == second_latest_bookmark_word for word in known_words)
        assert known_words_count_before +1 == len(known_words)
        rv = self.api_post('/gym/create_new_exercise/Too easy/Recognize/10000/'+ str(third_latest_bookmark_id))
        rv = self.api_get('/get_known_words/de')
        known_words = json.loads(rv.data)
        assert known_words_count_before +2 == len(known_words)
        assert any(word['word'] == latest_bookmark_word for word in known_words)
        assert any(word['word'] == third_latest_bookmark_word for word in known_words)
        time.sleep(5) # delays for 5 seconds
        rv = self.api_post('/gym/create_new_exercise/Show solution/Recognize/10000/'+ str(third_latest_bookmark_id))
        rv = self.api_get('/get_known_words/de')
        known_words = json.loads(rv.data)
        assert not any(word['word'] == third_latest_bookmark_word for word in known_words)


    def test_get_learned_bookmarks(self):
        formData = dict(
            url='http://mir.lu',
            context='somewhere over the rainbowwwwwwwww')
        rv = self.api_post('/bookmark_with_context/de/sondern/en/but', formData)
        latest_bookmark_id = json.loads(rv.data)
        #rv = self.api_get('/bookmarks_by_day/with_context')
        #bookmarks_by_day = json.loads(rv.data)
        #latest_bookmark_id = bookmarks_by_day[0]['bookmarks'][0]['id']
        rv = self.api_get('/get_learned_bookmarks/de')
        learned_bookmarks = json.loads(rv.data)
        assert any(bookmark['id'] == latest_bookmark_id for bookmark in learned_bookmarks)
        learned_bookmarks_count = len(learned_bookmarks)
        formData = dict(
            url='http://mir.lu',
            context='chilling on the streets')
        rv = self.api_post('/bookmark_with_context/de/strassen/en/streets', formData)
        new_latest_bookmark_id = json.loads(rv.data)
        #rv = self.api_get('/bookmarks_by_day/with_context')
        #bookmarks_by_day = json.loads(rv.data)
        #new_latest_bookmark_id = bookmarks_by_day[0]['bookmarks'][1]['id']
        rv = self.api_get('/get_learned_bookmarks/de')
        learned_bookmarks = json.loads(rv.data)
        assert learned_bookmarks_count +1 == len(learned_bookmarks)
        assert any(bookmark['id'] == latest_bookmark_id for bookmark in learned_bookmarks)
        assert any(bookmark['id'] == new_latest_bookmark_id for bookmark in learned_bookmarks)
        self.api_post('/gym/create_new_exercise/Too easy/Recognize/10000/'+ str(latest_bookmark_id))
        rv = self.api_get('/get_learned_bookmarks/de')
        learned_bookmarks = json.loads(rv.data)
        assert not any(bookmark['id'] == latest_bookmark_id for bookmark in learned_bookmarks)
        assert learned_bookmarks_count== len(learned_bookmarks)
        time.sleep(5)
        self.api_post('/gym/create_new_exercise/Show solution/Recognize/10000/'+ str(latest_bookmark_id))
        rv = self.api_get('/get_learned_bookmarks/de')
        learned_bookmarks = json.loads(rv.data)
        assert learned_bookmarks_count+1== len(learned_bookmarks)
        assert any(bookmark['id'] == latest_bookmark_id for bookmark in learned_bookmarks)

    def test_get_not_looked_up_words(self):
        rv = self.api_get('/bookmarks_by_day/with_context')
        bookmarks_by_day = []
        bookmarks_by_day_with_date = json.loads(rv.data)
        rv = self.api_get('/get_not_looked_up_words/de')
        estimated_user_voc_before = json.loads(rv.data)
        assert not any (bookmark['word'] == 'es' for bookmark in estimated_user_voc_before)
        assert not any (bookmark['word'] == 'an' for bookmark in estimated_user_voc_before)
        assert not any (bookmark['word'] == 'auch' for bookmark in estimated_user_voc_before)
        for i in range(0, len(bookmarks_by_day_with_date)):
            for j in range (0, len(bookmarks_by_day_with_date[i]['bookmarks'])):
                bookmarks_by_day.append(bookmarks_by_day_with_date[i]['bookmarks'][j]['context'])
        for bookmark in bookmarks_by_day:
            bookmark_content_words = re.sub("[^\w]", " ",  bookmark).split()
        assert not 'es' in bookmark_content_words
        assert not 'an' in bookmark_content_words
        assert not 'auch' in bookmark_content_words
        formData = dict(
            url='http://mir.lu',
            context='es an auch')
        rv = self.api_post('/bookmark_with_context/de/auch/en/also', formData)
        rv = self.api_get('/get_not_looked_up_words/de')
        estimated_user_voc_after = json.loads(rv.data)
        assert len(estimated_user_voc_after)==len(estimated_user_voc_before)+2
        assert any (bookmark['word'] == 'es' for bookmark in estimated_user_voc_after)
        assert any (bookmark['word'] == 'an' for bookmark in estimated_user_voc_after)
        assert not any (bookmark['word'] == 'auch' for bookmark in estimated_user_voc_after)


    def test_set_language(self):
        rv = self.api_post('/learned_language/it')
        rv = self.api_post('/native_language/fr')
        assert "OK" in rv.data
        rv = self.api_get('/learned_language')
        assert rv.data== "it"
        rv = self.api_get('/native_language')
        assert rv.data== "fr"


    def test_available_languages(self):
        rv = self.api_get('/available_languages')
        print rv.data


    def test_create_user(self):
        formData = dict(
            username= "gigi",
            password= "lala"
        )
        rv = self.api_post('/add_user/i@i.la',formData)
        print rv.data
        assert rv.data > 1


    def test_get_language(self):
        rv = self.api_get('/learned_language')
        print rv.data

    def test_get_bookmarks_by_date(self):
        rv = self.api_get('/bookmarks_by_day/with_context')

        elements = json.loads(rv.data)
        some_date = elements[0]
        assert some_date ["date"]

        some_bookmark = some_date ["bookmarks"][0]
        for key in ["from", "to", "id", "context", "title", "url"]:
            assert key in some_bookmark

        # if we don't pass the context argument, we don't get
        # the context
        rv = self.api_get('/bookmarks_by_day/no_context')
        elements = json.loads(rv.data)
        some_date = elements[0]
        some_contrib = some_date ["bookmarks"][0]
        assert not "context" in some_contrib


    def test_password_hash(self):
        p1 = "test"
        p2 = "pass"
        user = User.find("i@mir.lu")

        hash1 = util.password_hash(p1,user.password_salt)
        hash2 = util.password_hash(p2, user.password_salt)
        assert hash1 != hash2

        assert user.authorize("i@mir.lu", "pass") != None


    def test_text_difficulty(self):
        formData = dict(
            text='der die das warum, wer nicht fragt bleibt dumm!',
            personalized='true',
            method='average')
        rv = self.api_post('/get_difficulty_for_text/de', formData)

        print 'difficulty: ' + rv.data
        assert 0.0 <= float(rv.data) <= 1.0


    def test_text_learnability(self):
        formData = dict(
            text='der die das besteht warum, wer nicht fragt bleibt jeweils sogar dumm!')
        rv = self.api_post('/get_learnability_for_text/de', formData)

        print 'learnability: ' + rv.data
        assert 0.0 <= float(rv.data) <= 1.0


if __name__ == '__main__':
    unittest.main()
