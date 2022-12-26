import pymysql
import pymysql.cursors
import pandas as pd
from tqdm import tqdm

tqdm.pandas()


class DatabaseSearcher:

    def __init__(self) -> None:    
        self.db = pymysql.connect(host='localhost',
                                    user='root',
                                    password="PASSWORT",
                                    database='AlbanianCorpora',
                                    cursorclass=pymysql.cursors.DictCursor)
        
        self.all_data = self.get_all_data()
        self.all_data['color']='black'
        #self.all_data['context'] = self.all_data.token_order.progress_apply(lambda x: self.get_context(x))
        
        
    def get_all_data(self):
        self.cursor = self.db.cursor()
        sql = "SELECT * FROM dialect_corpus"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return pd.DataFrame(results)

    
    def search_words(self, word):
        self.cursor = self.db.cursor()
        sql = "SELECT token_order FROM dialect_corpus ac WHERE ac.Form="+"'"+word+"'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results)>0:
            results = pd.DataFrame(results)
            return results.token_order.tolist()
        else:
            return []

    def search_lemma(self, lemma):
        self.cursor = self.db.cursor()
        sql = "SELECT token_order FROM dialect_corpus ac WHERE ac.Lemma="+"'"+lemma+"'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results)>0:
            results = pd.DataFrame(results)
            return results.token_order.tolist()
        else:
            return []

    def search_upostag(self, UPosTag):
        self.cursor = self.db.cursor()
        sql = "SELECT token_order FROM dialect_corpus ac WHERE ac.UPosTag="+"'"+UPosTag+"'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results)>0:
            results = pd.DataFrame(results)
            return results.token_order.tolist()
        else:
            return []
    
    def search_deprel(self, DepRel):
        self.cursor = self.db.cursor()
        sql = "SELECT token_order FROM dialect_corpus ac WHERE ac.DepRel="+"'"+DepRel+"'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results)>0:
            results = pd.DataFrame(results)
            return results.token_order.tolist()
        else:
            return []

    def search_xpostag(self, XPosTag):
        self.cursor = self.db.cursor()
        sql = "SELECT token_order FROM dialect_corpus ac WHERE ac.XPosTag="+"'"+XPosTag+"'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results)>0:
            results = pd.DataFrame(results)
            return results.token_order.tolist()
        else:
            return []

    def search_basic_word_order(self, basic_word_order):
        self.cursor = self.db.cursor()
        sql = "SELECT token_order FROM dialect_corpus ac WHERE ac.basic_word_order="+"'"+basic_word_order+"'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results)>0:
            results = pd.DataFrame(results)
            return sorted(list(results.token_order.unique()))
        else:
            return []
    
    def search_main_sub(self, main_sub):
        self.cursor = self.db.cursor()
        sql = "SELECT token_order FROM dialect_corpus ac WHERE ac.main_sub="+"'"+main_sub+"'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results)>0:
            results = pd.DataFrame(results)
            return sorted(list(results.token_order.unique()))
        else:
            return []
    
    def search_dialect(self, dialect):
        self.cursor = self.db.cursor()
        sql = "SELECT token_order FROM dialect_corpus ac WHERE ac.dialect="+"'"+dialect+"'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results)>0:
            results = pd.DataFrame(results)
            return results.token_order.tolist()
        else:
            return []

    def search_country(self, country):
        self.cursor = self.db.cursor()
        sql = "SELECT token_order FROM dialect_corpus ac WHERE ac.country="+"'"+country+"'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results)>0:
            results = pd.DataFrame(results)
            return results.token_order.tolist()
        else:
            return []

    def search_tense(self, tense):
        self.cursor = self.db.cursor()
        sql = "SELECT token_order FROM dialect_corpus ac WHERE ac.tense="+"'"+tense+"'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results)>0:
            results = pd.DataFrame(results)
            return results.token_order.tolist()
        else:
            return []
    
    def search_case(self, case):
        self.cursor = self.db.cursor()
        sql = "SELECT token_order FROM dialect_corpus ac WHERE ac.`case`="+"'"+case+"'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results)>0:
            results = pd.DataFrame(results)
            return results.token_order.tolist()
        else:
            return []

    def search_number(self, number):
        self.cursor = self.db.cursor()
        sql = "SELECT token_order FROM dialect_corpus ac WHERE ac.number="+"'"+number+"'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results)>0:
            results = pd.DataFrame(results)
            return results.token_order.tolist()
        else:
            return []

    def search_by_token_order(self, token_orders):
        token_orders = [str(c) for c in token_orders]
        self.cursor = self.db.cursor()
        sql = "SELECT * FROM dialect_corpus ac WHERE ac.token_order "+"IN("+','.join(token_orders)+")"
        #print(sql)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        results = pd.DataFrame(results)
        return results

    def map_key_to_function(self, key):
        
        ['input_word_search', 'input_lemma_search', 'input_basic_word_order_search', 'input_dialect_search', 'input_country_search']

        key_function_mapper = {
            "input_word_search": self.search_words,
            "input_lemma_search": self.search_lemma,
            "input_basic_word_order_search": self.search_basic_word_order,
            "input_dialect_search": self.search_dialect,
            "input_country_search": self.search_country,
            "input_upostag_search": self.search_upostag,
            "input_xpostag_search": self.search_xpostag,
            "input_deprel_search": self.search_deprel,
            "input_main_sub_search": self.search_main_sub,
            "input_case_search":self.search_case,
            "input_tense_search": self.search_tense,
            "input_number_search": self.search_number
        }

        if key in key_function_mapper.keys():
            return key_function_mapper[key]
    
    
    def process_input(self, search_function, input):

        if input:
            db_results = search_function(input)
            return db_results
        else:
            return None

    def process_input_json(self, input_json):
        
        id_list = []

        for key in input_json.keys():
            function = self.map_key_to_function(key)
            if function is not None:
                result = self.process_input(function, input_json[key])
                if result is not None:
                    id_list.append(result)
        if len(id_list)>0:
            id_list = list(set.intersection(*map(set,id_list)))

        return id_list
    
    def get_query_results(self, input_json):

        id_list = self.process_input_json(input_json)

        results =  self.search_by_token_order(id_list)

        return results.to_dict(orient="records")

