from unittest import TestCase

from mmcc_framework.framework import *
from mmcc_framework.nlu_adapters import NoNluAdapter


class TestFrameworkBehaviourOR(TestCase):
    @staticmethod
    def callback_getter(_):
        return lambda d, k, c: Response(k, c, True, choice=d["choice"] if "choice" in d else "")

    def setUp(self) -> None:
        self.my_framework = Framework(
            Process(first_activity_id="start",
                    activities=[Activity("start", "gateway", ActivityType.START),
                                Activity("gateway", "end", ActivityType.OR, ["xor", "par", "or"]),
                                Activity("xor", None, ActivityType.XOR, ["A", "B"]),
                                Activity("A", None, ActivityType.TASK),
                                Activity("B", None, ActivityType.TASK),
                                Activity("par", None, ActivityType.PARALLEL, ["C", "D"]),
                                Activity("C", None, ActivityType.TASK),
                                Activity("D", None, ActivityType.TASK),
                                Activity("or", None, ActivityType.OR, ["E", "F"]),
                                Activity("E", None, ActivityType.TASK),
                                Activity("F", None, ActivityType.END),
                                Activity("end", None, ActivityType.END)]),
            {"my_key": "a value"},
            {"ctx_key": "ctx value"},
            self.callback_getter,
            NoNluAdapter([]),
            lambda k: None)

    def test_path_1(self):
        path = [["", "gateway", []],
                ["xor", "xor", ["gateway"]],
                ["A", "A", ["gateway"]],
                ["", "gateway", ["gateway"]],
                ["par", "par", ["gateway"]],
                ["C", "C", ["gateway"]],
                ["", "par", ["gateway"]],
                ["D", "D", ["gateway", "par"]],
                ["", "par", ["gateway", "par"]],
                [None, "gateway", ["gateway"]],
                ["or", "or", ["gateway"]],
                ["E", "E", ["gateway", "or"]],
                ["", "or", ["gateway", "or"]],
                [None, "gateway", ["gateway"]],
                ["or", "or", ["gateway"]],
                ["F", "F", ["gateway", "or"]],
                ["", "F", ["gateway", "or"]]]
        for index, step in enumerate(path):
            self.my_framework.handle_data_input({"choice": step[0]} if step[0] != "" else {"data": "value"})
            self.assertEqual(self.my_framework._current.id, step[1], f"Step index when test failed: {index}, "
                                                                     f"expected: {step[1]}")
            self.assertEqual(self.my_framework._ctx[CTX_COMPLETED], step[2], f"Step index when test failed: {index}")

    def test_path_2(self):
        path = [["", "gateway", []],
                ["xor", "xor", ["gateway"]],
                ["B", "B", ["gateway"]],
                ["", "gateway", ["gateway"]],
                ["or", "or", ["gateway"]],
                ["E", "E", ["gateway", "or"]],
                ["", "or", ["gateway", "or"]],
                [None, "gateway", ["gateway"]],
                ["par", "par", ["gateway"]],
                ["D", "D", ["gateway"]],
                ["", "par", ["gateway"]],
                ["C", "C", ["gateway", "par"]],
                ["", "par", ["gateway", "par"]],
                ["D", "D", ["gateway", "par"]],
                ["", "par", ["gateway", "par"]],
                [None, "gateway", ["gateway"]],
                [None, "end", []],
                ["", "end", []]]
        for index, step in enumerate(path):
            self.my_framework.handle_data_input({"choice": step[0]} if step[0] != "" else {"data": "value"})
            self.assertEqual(self.my_framework._current.id, step[1], f"Step index when test failed: {index}, "
                                                                     f"expected: {step[1]}")
            self.assertEqual(self.my_framework._ctx[CTX_COMPLETED], step[2], f"Step index when test failed: {index}")


