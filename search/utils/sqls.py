
def select_details_of_word(word: str) -> str:
  return f"""
            SELECT words, title, `text`, (
                SELECT url
                FROM `url`
                WHERE `url`.`id`=`text`.`url_id`
            ) as url
            FROM `text`, `words`
                WHERE `text`.`words_id`=`words`.`id`
                  AND LOCATE('{word}',words.words) > 0
            """


def select_relate_tags() -> str:
  return """
            SELECT `tag_name`, `words`
            FROM tag, words, words_tag
            WHERE 
              words.id=words_tag.words_id
              AND tag.id=words_tag.tag_id
              AND LOCATE('a', words.words) > 0
        """


def select_relate_words(word: str) -> str:
  return f"""
            SELECT words
            FROM words
            # WHERE LOCATE('{word}', words.words) > 0
            WHERE words.words LIKE '%{word}%'
        """