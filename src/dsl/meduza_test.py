import unittest

from src.dsl.commands.db import *
from src.dsl.commands.sln import *
from src.etc.driver import make_eager_driver
from src.dsl.model.Action import Action
from src.dsl.model.Actions import Actions
from src.dsl.model.Iterate import Iterate


class MeduzaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        context = {
            "driver": make_eager_driver(),
            "selector": "a.Link-root.Link-isInBlockTitle",
            "timeout": 10,
            "attr_text": "text",
            "attr_href": "href",
            "url": "https://meduza.io/",
        }

        # Define a mock schema with required attributes
        actions = Actions(actions=[Action(name="Get page", command=get_page),
                                   Action(name="Find all", command=find_all, result_to="elements"),
                                   Action(name="Get text", command=get_attr, input_mapping={"data": "elements", "attr": "attr_text"}, result_to="output_texts"),
                                   Action(name="Get hrefs", command=get_attr, input_mapping={"data": "elements", "attr": "attr_href"}, result_to="output_hrefs")],
                          context=context)

        context, fails = actions.do()
        cls.context = context
        cls.fails = fails

    @classmethod
    def tearDownClass(cls) -> None:
        db = cls.context.get("db")
        if db is not None:
            db.close()

        if os.path.exists(cls.context.get("db_name")):
            try:
                os.remove(cls.context.get("db_name"))
            except OSError:
                pass

    def test_get_main_page_elements(self):
        # Assertions
        self.assertEqual(self.fails, [])
        self.assertIsNotNone(self.context.get("output_texts"))
        self.assertIsNotNone(self.context.get("output_hrefs"))
        self.assertEqual(len(self.context.get("output_texts")), len(self.context.get("output_hrefs")))
        self.assertEqual("a", self.context.get("elements")[0].tag_name)

    def test_write_to_db(self):
        context = self.context
        context.update({
            "db_name": "test.db",
            "schema": "CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL, href TEXT NOT NULL);",
            "insert_query": "INSERT INTO test (text, href) VALUES ('?', '?')",
            "values": ["output_texts", "output_hrefs"],
        })
        actions = Actions(actions=[Action(name="Create db",
                                          command=create_database),
                                   Action(name="Create db",
                                          command=get_database,
                                          result_to="db"),
                                   Action(name="Write to db",
                                          command=insert,
                                          input_mapping={"query_template": "insert_query"})
                                   ],
                          context=self.context)
        context, fails = actions.do()
        self.assertEqual(fails, [])

        context["count_query"] = "SELECT COUNT(*) FROM test"
        actions = Actions(actions=[Action(name="Write to db",
                                          command=execute_query_results,
                                          input_mapping={"query": "count_query"},
                                          result_to="count")
                                   ],
                          context=context)
        context, fails = actions.do()
        self.assertEqual(fails, [])
        self.assertIsNotNone(context.get("count"))
        self.assertNotEqual(context.get("count"), 0)

    def test_iterate(self):
        context = self.context
        actions = Actions(actions=[
            Iterate(context=context, iterator="output_hrefs", actions=Actions([
                Action(name="follow hrefs",
                       command=get_page,
                       input_mapping={"url": "output_hrefs"}),
                Action(name="find article text",
                       command=find_all,
                       input_mapping={"selector": "article_text_selector"},
                       context={"article_text_selector": ".GeneralMaterial-article"},
                       result_to="article_texts",
                       ),
                Action(name="get text",
                       command=get_attr,
                       input_mapping={"data": "article_texts", "attr": "attr_text"},
                       result_to="article_texts",
                       )])
                    )])

        context, fails = actions.do()
        self.assertEqual(fails, [])
        texts = context.get("article_texts")
        print([v[:100] for v in texts], sep="*"*100+"\n")


if __name__ == '__main__':
    unittest.main()