class TestFrameworkBehaviourPAR(TestCase):
    @staticmethod
    def callback_getter(_):
        return lambda d, k, c: Response(k, c, True, choice=d["choice"] if "choice" in d else "")

    def setUp(self) -> None:
        self.my_framework = Framework(
            Process(first_activity_id="start",
                    activities=[Activity("start", "gateway", ActivityType.START),
                                Activity("gateway", "end", ActivityType.PARALLEL, ["xor", "par", "or"]),
                                Activity("xor", None, ActivityType.XOR, ["A", "B"]),
                                Activity("A", None, ActivityType.TASK),
                                Activity("B", None, ActivityType.TASK),
                                Activity("par", None, ActivityType.PARALLEL, ["C", "D"]),
                                Activity("C", None, ActivityType.TASK),
                                Activity("D", None, ActivityType.TASK),
                                Activity("or", None, ActivityType.OR, ["E", "F"]),
                                Activity("E", None, ActivityType.TASK),
                                Activity("F", None, ActivityType.END),
                                Activity("end", None, ActivityType.END)]),
            {"my_key": "a value"},
            {"ctx_key": "ctx value"},
            self.callback_getter,
            NoNluAdapter([]),
            lambda k: None)

    def test_path_1(self):
        path = [["", "gateway", []],
                ["xor", "xor", []],
                ["A", "A", []],
                ["", "gateway", []],
                ["par", "par", []],
                ["C", "C", []],
                ["", "par", []],
                ["D", "D", ["par"]],
                ["", "par", ["par"]],
                [None, "gateway", []],
                ["or", "or", ["gateway"]],
                ["E", "E", ["gateway", "or"]],
                ["", "or", ["gateway", "or"]],
                [None, "gateway", ["gateway"]],
                ["or", "or", ["gateway"]],
                ["F", "F", ["gateway", "or"]],
                ["", "F", ["gateway", "or"]]]
        for index, step in enumerate(path):
            self.my_framework.handle_data_input({"choice": step[0]} if step[0] != "" else {"data": "value"})
            self.assertEqual(self.my_framework._current.id, step[1], f"Step index when test failed: {index}, "
                                                                     f"expected: {step[1]}")
            self.assertEqual(self.my_framework._ctx[CTX_COMPLETED], step[2], f"Step index when test failed: {index}")

    def test_path_2(self):
        path = [["", "gateway", []],
                ["xor", "xor", []],
                ["B", "B", []],
                ["", "gateway", []],
                ["or", "or", []],
                ["E", "E", ["or"]],
                ["", "or", ["or"]],
                [None, "gateway", []],
                ["par", "par", ["gateway"]],
                ["D", "D", ["gateway"]],
                ["", "par", ["gateway"]],
                ["C", "C", ["gateway", "par"]],
                ["", "par", ["gateway", "par"]],
                ["D", "D", ["gateway", "par"]],
                ["", "par", ["gateway", "par"]],
                [None, "gateway", ["gateway"]],
                [None, "end", []],
                ["", "end", []]]
        for index, step in enumerate(path):
            self.my_framework.handle_data_input({"choice": step[0]} if step[0] != "" else {"data": "value"})
            self.assertEqual(self.my_framework._current.id, step[1], f"Step index when test failed: {index}, "
                                                                     f"expected: {step[1]}")
            self.assertEqual(self.my_framework._ctx[CTX_COMPLETED], step[2], f"Step index when test failed: {index}")


