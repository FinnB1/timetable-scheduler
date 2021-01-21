import comedian
import demographic
import ReaderWriter
import timetable
import random
import math


class task2_scheduler:

    def __init__(self, comedian_List, demographic_List):
        self.comedian_List = comedian_List
        self.demographic_List = demographic_List

    def prune(self, comedian, matches):
        for match in matches:
            if comedian in matches[match]:
                matches[match].remove(comedian)
        return matches

    slots = [
        [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10],
        [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [1, 10],
        [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9], [2, 10],
        [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8], [3, 9], [3, 10],
        [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7], [4, 8], [4, 9], [4, 10],
        ]

    # change to python _   case
    def next_slot(self, slot):
        self.slots.remove(slot)
        if len(self.slots) > 0:
            return self.slots[0]

    def sort_dict(self, dict):
        keysort = sorted(dict, key=lambda demographic: len(dict[demographic]))
        new_dict = {}
        for i in range(0, len(keysort)):
            new_dict[keysort[i]] = dict[keysort[i]]
        return new_dict

    def check_constraints(self, comedian, main_assignments, test_assignments, day):
        count = 0
        day_hours = 0
        for a in main_assignments:
            if comedian == main_assignments[a]:
                if a[0] == day:
                    return False
                count += 2
        for a in test_assignments:
            if comedian == test_assignments[a]:
                count += 1
                if a[0] == day:
                    day_hours += 1
        if count > 3 or day_hours > 1:
            return False
        return True

    def uses(self, comedian, assigned):
        for a in assigned:
            if assigned[a] == comedian:
                pass

    def forward_check(self, comedian, matches, index):
        skip = True
        for group in matches:
            if group == index and skip:
                skip = False
            if skip:
                continue
            if len(matches[group]) == 1:
                print(matches[group])
                return False
        return True


    # This simplistic approach merely assigns each demographic and comedian to a random, iterating through the
    # timetable.
    def schedule(self, timetableObj):
        slot = [0, 1]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        # put in init
        main = {}
        test = {}
        for demographic in self.demographic_List:
            main[demographic] = []
            test[demographic] = []
            for comedian in self.comedian_List:
                match_main = True
                match_test = False
                for topic in demographic.topics:
                    if topic not in comedian.themes:
                        match_main = False
                    elif topic in comedian.themes:
                        match_test = True
                        
                if match_main:
                    main[demographic].append(comedian)
                elif match_test:
                    test[demographic].append(comedian)

        main_assigned = {}
        test_assigned = {}

        main = self.sort_dict(main)


        for group in main:
            selected = 0
            comedian = main[group][selected]
            if len(main[group]) < 2:
                while not self.check_constraints(comedian, main_assigned, test_assigned, slot[0]):
                    slot = self.slots[self.slots.index(slot)+1]
            while not self.check_constraints(comedian, main_assigned, test_assigned, slot[0]) and selected < len(main[group]) -1:
                selected += 1
                comedian = main[group][selected]
            # Maybe use a stack in case a comedian is used twice you can backtrack and use a different one
            timetableObj.addSession(days[slot[0]], slot[1], comedian, group, "main")
            main_assigned[tuple(slot)] = comedian
            print("assigning " + comedian.name + " to " + days[slot[0]])
            slot = self.next_slot(slot)


        for group in test:
            selected = 0
            comedian = test[group][selected]
            while not self.check_constraints(comedian, main_assigned, test_assigned, slot[0]) and selected < len(test[group]) - 1:
                selected += 1
                comedian = test[group][selected]
            # Maybe use a stack in case a comedian is used twice you can backtrack and use a different one
            timetableObj.addSession(days[slot[0]], slot[1], comedian, group, "test")
            test_assigned[tuple(slot)] = comedian
            print("TEST assigning " + comedian.name + " to " + days[slot[0]])
            slot = self.next_slot(slot)
        return timetableObj
