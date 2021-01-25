import timetable


class Scheduler:

    def __init__(self, comedian_list, demographic_list):
        self.comedian_list = comedian_list
        self.demographic_list = demographic_list
        # slots lists optimised for each task
        self.task1_slots = [
            [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5],
            [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5],
            [4, 1], [4, 2], [4, 3], [4, 4], [4, 5]
        ]
        self.task2_slots = [
            [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10],
            [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [1, 10],
            [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9], [2, 10],
            [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8], [3, 9], [3, 10],
            [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7], [4, 8], [4, 9], [4, 10],
        ]
        self.task3_slots = [
            [0, 1], [1, 1], [0, 2], [1, 2], [0, 3], [1, 3], [0, 4], [1, 4], [0, 5], [1, 5],
            [0, 6], [1, 6], [0, 7], [1, 7], [0, 8], [1, 8], [0, 9], [1, 9], [0, 10], [1, 10],
            [2, 1], [3, 1], [2, 2], [3, 2], [4, 5], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7],
            [2, 8], [2, 9], [2, 10], [3, 3], [3, 4], [3, 5], [3, 6], [4, 1], [4, 2], [4, 3],
            [4, 4], [3, 7], [3, 8], [3, 9], [3, 10], [4, 6], [4, 7], [4, 8], [4, 9], [4, 10],
        ]
        # dicts and list used in tasks
        self.assigned = {}
        self.main_assigned = {}
        self.test_assigned = {}
        self.used_mains = []
        self.used_tests = []

    # Using the comedian_List and demographic_List, create a timetable of 5 slots for each of the 5 work days of the
    # week. The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
    # timetableObj.addSession("Monday", 1, comedian_Obj, demographic_Obj, "main") This line will set the session slot
    # '1' on Monday to a main show with comedian_obj, which is being marketed to demographic_obj. Note here that the
    # comedian and demographic are represented by objects, not strings. The day (1st argument) can be assigned the
    # following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday" The slot (2nd argument) can be
    # assigned the following values: 1, 2, 3, 4, 5 in task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in tasks 2 and 3.
    # Comedian (3rd argument) and Demographic (4th argument) can be assigned any value, but if the comedian or
    # demographic are not in the original lists, your solution will be marked incorrectly. The final, 5th argument,
    # is the show type. For task 1, all shows should be "main". For task 2 and 3, you should assign either "main" or
    # "test" as the show type. In tasks 2 and 3, all shows will either be a 'main' show or a 'test' show

    # demographic_List is a list of Demographic objects. A Demographic object, 'd' has the following attributes:
    # d.reference  - the reference code of the demographic d.topics - a list of strings, describing the topics that
    # the demographic like to see in their comedy shows e.g. ["Politics", "Family"]

    # comedian_List is a list of Comedian objects. A Comedian object, 'c', has the following attributes: c.name - the
    # name of the Comedian c.themes - a list of strings, describing the themes that the comedian uses in their comedy
    # shows e.g. ["Politics", "Family"]

    # For Task 1: Keep in mind that a comedian can only have their show marketed to a demographic if the comedian's
    # themes contain every topic the demographic likes to see in their comedy shows. Furthermore, a comedian can only
    # perform one main show a day, and a maximum of two main shows over the course of the week. There will always be
    # 25 demographics, one for each slot in the week, but the number of comedians will vary. In some problems,
    # demographics will have 2 topics and in others, 3. A comedian will have between 3-8 different themes.

    # For Task 2 and 3: A comedian can only have their test show marketed to a demographic if the comedian's themes
    # contain at least one topic that the demographic likes to see in their comedy shows. Comedians can only manage a
    # 4 hours of stage time, where main shows 2 hours and test shows are 1 hour. A Comedian can not be on stage for
    # more than 2 hours a day.

    # You should not use any other methods and/or properties from the classes, these five calls are the only methods
    # you should need. Furthermore, you should not import anything else beyond what has been imported above. To
    # reiterate, the five calls are timetableObj.addSession, d.name, d.genres, c.name, c.talents

    # This method should return a timetable object with a schedule that is legal according to all constraints of task 1.

    # Method for getting the next slot to assign in the timetable
    def next_slot(self, slot, task):
        # remove original slot and get next available slot
        if task == 1:
            self.task1_slots.remove(slot)
            slots = self.task1_slots
        elif task == 2:
            self.task2_slots.remove(slot)
            slots = self.task2_slots
        else:
            self.task3_slots.remove(slot)
            slots = self.task3_slots
        if len(slots) > 0:
            return slots[0]
        else:
            return []

    # Static method to sort a provided dictionary of matches. Sorted by the length of the value (a list)
    @staticmethod
    def sort_dict(dictionary):
        # Sort keys by length of their value
        sorted_keys = sorted(dictionary, key=lambda demographic: len(dictionary[demographic]))
        new_dict = {}
        # Copy values into a new dictionary
        for i in range(0, len(sorted_keys)):
            new_dict[sorted_keys[i]] = dictionary[sorted_keys[i]]
        return new_dict

    # Constraint checker for task 1
    # Checks that a comedian hasn't already performed two shows and hasn't already performed on the selected day
    def task1_constraints(self, selected_comedian, day):
        count = 0
        # Loop through assigned matches
        for a in self.assigned:
            if selected_comedian == self.assigned[a]:
                # False if comedian is already performing that day
                if a[0] == day:
                    return False
                # Otherwise increase count
                count += 1
        # False if performing two shows already
        if count > 1:
            return False
        return True

    # Constraint checker for task 2
    # Checks that a comedian hasn't already performed more than 2 hours in one day, or more than 4 hours in total
    def task2_constraints(self, selected_comedian, day):
        count = 0
        day_hours = 0
        # Loop through
        for a in self.assigned:
            if selected_comedian == self.assigned[a][0]:
                # If comedian has performed a main show on same day return false otherwise note the hours
                if self.assigned[a][1] == "main":
                    if a[0] == day:
                        return False
                    count += 2
                # If comedian has performed a test show count the hours for the week and day itself
                elif self.assigned[a][1] == "test":
                    count += 1
                    if a[0] == day:
                        day_hours += 1
        # False if they have already performed 4 hours of shows in the week or 2 hours in the day
        if count > 3 or day_hours > 1:
            return False
        return True

    # Constraint checker for task 3
    # Checks a specific comedian/demographic match to make sure the demographic hasn't already been assigned main/test
    # shows. Also checks the hours in one week
    def task3_constraints(self, selected_comedian, group, day, show_type):
        count = 0
        day_hours = 0
        # Loop through assigned matches
        for a in self.assigned:
            # If the demographic has been assigned for that particular show type return false
            if group == self.assigned[a][2]:
                if show_type == self.assigned[a][1]:
                    return False
            # Check comedian hasn't worked the maximum number of hours already
            if selected_comedian == self.assigned[a][0]:
                if self.assigned[a][1] == "main":
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

    # Method for calculating the cost of putting a match in a specific slot, used in task 3
    @staticmethod
    def cost(selected_comedian, slot, assignments, show_type):
        # Multiplier for test shows on same day as each other
        multiplier = 1
        count = 0
        # Default values
        if show_type == 'main':
            cost = 500
        else:
            cost = 250
        # Loop through assigments
        for a in assignments:
            if selected_comedian == assignments[a][0]:
                # If test show is on the same day as another set multiplier to 1/2
                if a[0] == slot[0]:
                    multiplier = 0.5
                # If already performed a main show, this one will be 300 or 100 if on a conescutive day
                if assignments[a][1] == "main":
                    if show_type == "main":
                        cost = 300
                        if a[0] == slot[0] - 1:
                            return 100
                # Count previous test shows to calculate cost for current
                if assignments[a][1] == "test":
                    count += 1
        # Calculate cost for test show using previous count and multiplier
        if show_type == "test":
            cost = cost - (count * 50)
            cost = cost * multiplier
        return cost

    # Heuristic function for minimum cost scheduler
    def heuristic(self, match, slot, comedians_list, demos_list, show_type):

        # Comedian and demographic
        com = match[0]
        demo = match[1]

        # If it violates constraints assign a value of 0
        if not self.task3_constraints(com, demo, slot[0], show_type):
            return 0

        # CLEAN THIS UP
        if len(comedians_list[com]) == 1 and len(demos_list[demo]) == 1 and com not in self.used_mains:
            return 9999
        if len(comedians_list[com]) < 2 and com not in self.used_mains and show_type == "main":
            return 0.0001
        if len(comedians_list[com]) < 4 and com not in self.used_tests and show_type == "test":
            return 0.0001
        if show_type == "test" and com in self.used_mains:
            return 0.0001

        # Prioritise assigning necessary comedians with fewer possible shows (mains)
        aspect1 = 1 / len(comedians_list[com])
        # If assigning for test shows halve the influence of this number
        if show_type == "test":
            aspect1 = len(comedians_list[com]) * 0.5
        # Prioritise assigning necessary demographics with fewer possible comedians that can perform them
        aspect2 = 1 / len(demos_list[demo])
        # Prioritise assigning comedians who have already performed a show/shows
        if show_type == "test":
            aspect1 += self.used_tests.count(com)
        else:
            aspect1 += self.used_mains.count(com) * 5
        # Prioritise shows with a lower cost
        cost = 1 / (self.cost(com, slot, self.assigned, "main") / 50)
        return aspect1 + aspect2 + cost

    # Method to prune used demographics from a list of matches to maintain accuracy of heuristic
    @staticmethod
    def prune_used(main_comedians, group):
        for com in main_comedians:
            if group in main_comedians[com]:
                main_comedians[com].remove(group)
        return main_comedians

    # This method models the problem as a CSP (with another inside).
    # The variables in the outer CSP are the slots in the timetable, with the domain being the matches between demo
    # graphic and comedian. The matches themselves are similar with the domains being the demographics and the variables
    # being the comedians that can perform a show for them.
    # The constraints in question are relatively simple in that a comedian may not be selected more than 2 times and
    # a value may not be used twice in one day. These constraints are enforced by the task1_constraints method.
    # The assignment of the matches is ordered by how many comedians can fulfill the show, meaning there should never
    # be a need to backtrack or forward check. For example if a show has only one comedian who can perform it they will
    # be assigned first before any others even if the comedian has other possible shows they could perform.
    def createSchedule(self):
        # Do not change this line
        timetableObj = timetable.Timetable(1)

        # Slot and list of days
        slot = [0, 1]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        matches = {}
        # Loop through demographics
        for demo in self.demographic_list:
            matches[demo] = []
            # Loop through comedians
            for com in self.comedian_list:
                match = True
                # If the comedian does not have all topics required for demographic skip
                for topic in demo.topics:
                    if topic not in com.themes:
                        match = False
                        break
                # Otherwise add comedian to the list of demographic's matches
                if match:
                    matches[demo].append(com)
        # Sort demographics by number of comedians that can perform them (ascending)
        matches = self.sort_dict(matches)

        # Loop through all possible matches
        for group in matches:
            selected = 0
            # Select the first possible comedian
            selected_comedian = matches[group][selected]
            # If there is only one possible comedian
            if len(matches[group]) == 1:
                # Find a slot for it that does not violate constraints
                while not self.task1_constraints(selected_comedian, slot[0]):
                    slot = self.task1_slots[self.task1_slots.index(slot) + 1]
            # If this match violates constraints then pick the next one
            while not self.task1_constraints(selected_comedian, slot[0]) and selected < len(matches[group]) - 1:
                selected += 1
                selected_comedian = matches[group][selected]
            # Add match to timetable
            timetableObj.addSession(days[slot[0]], slot[1], selected_comedian, group, "main")
            # Add to the list of assigned matches
            self.assigned[tuple(slot)] = selected_comedian
            # DEBUG PRINT
            #print("Assigning " + selected_comedian.name + " to " + days[slot[0]])

            # Get the next available slot
            slot = self.next_slot(slot, 1)

        # Do not change this line
        return timetableObj

    # This task is modelled similarly to the task above but duplicated for test shows and with slightly different
    # constraints Comedians are now only allowed to be chosen once by main show variables, though they are still
    # allowed to be chosen twice by test show variables. Main shows are assigned first, with the method only checking
    # constraints on comedians who have the ability to perform at least one main show. As above, this method requires
    # no backtracking or forward checking as it assigns in order of |V|.
    def createTestShowSchedule(self):
        # Do not change this line
        timetableObj = timetable.Timetable(2)

        # Slots and dicts
        slot = [0, 1]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        main = {}
        test = {}

        # Loop through demographics
        for demo in self.demographic_list:
            main[demo] = []
            test[demo] = []
            # Loop through comedians
            for com in self.comedian_list:
                match_main = True
                match_test = False
                # If they don't contain all matching themes set main flag to false
                # If they match at least one theme set test flag to true
                for topic in demo.topics:
                    if topic not in com.themes:
                        match_main = False
                    elif topic in com.themes:
                        match_test = True

                # Add to the correct dictionary
                if match_main:
                    main[demo].append(com)
                elif match_test:
                    test[demo].append(com)

        # Sort main matches by number of comedians who can match
        main = self.sort_dict(main)
        test = self.sort_dict(test)

        # Loop through matches
        for group in main:
            selected = 0
            # Choose the first in the list
            selected_comedian = main[group][selected]
            # If only one comedian
            if len(main[group]) < 2:
                # Loop through slots until a match is found
                while not self.task2_constraints(selected_comedian, slot[0]):
                    slot = self.task2_slots[self.task2_slots.index(slot) + 1]
            # If comedian violates constraints then pick the next comedian in list
            while not self.task2_constraints(selected_comedian, slot[0]) and selected < len(main[group]) - 1:
                selected += 1
                selected_comedian = main[group][selected]
            # Add match to the timetable
            timetableObj.addSession(days[slot[0]], slot[1], selected_comedian, group, "main")
            # Add match to the list of assigned matches
            self.assigned[tuple(slot)] = (selected_comedian, "main")

            # DEBUG PRINT
            # print("Assigning " + comedian.name + " to " + days[slot[0]] + " show type: Main")

            # Get the next slot
            slot = self.next_slot(slot, 2)

        # Loop test matches
        for group in test:
            selected = 0
            # Select first comedian
            selected_comedian = test[group][selected]
            # Select the next one until one is found that does not violate constraints
            while not self.task2_constraints(selected_comedian, slot[0]) and selected < len(test[group]) - 1:
                selected += 1
                selected_comedian = test[group][selected]
            # Add match to timetable object
            timetableObj.addSession(days[slot[0]], slot[1], selected_comedian, group, "test")
            self.assigned[tuple(slot)] = (selected_comedian, "test")
            # DEBUG PRINT
            # print("Assigning " + comedian.name + " to " + days[slot[0]] + " show type: Test")

            # Get next slot
            slot = self.next_slot(slot, 2)

        # Do not change this line
        return timetableObj

    # This tasks takes aspects of the previous task but implements them differently. For this task I decided to try
    # and implement an A* search algorithm using a heuristic function. I first began with a basic heuristic based
    # solely on the cost of the show that was going to be assigned. From there I began to optimise the heuristic by
    # taking into consideration factors such as how many possible alternative shows the comedian could perform,
    # how many other comedians could perform for the demographic as well as how many times the comedian has performed
    # already. I tweaked these numbers until I ended with a heuristic function that correctly selected the optimal
    # shows for each example problem we were provided. I also generated some additional example problems to test it
    # on. The algorithm in this function works by calculating heuristic values for all matches (or nodes in the
    # tree), then selecting the one with the highest value (which represents lowest path cost). This is then repeated
    # starting from the selected node until either the goal state is found or no more nodes/matches remain with a
    # heuristic value greater than 0. The heuristic function also contains a set of predetermined conditions made for
    # specific irregular cases such as where a comedian can only perform one show for a demographic who only has one
    # comedian that can perform it. This is assigned a value that is higher than any possible value for a show to make
    # sure it is definitely assigned.
    # For this task I put the slot list in an order such that it represents the optimal layout of test shows and main
    # shows that can be assigned.
    def createMinCostSchedule(self):
        # Do not change this line
        timetableObj = timetable.Timetable(3)

        # Slots, lists and dicts
        slot = [0, 1]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        main_comedians = {}
        test_comedians = {}
        main_demos = {}
        test_demos = {}
        main_matches = []
        test_matches = []
        # Key for intialisation of dicts
        key = True
        # Loop through comedians
        for com in self.comedian_list:
            main_comedians[com] = []
            test_comedians[com] = []
            # Loop through demographics
            for demo in self.demographic_list:
                # If its the first in loop, initialise dict entry
                if key:
                    main_demos[demo] = []
                    test_demos[demo] = []

                match_main = True
                match_test = False
                # If the comedian and demographic does not have all same themes set main flag to false
                # If comedian does not have all but at least one set test flag to true
                for topic in demo.topics:
                    if topic not in com.themes:
                        match_main = False
                    elif topic in com.themes:
                        match_test = True

                # Add comedian and demographic to respective dictionaries/lists for later
                if match_main:
                    main_matches.append((com, demo))
                    main_comedians[com].append(demo)
                    main_demos[demo].append(com)
                elif match_test:
                    test_matches.append((com, demo))
                    test_comedians[com].append(demo)
                    test_demos[demo].append(com)

            # Set key to false after first iteration
            key = False

        # Debug statements for cost
        # main_cost = 0
        # test_cost = 0

        # Loop through each main slot
        for x in range(0, 25):
            # Max value for finding largest heuristic value match
            max_value = 0
            chosen = ()
            # Loop through main matches
            for match in main_matches:
                # If heuristic value is greater than highest found
                if self.heuristic(match, slot, main_comedians, main_demos, "main") > max_value:
                    # Set max value to that and chosen match
                    max_value = self.heuristic(match, slot, main_comedians, main_demos, "main")
                    chosen = match
            # If max value is 9999 (flag for comedian has 1 match only, demographic main show can only be filled by
            # that individual comedian
            if max_value == 9999:
                # Assign it to the wildcard slot in the timetable if it hasn't already been filled~ =
                if [4, 5] in self.task3_slots:
                    slot = [4, 5]
            # If no match exists with heuristic > 0 then timetable does not exist
            if chosen == ():
                print("Unable to generate timetable")
                return

            # DEBUG PRINTS
            # print("Assigning " + chosen[0].name + " to " + chosen[1].reference + " " + days[slot[0]] + " cost " + str(
            #            self.cost(chosen[0], slot, self.assigned, "main")))

            # Add chosen match to the timetable
            timetableObj.addSession(days[slot[0]], slot[1], chosen[0], chosen[1], "main")
            # Cost debug
            # main_cost += self.cost(chosen[0], slot, self.assigned, "main")

            # Add to used/assigned lists/dicts
            self.assigned[tuple(slot)] = (chosen[0], "main", chosen[1])
            self.used_mains.append(chosen[0])
            # Prune matches containing the recently assigned comedian/demographic
            main_comedians = self.prune_used(main_comedians, chosen[1])
            main_matches.remove(chosen)
            # Get next slot
            slot = self.next_slot(slot, 3)

        # Loop through test show slots
        for x in range(0, 25):
            # Loop matches getting maximum value
            max_value = 0
            chosen = ()
            for match in test_matches:
                if self.heuristic(match, slot, test_comedians, test_demos, "test") > max_value:
                    max_value = self.heuristic(match, slot, test_comedians, test_demos, "test")
                    chosen = match

            # Flag for match with demographic that only has one possible comedian to assign it and that comedian has
            # only one possible test show
            if max_value == 9999:
                # If wildcard slot is empty assign it there
                if [4, 6] in self.task3_slots:
                    slot = [4, 6]

            # DEBUG PRINTS
            # print("Assigning " + chosen[0].name + " to " + chosen[1].reference + " " + days[slot[0]] + " cost " + str(
            #            self.cost(chosen[0], slot, self.assigned, "test")))
            # print("Heuristic value: "+ str(self.heuristic(chosen, slot, test_comedians, test_demos, "test")))

            # Add match to timetable
            timetableObj.addSession(days[slot[0]], slot[1], chosen[0], chosen[1], "test")

            # Add match to used/assigned lists
            self.used_tests.append(chosen[0])

            # Cost debug
            # test_cost += self.cost(chosen[0], slot, self.assigned, "test")

            self.assigned[tuple(slot)] = (chosen[0], "test", chosen[1])

            # Prune match from lists
            test_comedians = self.prune_used(test_comedians, chosen[1])
            test_matches.remove(chosen)
            slot = self.next_slot(slot, 3)

        # DEBUGGING PRINTS
        # print("Main cost (optimal 7700): " + str(main_cost))
        # print("Test cost (optimal 2350): "+str(test_cost))
        # print("Total cost (optimal 10050): "+ str(test_cost + main_cost))

        # Do not change this line
        return timetableObj