class TestFrameworkBehaviourXOR(TestCase):
    @staticmethod
    def callback_getter(_):
        return lambda d, k, c: Response(k, c, True, choice=d["choice"] if "choice" in d else "")

    def setUp(self) -> None:
        self.my_framework = Framework(
            Process(first_activity_id="start",
                    activities=[Activity("start", "gateway", ActivityType.START),
                                Activity("gateway", "end", ActivityType.XOR, ["xor", "par", "or"]),
                                Activity("xor", None, ActivityType.XOR, ["A", "B"]),
                                Activity("A", None, ActivityType.TASK),
                                Activity("B", None, ActivityType.TASK),
                                Activity("par", None, ActivityType.PARALLEL, ["C", "D"]),
                                Activity("C", None, ActivityType.TASK),
                                Activity("D", None, ActivityType.TASK),
                                Activity("or", None, ActivityType.OR, ["E", "F"]),
                                Activity("E", None, ActivityType.TASK),
                                Activity("F", None, ActivityType.END),
                                Activity("end", None, ActivityType.END)]),
            {"my_key": "a value"},
            {"ctx_key": "ctx value"},
            self.callback_getter,
            NoNluAdapter([]),
            lambda k: None)

    def test_path_1a(self):
        path = [["", "gateway", []],
                ["xor", "xor", []],
                ["A", "A", []],
                ["", "end", []],
                ["", "end", []]]
        for index, step in enumerate(path):
            self.my_framework.handle_data_input({"choice": step[0]} if step[0] != "" else {"data": "value"})
            self.assertEqual(self.my_framework._current.id, step[1], f"Step index when test failed: {index}, "
                                                                     f"expected: {step[1]}")
            self.assertEqual(self.my_framework._ctx[CTX_COMPLETED], step[2], f"Step index when test failed: {index}")

    def test_path_1b(self):
        path = [["", "gateway", []],
                ["par", "par", []],
                ["C", "C", []],
                ["", "par", []],
                ["D", "D", ["par"]],
                ["", "par", ["par"]],
                [None, "end", []],
                ["", "end", []]]
        for index, step in enumerate(path):
            self.my_framework.handle_data_input({"choice": step[0]} if step[0] != "" else {"data": "value"})
            self.assertEqual(self.my_framework._current.id, step[1], f"Step index when test failed: {index}, "
                                                                     f"expected: {step[1]}")
            self.assertEqual(self.my_framework._ctx[CTX_COMPLETED], step[2], f"Step index when test failed: {index}")

    def test_path_1c(self):
        path = [["", "gateway", []],
                ["or", "or", []],
                ["F", "F", ["or"]],
                ["", "F", ["or"]]]
        for index, step in enumerate(path):
            self.my_framework.handle_data_input({"choice": step[0]} if step[0] != "" else {"data": "value"})
            self.assertEqual(self.my_framework._current.id, step[1], f"Step index when test failed: {index}, "
                                                                     f"expected: {step[1]}")
            self.assertEqual(self.my_framework._ctx[CTX_COMPLETED], step[2], f"Step index when test failed: {index}")

    def test_path_2a(self):
        path = [["", "gateway", []],
                ["par", "par", []],
                ["D", "D", []],
                ["", "par", []],
                ["C", "C", ["par"]],
                ["", "par", ["par"]],
                ["D", "D", ["par"]],
                ["", "par", ["par"]],
                [None, "end", []],
                ["", "end", []]]
        for index, step in enumerate(path):
            self.my_framework.handle_data_input({"choice": step[0]} if step[0] != "" else {"data": "value"})
            self.assertEqual(self.my_framework._current.id, step[1], f"Step index when test failed: {index}, "
                                                                     f"expected: {step[1]}")
            self.assertEqual(self.my_framework._ctx[CTX_COMPLETED], step[2], f"Step index when test failed: {index}")


