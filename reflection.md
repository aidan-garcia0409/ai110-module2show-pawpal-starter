# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
There are three essential classes. Owner, Pet, and Schedules. Owners own pets and pets have schedules that are generated for them.
- What classes did you include, and what responsibilities did you assign to each?
See above.
**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used claude code with GSD running. This turns claude code into a more robust design partner that helped me to actually map out the precise functionality of features of the project ahead of time, leaving less room for assumptions. Additionally it prompted me to provide core classes and methods for this assignment.
- What kinds of prompts or questions were most helpful?
I provided it details that this was a learning assignment and how I wanted to go about designing this and it made sure to prompt me for input as it went about scaffolding the plan for this assignment.
**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
It initially developed a really broadscope app that covered all kinds of animals including birds and reptiles and small rodents. I felt that this was beyond the scope of what PawPal needed to be, so I had it reign in it's focus so that it could create a more polished and focused final product.
- How did you evaluate or verify what the AI suggested?
I evaluated it based on what I thought the app actually needed to be given the scope of the assignment. I then looked at the plan it vae me and decided that it was too broad and would likely result in a more complicated and unpolished product.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested that it would know when there wasn't enough room in the schedule. That it wouldn't build a schedule with no tasks. That schedules persisted when you updated some info. That it would list skipped tasks. That it would tell you if a task was simply too long.
- Why were these tests important?
These were all of the tests that allowed for the schedule to catch basic error cases and make sure that it was able to perform it's general functionality.
**b. Confidence**

- How confident are you that your scheduler works correctly?
I feel fairly confident that this is working correctly.
- What edge cases would you test next if you had more time?
I would likely spend more time testing out the priority handling to see if it was consistent in building realistic and approproriate schedules.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I'm most satisfied with my testing of a new AI tool as well as knowing when to give it some feedback on what I didn't like about it's initial design.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would likely want to build a UI that is more visually appealing and also build it in a format that would let you save a long term account with pets and schedules that you can always reference on the go.
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
That it's important to look at the suggestions that they make and not just take it as given that what the AI provides is always best.