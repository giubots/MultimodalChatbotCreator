# (C) Copyright 2020 Giulio Antonio Abbo, Pier Carlo Cadoppi, Davide Savoldelli.
# All rights reserved.
# This file is part of the "Multimodal chatbot creator" project.
#
# Author: Giulio Antonio Abbo
from unittest import TestCase

from framework import *


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

    def test_check(self):
        pass  # TODO implement tests here


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