class TestFramework(TestCase):
    @staticmethod
    def callback_getter(_):
        return lambda d, k, c: Response(k, c, True)

    def setUp(self) -> None:
        self.my_kb = {"my_key": "a value"}
        self.my_ctx = {"ctx_key": "ctx value"}
        self.my_callback = self.callback_getter
        self.my_nlu = NoNluAdapter([])
        self.my_save = lambda k: None

    def test_init(self):
        my_proc = Process([Activity("one", None, ActivityType.START)], "one")

        my_framework = Framework(my_proc, self.my_kb, self.my_ctx, self.my_callback, self.my_nlu, self.my_save)
        self.assertEqual(my_framework._process, my_proc)
        self.assertEqual(my_framework._kb, self.my_kb)
        self.assertEqual(my_framework._ctx, self.my_ctx)
        self.assertEqual(my_framework._callback_getter, self.my_callback)
        self.assertEqual(my_framework._nlu, self.my_nlu)
        self.assertEqual(my_framework._on_save, self.my_save)

    def test_init_dict(self):
        proc_dic = {
            "first_activity_id": "one",
            "activities": [{"my_id": "one", "next_id": None, "my_type": "task"}]
        }
        my_framework = Framework(proc_dic, self.my_kb, self.my_ctx, self.my_callback, self.my_nlu, self.my_save)
        self.assertEqual(my_framework._process.first.id, proc_dic["first_activity_id"])
        self.assertEqual(my_framework._process.activities[0].id, proc_dic["activities"][0]["my_id"])
        self.assertEqual(my_framework._process.activities[0].next_id, proc_dic["activities"][0]["next_id"])
        self.assertEqual(my_framework._process.activities[0].type.value, proc_dic["activities"][0]["my_type"])
        self.assertEqual(my_framework._kb, self.my_kb)
        self.assertEqual(my_framework._ctx, self.my_ctx)
        self.assertEqual(my_framework._callback_getter, self.my_callback)
        self.assertEqual(my_framework._nlu, self.my_nlu)
        self.assertEqual(my_framework._on_save, self.my_save)

    def test_init_callback(self):
        my_proc = Process([Activity("one", None, ActivityType.START)], "one")

        def proc_call():
            return my_proc

        def kb_call():
            return self.my_kb

        my_framework = Framework(proc_call, kb_call, self.my_ctx, self.my_callback, self.my_nlu, self.my_save)

        self.assertEqual(my_framework._process, my_proc)
        self.assertEqual(my_framework._kb, self.my_kb)
        self.assertEqual(my_framework._ctx, self.my_ctx)
        self.assertEqual(my_framework._callback_getter, self.my_callback)
        self.assertEqual(my_framework._nlu, self.my_nlu)
        self.assertEqual(my_framework._on_save, self.my_save)

    def test_init_callback_dict(self):
        proc_dic = {
            "first_activity_id": "one",
            "activities": [{"my_id": "one", "next_id": None, "my_type": "task"}]
        }

        def proc_call():
            return proc_dic

        def kb_call():
            return self.my_kb

        my_framework = Framework(proc_call, kb_call, self.my_ctx, self.my_callback, self.my_nlu, self.my_save)
        self.assertEqual(my_framework._process.first.id, proc_dic["first_activity_id"])
        self.assertEqual(my_framework._process.activities[0].id, proc_dic["activities"][0]["my_id"])
        self.assertEqual(my_framework._process.activities[0].next_id, proc_dic["activities"][0]["next_id"])
        self.assertEqual(my_framework._process.activities[0].type.value, proc_dic["activities"][0]["my_type"])
        self.assertEqual(my_framework._kb, self.my_kb)
        self.assertEqual(my_framework._ctx, self.my_ctx)
        self.assertEqual(my_framework._callback_getter, self.my_callback)
        self.assertEqual(my_framework._nlu, self.my_nlu)
        self.assertEqual(my_framework._on_save, self.my_save)


class TestResponse(TestCase):
    def setUp(self) -> None:
        self.my_kb = {"key": "value", "key2": "value2"}
        self.my_ctx = {"c key": "c value"}
        self.my_bool = True
        self.my_utt = "An utt"
        self.my_payload = {"payload": "payload value"}
        self.my_choice = "A choice"

    def test_init(self):
        my_response = Response(self.my_kb, self.my_ctx, self.my_bool, self.my_utt, self.my_payload, self.my_choice)

        self.assertEqual(my_response.kb, self.my_kb, "The kb is correctly saved")
        self.assertEqual(my_response.ctx, self.my_ctx, "The ctx is correctly saved")
        self.assertEqual(my_response.complete, self.my_bool, "Completed is correctly saved")
        self.assertEqual(my_response.utterance, self.my_utt, "The utterance is correctly saved")
        self.assertEqual(my_response.payload, self.my_payload, "The payload is correctly saved")
        self.assertEqual(my_response.choice, self.my_choice, "The choice is correctly saved")

    def test_init_with_default(self):
        my_response = Response(self.my_kb, self.my_ctx, self.my_bool)
        self.assertEqual(my_response.kb, self.my_kb, "The kb is correctly saved")
        self.assertEqual(my_response.ctx, self.my_ctx, "The ctx is correctly saved")
        self.assertEqual(my_response.complete, self.my_bool, "Completed is correctly saved")
        self.assertEqual(my_response.utterance, "", "The default utterance is empty")
        self.assertEqual(my_response.payload, {}, "The default payload is empty")
        self.assertIsNone(my_response.choice, "The default choice is None")

    def test_to_dict(self):
        my_dict = Response(self.my_kb, self.my_ctx, self.my_bool, self.my_utt, self.my_payload,
                           self.my_choice).to_dict()

        self.assertEqual(my_dict["utterance"], self.my_utt, "The utterance is correctly passed to the dict")
        self.assertEqual(my_dict["payload"], self.my_payload, "The payload is correctly passed to the dict")

    def test_to_dict_with_default(self):
        my_dict = Response(self.my_kb, self.my_ctx, self.my_bool).to_dict()

        self.assertEqual(my_dict["utterance"], "", "The utterance is correctly passed to the dict")
        self.assertEqual(my_dict["payload"], {}, "The payload is correctly passed to the dict")

    def test_add_utterance(self):
        my_response = Response(self.my_kb, self.my_ctx, self.my_bool, self.my_utt, self.my_payload, self.my_choice)
        my_response.add_utterance(self.my_kb, "key")
        self.assertEqual(my_response.utterance, self.my_utt + "\n" + self.my_kb["key"])

        my_response = Response(self.my_kb, self.my_ctx, self.my_bool, self.my_utt, self.my_payload, self.my_choice)
        my_response.add_utterance(self.my_kb, "key3", "def")
        self.assertEqual(my_response.utterance, self.my_utt + "\n" + "def")

        my_response = Response(self.my_kb, self.my_ctx, self.my_bool, self.my_utt, self.my_payload, self.my_choice)
        my_response.add_utterance(self.my_kb, "key3")
        self.assertEqual(my_response.utterance, self.my_utt)

        my_response = Response(self.my_kb, self.my_ctx, self.my_bool)
        my_response.add_utterance(self.my_kb, "key")
        self.assertEqual(my_response.utterance, self.my_kb["key"])


