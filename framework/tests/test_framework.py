# (C) Copyright 2020 Giulio Antonio Abbo, Pier Carlo Cadoppi, Davide Savoldelli.
# All rights reserved.
# This file is part of the "Multimodal chatbot creator" project.
#
# Author: Giulio Antonio Abbo
from unittest import TestCase

from mccreator_framework.framework import *


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
