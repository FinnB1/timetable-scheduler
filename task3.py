import comedian
import demographic
import ReaderWriter
import timetable
import random
import math


class task3_scheduler:

    def __init__(self, comedian_List, demographic_List):
        self.comedian_List = comedian_List
        self.demographic_List = demographic_List

    slots = [
        [0, 1], [1, 1], [0, 2], [1, 2], [0, 3], [1, 3], [0, 4], [1, 4], [0, 5], [1, 5],
        [0, 6], [1, 6], [0, 7], [1, 7], [0, 8], [1, 8], [0, 9], [1, 9], [0, 10], [1, 10],
        [2, 1], [3, 1], [2, 2], [3, 2], [4, 5], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8],
        [2, 9], [2, 10], [3, 3], [3, 4], [3, 5], [3, 6], [4, 1], [4, 2], [4, 3], [4, 4],
        [3, 7], [3, 8], [3, 9], [3, 10], [4, 6], [4, 7], [4, 8], [4, 9], [4, 10],
        ]

    assigned = {}
    used_mains = []
    used_tests = []
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

    def check_constraints(self, comedian, group, assignments, day, show_type):
        count = 0
        day_hours = 0
        for a in assignments:
            if group == assignments[a][2]:
                if show_type == assignments[a][1]:
                    return False
            if comedian == assignments[a][0]:
                if assignments[a][1] == "main":
                    if a[0] == day:
                        return False
                    count += 2
                else:
                    count += 1
                    if a[0] == day:
                        day_hours += 1
        if count > 3 or day_hours > 1:
            return False
        return True


    def cost(self, comedian, slot, assignments, show_type):
        multiplier = 1
        count = 0
        if show_type == 'main':
            cost = 500
        else:
            cost = 250
        for a in assignments:
            if comedian == assignments[a][0]:
                if a[0] == slot[0]:
                    multiplier = 0.5
                if assignments[a][1] == "main":
                    if show_type == "main":
                        cost = 300
                        if a[0] == slot[0] - 1:
                            return 100
                if assignments[a][1] == "test":
                    count += 1
        if show_type == "test":
            cost = cost - (count * 50)
            cost = cost * multiplier
        return cost

    def heuristic(self, match, slot, comedians_list, demos_list, show_type):

        com = match[0]
        demo = match[1]

        if not self.check_constraints(com, demo, self.assigned, slot[0], show_type):
            return 0

        if len(comedians_list[com]) + len(demos_list[demo]) == 2:
            return 9999

        if len(comedians_list[com]) < 2:
            return 0.0001
        aspect1 = len(comedians_list[com]) / 5
        aspect2 = 0.5 / len(demos_list[demo])

        if show_type == "test":
            aspect1 += self.used_tests.count(com)
        else:
            aspect1 += self.used_mains.count(com)

        cost = 1 / (self.cost(com, slot, self.assigned, "main") / 50)
        return aspect1 + aspect2 + cost




    # This simplistic approach merely assigns each demographic and comedian to a random, iterating through the
    # timetable.
    def schedule(self, timetableObj):
        slot = [0, 1]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        # put in init
        main_comedians = {}
        test_comedians = {}
        main_demos = {}
        test_demos = {}
        main_matches = []
        test_matches = []
        key = True
        for comedian in self.comedian_List:
            main_comedians[comedian] = []
            test_comedians[comedian] = []
            for demographic in self.demographic_List:
                if key:
                    main_demos[demographic] = []
                    test_demos[demographic] = []
                match_main = True
                match_test = False
                for topic in demographic.topics:
                    if topic not in comedian.themes:
                        match_main = False
                    elif topic in comedian.themes:
                        match_test = True
                        
                if match_main:
                    main_matches.append((comedian, demographic))
                    main_comedians[comedian].append(demographic)
                    main_demos[demographic].append(comedian)
                elif match_test:
                    test_matches.append((comedian, demographic))
                    test_comedians[comedian].append(demographic)
                    test_demos[demographic].append(comedian)

            key = False

        used_groups = []
        used_comedians = []

        main_demos = self.sort_dict(main_demos)
        main_comedians = self.sort_dict(main_comedians)
        # go through comedians in order of least possible mains, getting them to fill in two slots at a time in consecutive days following
        # the timetabled spreadhseet image
        needed = []
        main_cost = 0
        test_cost = 0
        print(main_comedians)
        print(main_comedians[self.comedian_List[0]])
        print(main_comedians[self.comedian_List[13]])

        for x in range (0, 25):
            max = 0
            chosen = ()
            for match in main_matches:
                if self.heuristic(match, slot, main_comedians, main_demos, "main") > max:
                    max = self.heuristic(match, slot, main_comedians, main_demos, "main")
                    chosen = match
            if max == 9999:
                if [4, 5] in self.slots:
                    slot = [4, 5]
            if chosen == ():
                print("UH OH!!!!")
            print("assigning " + chosen[0].name + " to " + chosen[1].reference + " " + days[slot[0]] + " cost " + str(
                       self.cost(chosen[0], slot, self.assigned, "main")))
            print(self.heuristic(chosen, slot, main_comedians, main_demos, "main"))
            timetableObj.addSession(days[slot[0]], slot[1], chosen[0], chosen[1], "main")
            main_cost += self.cost(chosen[0], slot, self.assigned, "main")
            self.assigned[tuple(slot)] = (chosen[0], "main", chosen[1])
            self.used_mains.append(chosen[0])
            main_matches.remove(chosen)
            slot = self.next_slot(slot)

        last_comedian = []
        running_cost = 0
        for x in range (0, 25):
            max = 0
            chosen = ()
            for match in test_matches:
                if self.heuristic(match, slot, test_comedians, test_demos, "test") > max:
                    max = self.heuristic(match, slot, test_comedians, test_demos, "test")
                    chosen = match

            if max == 8888:
                if [4, 6] in self.slots:
                    slot = [4, 6]
            print("assigning " + chosen[0].name + " to " + chosen[1].reference + " " + days[slot[0]] + " cost " + str(
                       self.cost(chosen[0], slot, self.assigned, "test")))
            print(self.heuristic(chosen, slot, test_comedians, test_demos, "test"))
            timetableObj.addSession(days[slot[0]], slot[1], chosen[0], chosen[1], "test")
            self.used_tests.append(chosen[0])
            if chosen[0] in last_comedian:
                print("minus " + str(((self.cost(chosen[0], slot, self.assigned, "test") * 2) + 50) / 2))
                test_cost -= ((self.cost(chosen[0], slot, self.assigned, "test") * 2) + 50) / 2
                last_comedian.remove(chosen[0])
            else:
                last_comedian.append(chosen[0])
            print("plus "+ str(self.cost(chosen[0], slot, self.assigned, "test")))
            test_cost += self.cost(chosen[0], slot, self.assigned, "test")
            self.assigned[tuple(slot)] = (chosen[0], "test", chosen[1])
            test_matches.remove(chosen)
            slot = self.next_slot(slot)
        print("Main cost (optimal 7700): " + str(main_cost))
        print("Test cost (optimal 2350): "+str(test_cost))
        print("Total cost (optimal 10050): "+ str(test_cost + main_cost))





        # for group in main_demos:
        #     if len(main_demos[group]) == 1:
        #         needed.append((main_demos[group][0], group))
        #     else:
        #         break
        # for t in needed:
        #     comedian = t[0]
        #     group = t[1]
        #     if len(main_comedians[comedian]) > 1 and comedian not in used_comedians:
        #         print("assigning " + comedian.name + " to " + group.reference + " " + days[slot[0]] + " cost " + str(
        #             self.cost(comedian, slot, self.assigned, "main")))
        #         print(self.heuristic((comedian, group), slot, main_comedians, main_demos))
        #         timetableObj.addSession(days[slot[0]], slot[1], comedian, group, "main")
        #         self.assigned[tuple(slot)] = (comedian, "main")
        #         used_groups.append(group)
        #         slot[0] += 1
        #         selected_group = 0
        #         # potentially make a method "assign_pair()", with  also "assign_single()" for when there exists a comedian
        #         # whom is the only comedian for a certain show and ONLY that show
        #         if needed.count(comedian) > 1:
        #             first_group = needed.index(comedian)
        #             group = needed[first_group+1:].index(comedian)
        #         else:
        #             while group == main_comedians[comedian][selected_group] and main_comedians[comedian][selected_group] in used_groups:
        #                 selected_group += 1
        #             group = main_comedians[comedian][selected_group]
        #         print("assigning " + comedian.name + " to " + group.reference + " " + days[slot[0]] + " cost " + str(
        #             self.cost(comedian, slot, self.assigned, "main")))
        #         print(self.heuristic((comedian, group), slot, main_comedians, main_demos))
        #         timetableObj.addSession(days[slot[0]], slot[1], comedian, group, "main")
        #         used_groups.append(group)
        #         self.assigned[tuple(slot)] = (comedian, "main")
        #         slot = self.next_slot(slot)
        #         used_comedians.append(comedian)
        # for comedian in main_comedians:
        #     if len(main_comedians[comedian]) > 1 and comedian not in used_comedians:
        #         selected = 0
        #         mains = []
        #         while len(mains) < 3 and selected < len(main_comedians[comedian]) - 1:
        #             if main_comedians[comedian][selected] not in used_groups:
        #                 mains.append(main_comedians[comedian][selected])
        #             selected += 1
        #         if len(mains) < 2:
        #             continue
        #         else:
        #             print(
        #                 "assigning " + comedian.name + " to " + mains[0].reference + " " + days[slot[0]] + " cost " + str(
        #                     self.cost(comedian, slot, self.assigned, "main")))
        #             print(self.heuristic((comedian, group), slot, main_comedians, main_demos))
        #             timetableObj.addSession(days[slot[0]], slot[1], comedian, mains[0], "main")
        #             self.assigned[tuple(slot)] = (comedian, "main")
        #             used_groups.append(mains[0])
        #             slot[0] += 1
        #             # potentially make a method "assign_pair()", with  also "assign_single()" for when there exists a comedian
        #             # whom is the only comedian for a certain show and ONLY that show
        #             print(
        #                 "assigning " + comedian.name + " to " + mains[1].reference + " " + days[slot[0]] + " cost " + str(
        #                     self.cost(comedian, slot, self.assigned, "main")))
        #             print(self.heuristic((comedian, group), slot, main_comedians, main_demos))
        #             timetableObj.addSession(days[slot[0]], slot[1], comedian, mains[1],
        #                                     "main")
        #             self.assigned[tuple(slot)] = (comedian, "main")
        #             used_groups.append(mains[1])
        #             slot = self.next_slot(slot)
        #             used_comedians.append(comedian)
        #
        #


        # for group in main:
        #
        #     if len(main[group]) == 1:
        #         comedian = main[group][0]
        #         while not self.check_constraints(comedian, assigned, slot[0]):
        #             slot = self.slots[self.slots.index(slot)+1]
        #         # get new slot
        #         timetableObj.addSession(days[slot[0]], slot[1], comedian, group, "main")
        #         print("Assigning " + comedian.name + " to " + days[slot[0]] + " cost " + str(self.cost(comedian, slot, assigned, "main")))
        #         assigned[tuple(slot)] = (comedian, "main")
        #         slot = self.next_slot(slot)
        #
        # for group in main:
        #     if len(main[group]) > 1:
        #         selected = 0
        #         comedian = main[group][selected]
        #         while not self.check_constraints(comedian, assigned, slot[0]) and selected < len(main[group]) -1:
        #             selected += 1
        #             comedian = main[group][selected]
        #         # Maybe use a stack in case a comedian is used twice you can backtrack and use a different one
        #         timetableObj.addSession(days[slot[0]], slot[1], comedian, group, "main")
        #         print("assigning " + comedian.name + " to " + days[slot[0]] + " cost " + str(self.cost(comedian, slot, assigned, "main")))
        #         assigned[tuple(slot)] = (comedian, "main")
        #         slot = self.next_slot(slot)
        # for group in test:
        #     selected = 0
        #     comedian = test[group][selected]
        #     while not self.check_constraints(comedian, assigned, slot[0]) and selected < len(test[group]) - 1:
        #         selected += 1
        #         comedian = test[group][selected]
        #     # Maybe use a stack in case a comedian is used twice you can backtrack and use a different one
        #     timetableObj.addSession(days[slot[0]], slot[1], comedian, group, "test")
        #     print("TEST assigning " + comedian.name + " to " + days[slot[0]] + " cost " + str(self.cost(comedian, slot, assigned, "test")))
        #     assigned[tuple(slot)] = (comedian, "test")
        #     slot = self.next_slot(slot)
        return timetableObj