class TestProcess(TestCase):
    def test_init(self):
        my_activities = [Activity("one", "two", ActivityType.TASK),
                         Activity("two", None, ActivityType.OR, choices=["one"])]
        my_process = Process(my_activities, "one")
        self.assertEqual(my_process.activities, my_activities, "The activities are saved")
        self.assertEqual(my_process.first, my_activities[0], "The first activity is saved")

    def test_init_with_dict(self):
        my_activities = [Activity("one", "two", ActivityType.TASK),
                         Activity("two", None, ActivityType.OR, choices=["one"])]
        my_dicts = [
            {"my_id": my_activities[0].id, "next_id": my_activities[0].next_id, "my_type": my_activities[0].type.value},
            {"my_id": my_activities[1].id, "next_id": my_activities[1].next_id, "my_type": my_activities[1].type.value,
             "choices": my_activities[1].choices}]
        my_process = Process(my_dicts, "one")
        self.assertEqual(my_process.activities, my_activities, "The activities are saved")
        self.assertEqual(my_process.first, my_activities[0], "The first activity is saved")

    def test_init_with_missing_first(self):
        with self.assertRaises(DescriptionException, msg="Raise if first activity id has no corresponding activity"):
            Process([Activity("one", None, ActivityType.TASK)], "two")

    def test_from_dict(self):
        my_activities = [Activity("one", "two", ActivityType.TASK),
                         Activity("two", None, ActivityType.OR, choices=["one"])]
        my_dict = {
            "activities": [
                {"my_id": my_activities[0].id, "next_id": my_activities[0].next_id,
                 "my_type": my_activities[0].type.value},
                {"my_id": my_activities[1].id, "next_id": my_activities[1].next_id,
                 "my_type": my_activities[1].type.value,
                 "choices": my_activities[1].choices}], "first_activity_id": my_activities[0].id
        }
        my_process = Process.from_dict(my_dict)
        self.assertEqual(my_process.activities, my_activities, "The activities are correctly set")
        self.assertEqual(my_process.first, my_activities[0], "The first activity is correctly set")

    def test_from_dict_shuffled(self):
        my_activities = [Activity("one", "two", ActivityType.TASK),
                         Activity("two", None, ActivityType.OR, choices=["one"])]
        my_dict = {
            "first_activity_id": my_activities[0].id,
            "activities": [
                {"my_id": my_activities[0].id, "next_id": my_activities[0].next_id,
                 "my_type": my_activities[0].type.value},
                {"my_id": my_activities[1].id, "next_id": my_activities[1].next_id,
                 "my_type": my_activities[1].type.value, "choices": my_activities[1].choices}]
        }
        my_process = Process.from_dict(my_dict)
        self.assertEqual(my_process.activities, my_activities, "The activities are correctly set")
        self.assertEqual(my_process.first, my_activities[0], "The first activity is correctly set")

    def test_from_dict_with_wrong_params(self):
        with self.assertRaises(DescriptionException, msg="If necessary params are missing, raise. activities"):
            Process.from_dict({"first_activity_id": "one"})

        with self.assertRaises(DescriptionException, msg="If necessary params are missing, raise. first id"):
            Process.from_dict({"activities": [{"my_id": "one", "next_id": "two", "my_type": "task"}]})

        with self.assertRaises(DescriptionException, msg="With more params than needed, raise"):
            Process.from_dict(
                {"activities": [{"my_id": "one", "next_id": "two", "my_type": "task"}], "first_activity_id": "one",
                 "other": True})

    def test_check_first_with_more_correspondences(self):
        with self.assertRaises(DescriptionException, msg="Raise if first activity id has more correspondences"):
            Process([Activity("one", None, ActivityType.TASK),
                     Activity("one", None, ActivityType.TASK)], "one")

    def test_check_exists_unique_next_id(self):
        with self.assertRaises(DescriptionException, msg="Raise if a next id is not unique"):
            Process([Activity("one", "two", ActivityType.TASK),
                     Activity("two", None, ActivityType.TASK),
                     Activity("two", None, ActivityType.TASK)], "one")

        with self.assertRaises(DescriptionException, msg="Raise if a next id is not found"):
            Process([Activity("one", "two", ActivityType.TASK)], "one")

    def test_check_next_id_is_not_self(self):
        with self.assertRaises(DescriptionException, msg="Raise if a next id is equal to id"):
            Process([Activity("one", "one", ActivityType.TASK)], "one")

    def test_check_exists_unique_choices(self):
        with self.assertRaises(DescriptionException, msg="Raise if a choice is not unique"):
            Process([Activity("one", None, ActivityType.OR, ["two"]),
                     Activity("two", None, ActivityType.TASK),
                     Activity("two", None, ActivityType.TASK)], "one")

        with self.assertRaises(DescriptionException, msg="Raise if a choice is not found"):
            Process([Activity("one", None, ActivityType.OR, ["two"])], "one")

    def test_check_choice_not_allowed(self):
        with self.assertRaises(DescriptionException, msg="Raise if a choice is None"):
            Process([Activity("one", None, ActivityType.OR, ["two", None]),
                     Activity("two", None, ActivityType.TASK)], "one")

        with self.assertRaises(DescriptionException, msg="Raise if a choice is the same as the id"):
            Process([Activity("one", None, ActivityType.OR, ["one"])], "one")

        with self.assertRaises(DescriptionException, msg="Raise if a choice contains duplicates"):
            Process([Activity("one", None, ActivityType.OR, ["two", "two"]),
                     Activity("two", None, ActivityType.TASK)], "one")


