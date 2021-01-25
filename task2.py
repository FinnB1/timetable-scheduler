import comedian
import demographic
import ReaderWriter
import timetable
import random
import math


class task2_scheduler:

    def __init__(self, comedian_list, demographic_list):
        self.comedian_list = comedian_list
        self.demographic_list = demographic_list
        self.slots = [
            [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10],
            [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [1, 10],
            [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9], [2, 10],
            [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8], [3, 9], [3, 10],
            [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7], [4, 8], [4, 9], [4, 10],
        ]
        self.main_assigned = {}
        self.test_assigned = {}

    def next_slot(self, slot):
        self.slots.remove(slot)
        if len(self.slots) > 0:
            return self.slots[0]

    @staticmethod
    def sort_dict(dictionary):
        sorted_keys = sorted(dictionary, key=lambda demographic: len(dictionary[demographic]))
        new_dict = {}
        for i in range(0, len(sorted_keys)):
            new_dict[sorted_keys[i]] = dictionary[sorted_keys[i]]
        return new_dict

    def check_constraints(self, selected_comedian, day):
        count = 0
        day_hours = 0
        for a in self.main_assigned:
            if selected_comedian == self.main_assigned[a]:
                if a[0] == day:
                    return False
                count += 2
        for a in self.test_assigned:
            if selected_comedian == self.test_assigned[a]:
                count += 1
                if a[0] == day:
                    day_hours += 1
        if count > 3 or day_hours > 1:
            return False
        return True

    # This simplistic approach merely assigns each demographic and comedian to a random, iterating through the
    # timetable.
    def schedule(self, timetable_obj):
        slot = [0, 1]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        main = {}
        test = {}
        for demo in self.demographic_list:
            main[demo] = []
            test[demo] = []
            for com in self.comedian_list:
                match_main = True
                match_test = False
                for topic in demo.topics:
                    if topic not in com.themes:
                        match_main = False
                    elif topic in com.themes:
                        match_test = True

                if match_main:
                    main[demo].append(com)
                elif match_test:
                    test[demo].append(com)

        main = self.sort_dict(main)

        for group in main:
            selected = 0
            selected_comedian = main[group][selected]
            if len(main[group]) < 2:
                while not self.check_constraints(selected_comedian, slot[0]):
                    slot = self.slots[self.slots.index(slot) + 1]
            while not self.check_constraints(selected_comedian, slot[0]) and selected < len(main[group]) - 1:
                selected += 1
                selected_comedian = main[group][selected]
            # Maybe use a stack in case a comedian is used twice you can backtrack and use a different one
            timetable_obj.addSession(days[slot[0]], slot[1], selected_comedian, group, "main")
            self.main_assigned[tuple(slot)] = selected_comedian
            # print("assigning " + comedian.name + " to " + days[slot[0]] + " show type: Main")
            slot = self.next_slot(slot)

        for group in test:
            selected = 0
            selected_comedian = test[group][selected]
            while not self.check_constraints(selected_comedian, slot[0]) and selected < len(test[group]) - 1:
                selected += 1
                selected_comedian = test[group][selected]
            # Maybe use a stack in case a comedian is used twice you can backtrack and use a different one
            timetable_obj.addSession(days[slot[0]], slot[1], selected_comedian, group, "test")
            self.test_assigned[tuple(slot)] = selected_comedian
            # print("Assigning " + comedian.name + " to " + days[slot[0]] + " show type: Test")
            slot = self.next_slot(slot)
        return timetable_obj
