import comedian
import demographic
import ReaderWriter
import timetable
import random
import math


class task1_scheduler:

    def __init__(self, comedian_list, demographic_list):
        self.comedian_List = comedian_list
        self.demographic_List = demographic_list
        self.slots = [
            [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5],
            [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5],
            [4, 1], [4, 2], [4, 3], [4, 4], [4, 5]
        ]
        self.assigned = {}

    def next_slot(self, slot):
        self.slots.remove(slot)
        if len(self.slots) > 0:
            return self.slots[0]

    def sort_dict(self, dictionary):
        sorted_keys = sorted(dictionary, key=lambda demographic: len(dictionary[demographic]))
        new_dict = {}
        for i in range(0, len(sorted_keys)):
            new_dict[sorted_keys[i]] = dictionary[sorted_keys[i]]
        return new_dict

    def check_constraints(self, comedian, day):
        count = 0
        for a in self.assigned:
            if comedian == self.assigned[a]:
                if a[0] == day:
                    return False
                day = a[0]
                count += 1
        if count > 1:
            return False
        return True

    # This simplistic approach merely assigns each demographic and comedian to a random, iterating through the
    # timetable.
    def schedule(self, timetable_obj):
        slot = [0, 1]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        matches = {}
        for demo in self.demographic_List:
            matches[demo] = []
            for com in self.comedian_List:
                match = True
                for topic in demo.topics:
                    if topic not in com.themes:
                        match = False
                        break
                if match:
                    matches[demo].append(com)

        matches = self.sort_dict(matches)

        for group in matches:
            selected = 0
            selected_comedian = matches[group][selected]
            if len(matches[group]) == 1:
                while not self.check_constraints(selected_comedian, slot[0]):
                    slot = self.slots[self.slots.index(slot) + 1]
            while not self.check_constraints(selected_comedian, slot[0]) and selected < len(matches[group]) - 1:
                selected += 1
                selected_comedian = matches[group][selected]
            timetable_obj.addSession(days[slot[0]], slot[1], selected_comedian, group, "main")
            self.assigned[tuple(slot)] = selected_comedian
            # print("assigning " + comedian.name + " to " + days[slot[0]])
            slot = self.next_slot(slot)
        return timetable_obj