class TestActivity(TestCase):
    def setUp(self) -> None:
        self.my_id = "my id"
        self.next_id = "next id"
        self.choices = ["a", "b", "c"]
        self.value = {}

    def test_init(self):
        for t in ActivityType:
            self.value[t] = Activity(self.my_id, self.next_id, t,
                                     self.choices if t in ActivityType.get_require_choice() else None)

        for t in ActivityType:
            self.assertEqual(self.value[t].id, self.my_id, "The id is correctly set")
            self.assertEqual(self.value[t].next_id, self.next_id, "The next id is correctly set")
            self.assertEqual(self.value[t].type, t, "The type is correctly set")
            self.assertEqual(self.value[t].choices, self.choices if t in ActivityType.get_require_choice() else None,
                             "The choices are correctly set")

    def test_init_with_type_from_text(self):
        for t in ActivityType:
            self.value[t] = Activity(self.my_id, self.next_id, t.value,
                                     self.choices if t in ActivityType.get_require_choice() else None)

        for t in ActivityType:
            self.assertEqual(self.value[t].id, self.my_id, "The id is correctly set")
            self.assertEqual(self.value[t].next_id, self.next_id, "The next id is correctly set")
            self.assertEqual(self.value[t].type, t, "The type is correctly casted and set")
            self.assertEqual(self.value[t].choices, self.choices if t in ActivityType.get_require_choice() else None,
                             "The choices are correctly set")

    def test_init_with_wrong_choices(self):
        for t in ActivityType:
            with self.assertRaises(DescriptionException, msg="If wrong choices are provided, should raise exception"):
                Activity(self.my_id, self.next_id, t, None if t in ActivityType.get_require_choice() else self.choices)

    def test_init_with_wrong_type(self):
        with self.assertRaises(KeyError, msg="If the type is wrong, should raise an exception"):
            Activity(self.my_id, self.next_id, "no_type")

    def test_from_dict(self):
        for t in ActivityType:
            my_dict = {"my_id": self.my_id, "next_id": self.next_id, "my_type": t.value}
            if t in ActivityType.get_require_choice():
                my_dict["choices"] = self.choices
            self.value[t] = Activity.from_dict(my_dict)

        for t in ActivityType:
            self.assertEqual(self.value[t].id, self.my_id, "The id is correctly set")
            self.assertEqual(self.value[t].next_id, self.next_id, "The next id is correctly set")
            self.assertEqual(self.value[t].type, t, "The type is correctly set")
            self.assertEqual(self.value[t].choices, self.choices if t in ActivityType.get_require_choice() else None,
                             "The choices are correctly set")

    def test_from_dict_shuffled(self):
        for t in ActivityType:
            my_dict = {"next_id": self.next_id, "my_id": self.my_id, }
            if t in ActivityType.get_require_choice():
                my_dict["choices"] = self.choices
            my_dict["my_type"] = t.value
            self.value[t] = Activity.from_dict(my_dict)

        for t in ActivityType:
            self.assertEqual(self.value[t].id, self.my_id, "The id is correctly set")
            self.assertEqual(self.value[t].next_id, self.next_id, "The next id is correctly set")
            self.assertEqual(self.value[t].type, t, "The type is correctly set")
            self.assertEqual(self.value[t].choices, self.choices if t in ActivityType.get_require_choice() else None,
                             "The choices are correctly set")

    def test_from_dict_with_wrong_params(self):
        with self.assertRaises(DescriptionException, msg="If necessary params are missing, raise. my_id"):
            Activity.from_dict(
                {"next_id": self.next_id, "my_type": ActivityType.XOR, "choices": self.choices})

        with self.assertRaises(DescriptionException, msg="If necessary params are missing, raise. next_id"):
            Activity.from_dict(
                {"my_id": self.my_id, "my_type": ActivityType.XOR, "choices": self.choices})

        with self.assertRaises(DescriptionException, msg="If necessary params are missing, raise. my_type"):
            Activity.from_dict(
                {"my_id": self.my_id, "next_id": self.next_id, "choices": self.choices})

        with self.assertRaises(DescriptionException, msg="With more params than needed, raise"):
            Activity.from_dict(
                {"my_id": self.my_id, "next_id": self.next_id, "my_type": ActivityType.XOR, "choices": self.choices,
                 "other": True})

    def test_eq_ne(self):
        subject = Activity(self.my_id, self.next_id, ActivityType.TASK)
        equal = Activity(self.my_id, self.next_id, ActivityType.TASK)
        diff_id = Activity("different", self.next_id, ActivityType.TASK)
        diff_next = Activity(self.my_id, "different", ActivityType.TASK)
        diff_type = Activity(self.my_id, self.next_id, ActivityType.OR, self.choices)
        subject_choices = Activity(self.my_id, self.next_id, ActivityType.OR, ["a"])

        self.assertEqual(subject, subject, "Activity should be equal to itself")
        self.assertEqual(subject, equal, "Activities with same attributes should be equal")
        self.assertNotEqual(subject, diff_id, "Activities with different id should not be equal")
        self.assertNotEqual(subject, diff_next, "Activities with different next id should not be equal")
        self.assertNotEqual(subject, diff_type, "Activities with different type should not be equal")
        self.assertNotEqual(subject_choices, diff_type, "Activities with different choices should not be equal")


class TestDescriptionException(TestCase):
    def setUp(self) -> None:
        self.cause = "cause"
        self.message = "message"
        self.value = DescriptionException(self.cause, self.message)

    def test_init(self):
        self.assertIs(self.value.cause, self.cause, "The cause is correctly set")
        self.assertIs(self.value.args[0], self.message, "The message is correctly set")

    def test_str(self):
        self.assertEqual(self.value.__str__(), f"{self.message} The cause of the exception was: {self.cause}")


class TestCallbackException(TestCase):
    def setUp(self) -> None:
        self.cause = "cause"
        self.message = "message"
        self.value = CallbackException(self.cause, self.message)

    def test_init(self):
        self.assertIs(self.value.cause, self.cause, "The cause is correctly set")
        self.assertIs(self.value.args[0], self.message, "The message is correctly set")

    def test_str(self):
        self.assertEqual(self.value.__str__(), f"{self.message} The parameter of the function was: {self.cause}")
