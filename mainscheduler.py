import comedian
import demographic
import ReaderWriter
import timetable
import random
import math


class mainscheduler:

    def __init__(self, comedian_List, demographic_List):
        self.comedian_List = comedian_List
        self.demographic_List = demographic_List

    def prune(self, comedian, matches):
        for match in matches:
            if comedian in matches[match]:
                matches[match].remove(comedian)
        return matches

    slots = [
        [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5],
        [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5],
        [4, 1], [4, 2], [4, 3], [4, 4], [4, 5]
        ]

    # change to python _   case
    def next_slot(self, slot):
        self.slots.remove(slot)
        if len(self.slots) > 0:
            return self.slots[0]

    def check_constraints(self, comedian, assignments, day):
        count = 0
        for a in assignments:
            if comedian == assignments[a]:
                if a[0] == day:
                    return False
                day = a[0]
                count += 1
        if count > 1:
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
        matches = {}
        for demographic in self.demographic_List:
            matches[demographic] = []
            for comedian in self.comedian_List:
                match = True
                for topic in demographic.topics:
                    if topic not in comedian.themes:
                        match = False
                        break
                if match:
                    matches[demographic].append(comedian)

        assigned = {}

        # could find a way to sort matches ascending in length of comedians that can fulfill the show?
        for group in matches:

            if len(matches[group]) == 1:
                comedian = matches[group][0]
                while not self.check_constraints(comedian, assigned, slot[0]):
                    slot = self.slots[self.slots.index(slot)+1]
                # get new slot
                timetableObj.addSession(days[slot[0]], slot[1], comedian, group, "main")
                assigned[tuple(slot)] = comedian
                print("Assigning " + comedian.name + " to " + days[slot[0]])
                slot = self.next_slot(slot)

        for group in matches:
            if len(matches[group]) > 1:
                selected = 0
                comedian = matches[group][selected]
                while not self.check_constraints(comedian, assigned, slot[0]) and selected < len(matches[group]) -1:
                    selected += 1
                    comedian = matches[group][selected]
                # Maybe use a stack in case a comedian is used twice you can backtrack and use a different one
                timetableObj.addSession(days[slot[0]], slot[1], comedian, group, "main")
                assigned[tuple(slot)] = comedian
                print("assigning " + comedian.name + " to " + days[slot[0]])
                slot = self.next_slot(slot)
                # do something here using while loop
        return timetableObj
